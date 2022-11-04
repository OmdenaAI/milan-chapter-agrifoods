import numpy as np 
from utils import read_config
import glob,os
from matplotlib import pyplot as plt
def hist_visulize(hist_file,save_dir,show=True):
    title = 'histogram'
    fig,axarr = plt.subplots(9,sharex=True)
    with np.load(hist_file) as hist:
        images = hist['output_image']
    for idx,image in enumerate(images[:5]):    
        image = np.transpose(image,axes=(2,1,0))    
        num_bands = image.shape[2]
        for band in range(num_bands):
            axarr[band].imshow(image[:,:,band])
    plt.suptitle(title)
    plt.savefig(os.path.join(save_dir, title +'.png'))
    plt.show()




if __name__ == '__main__':
    config = read_config('./config/config.yaml')
    hist_dir = config['paths']['hist_dir'] 
    save_dir = config['paths']['hist_fig_save_dir']
    hist_files = glob.glob(f"{hist_dir}/*.npz")
    hist_visulize(hist_files[1],save_dir)