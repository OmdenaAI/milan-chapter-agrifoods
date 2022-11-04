import torch
import pandas as pd 
from pathlib import Path
from bs4 import BeautifulSoup
import matplotlib as mpl
from matplotlib import pyplot as plt
from utils import read_config
import os,glob
import json

def plot_errors(config):
    model_dir = Path(config['paths'].get("model_dir"))
    svg_file = Path(config['paths'].get("country_svg"))
    save_colorbar = True

    #for cnn model
    
    model= Path(glob.glob(f"{model_dir}/cnn/*.tar")[1])
    model_sd = torch.load(model,map_location='cpu')
    
    real_values = model_sd["test_real"]
    pred_values = model_sd["test_pred"]    

    gp = True
    try:
        gp_values = model_sd["test_pred_gp"]
    except KeyError:
        gp = False

    indices = model_sd["test_indices"]

    pred_err = pred_values - real_values
    pred_dict = {}
    pred_lst= []
    for idx, err in zip(indices, pred_err):
        state, county = idx
        pred_lst.append([int(state), int(county),err])
        state = str(state).zfill(2)
        county = str(county).zfill(3)

        pred_dict[state + county] = err

    model_info = model.name[:-8].split("_")
    colors = [
        "#b2182b",
        "#d6604d",
        "#f4a582",
        "#fddbc7",
        "#d1e5f0",
        "#92c5de",
        "#4393c3",
        "#2166ac",
    ]

    pred_svg = model_dir / f"pred_error_{model_info[0]}_{model_info[1]}"

    # _single_plot(
    #     pred_dict, svg_file, f"{pred_svg}.svg", colors
    # )

    if gp:
        gp_pred_err = gp_values - real_values
        gp_dict = {}
        gp_lst =[]
        for idx, err in zip(indices, gp_pred_err):
            state, county = idx
            gp_lst.append([int(state), int(county),err])
            state = str(state).zfill(2)
            county = str(county).zfill(3)

            gp_dict[state + county] = err

    gp_svg = model_dir / f"{model_info[0]}_{model_info[1]}_gp"


    pd.DataFrame(pred_lst).to_csv(f"{pred_svg}.csv",na_rep=0,header =['COD_REG','COD_UTS','pred_err'],index=False)

    

    # _single_plot(
    #     gp_dict, svg_file, gp_svgf".svg", colors
    # )

    # if save_colorbar:
    #     _save_colorbar(model_dir / "colorbar.png", colors)


def _single_plot(err_dict, svg_file, savepath, colors):

    # load the svg file
    svg = svg_file.open("r").read()
    # Load into Beautiful Soup
    soup = BeautifulSoup(svg, features="html.parser")
    # Find counties
    paths = soup.findAll("path")

    path_style = (
        "font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.1"
        ";stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start"
        ":none;stroke-linejoin:bevel;fill:"
    )

    for p in paths:
        uts=p['cod_reg'].zfill(2)+p['cod_uts'].zfill(3)
        if uts not in ["State_Lines", "separator"]:

            try:
                rate = err_dict[uts]
            except KeyError:
                continue
            if rate > 15:
                color_class = 7
            elif rate > 10:
                color_class = 6
            elif rate > 5:
                color_class = 5
            elif rate > 0:
                color_class = 4
            elif rate > -5:
                color_class = 3
            elif rate > -10:
                color_class = 2
            elif rate > -15:
                color_class = 1
            else:
                color_class = 0

            color = colors[color_class]
            p["style"] = path_style + color
    soup = soup.prettify()
    with savepath.open("w") as f:
        f.write(soup)


def _save_colorbar(savedir, colors):
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.02, 0.8])

    cmap = mpl.colors.ListedColormap(colors[1:-1])

    cmap.set_over(colors[-1])
    cmap.set_under(colors[0])

    bounds = [-15, -10, -5, 0, 5, 10, 15]

    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb = mpl.colorbar.ColorbarBase(
        ax,
        cmap=cmap,
        norm=norm,
        # to use 'extend', you must
        # specify two extra boundaries:
        boundaries=[-20] + bounds + [20],
        extend="both",
        ticks=bounds,  # optional
        spacing="proportional",
        orientation="vertical",
    )
    plt.savefig(savedir, dpi=300, bbox_inches="tight")    

if __name__ == '__main__':
    config = read_config("./config/config.yaml")
    plot_errors(config)

