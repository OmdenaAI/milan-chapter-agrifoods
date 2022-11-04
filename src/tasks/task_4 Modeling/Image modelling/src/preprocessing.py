import os ,glob
from pathlib import Path
import matplotlib.pyplot as plt 
import numpy as np 
import math
from typing import Optional
from osgeo import gdal
import logging
from utils import get_tif_files,read_config,create_dir,check_for_tif_file


logging.basicConfig(
    filename=os.path.join("logs", 'preprocessing.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


class DataProcess:

    def __init__(self,config):
        self.surf_refl_image_dir = Path(config['paths'].get('surf_refl_image_dir'))
        self.surf_temp_image_dir = Path(config['paths'].get('surf_temp_image_dir'))
        self.land_cover_image_dir = Path(config['paths'].get('land_cover_image_dir'))
        self.save_dir = Path(config['paths'].get('preproc_dir'))
        #create output dir if not exists
        if not self.save_dir.exists():
            self.save_dir.mkdir()

    def convert_to_array(self,file_path):
        image = np.transpose(
        np.array(gdal.Open(str(file_path)).ReadAsArray(), dtype="uint16"),
        axes=(1, 2, 0),
        
    )
        return image

    
    def divide_into_years(self,img,bands,image_frq,num_years,extend=True):
        bands_per_year = bands*math.ceil(365/image_frq)
        if extend:
            num_bands_expected = bands_per_year*num_years
            while img.shape[2] < num_bands_expected:
                img = np.concatenate((img,img[:,:,-bands:]),axis=2)

        img_list = []
        idx = 0
        for i in range(0,num_years-1):
            img_list.append(img[:,:,idx:idx+bands_per_year])
            idx+=bands_per_year
        img_list.append(img[:,:,idx:])
        return img_list

    def merge_image_lists(self,img_lst_1,img1_bands,img_lst_2,img2_bands):
        """
        To image the MODIS surface reflectance and the MODIS temperatures),
        merges them together.
        Parameters
        ----------
        img_lst_1: one year surfcace reflectance numpy converted data
        img1_bands_1: surface reflectance bands
        img_lst_2: one year surface temperatures numpy converted data
        img2_bands_2: surface temparature bands_per_year
        Returns
        ----------
        merged_im_list: A merged image list
        """
        merged_list = []
        #check image list length are same or not 
        assert len(img_lst_1) == len(img_lst_2),"Image lists are not the same length!"

        for im1,im2 in zip(img_lst_1,img_lst_2):
            single_image = [] 
            # split year and append images to induvidual images
              
            for image_1, image_2 in zip(
            np.split(im1, im1.shape[-1] / img1_bands, axis=-1),
            np.split(im2, im2.shape[-1] / img2_bands, axis=-1),
            ):
                single_image.append(np.concatenate((image_1,image_2),axis=-1))
            merged_list.append(np.concatenate(single_image,axis=-1))

        return merged_list 

    def mask_image(self,surf_temp_merged,mask_lst):
        """
        Args:
        surf_temp_merged (list):  surface reflectance
        and surface temparature is merged year wise 
        mask_lsit (list): land cover image list per year
        Returns: merged image list 
        """
        masked_img_lst =[] 
        assert len(surf_temp_merged)==len(mask_lst),"Mask and Image lists are not the same length!"

        for img,mask in zip(surf_temp_merged,mask_lst):
            expanded_mask = np.tile(mask, (1, 1, img.shape[2]))
            masked_img = img * expanded_mask
            masked_img_lst.append(masked_img)

        return masked_img_lst

    def process_image_file(self,path,num_years=11):
        path,filename = os.path.split(path)
        logging.info(f">>>>> preprocessing  file {filename} started!<<<<<\n")
        city = filename.split('.')[0].split('_')[-3]
        surf_path = os.path.join(self.surf_refl_image_dir,filename)
        temperature_path = check_for_tif_file(self.surf_temp_image_dir,city)
        mask_path = check_for_tif_file(self.land_cover_image_dir, city)
        
        if not temperature_path:
            logging.info(f"Skipping {filename} - no temperature")
            return None
        if not mask_path:
            logging.info(f"Skipping {filename} - no mask")
            return None


      
        #converting to numpy array
        surf = self.convert_to_array(surf_path)
        temp = self.convert_to_array(temperature_path)
        # From https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD09A1#description,
        # the temperature bands are in Kelvin, with a scale of 0.02. 11500 therefore represents -43C,
        # and (with a bin range of 4999), we get to 16500 which represents 57C - this should
        # comfortably cover the range of expected temperatures for these counties.
        temp -= 11500
        mask = self.convert_to_array(mask_path)
        if surf.shape[0] == 1 and surf.shape[1] == 1:
            logging.info(f'Skipping {filename} - only one pixel')
            return None

        #pixel value is 12 for crop fields   
        mask[mask!=12] = 0
        mask[mask==12] = 1

        #saparate the images into years

        surf_list = self.divide_into_years(surf, bands=7, image_frq=8, num_years=num_years,extend=True)
        mask_list = self.divide_into_years(mask, bands=1, image_frq=365, num_years=num_years, extend=True)
        temp_list = self.divide_into_years(temp, bands=2, image_frq=8, num_years=num_years,extend=True)

        surf_temp_merge = self.merge_image_lists(surf_list, 7, temp_list, 2)

        masked_img_temp = self.mask_image(surf_temp_merge, mask_list)

        start_year = 2012
        for i in range(0,num_years):
            year = i+start_year
            save_file = f"{city}_{year}"
            create_dir(self.save_dir/city)
            np.save(self.save_dir/city/save_file,masked_img_temp[i])



    
if __name__ == "__main__":
    logging.info("\n********************")
    logging.info(f">>>>> stage preprocessing started <<<<<")
    config = read_config('./config/config.yaml')
    p = DataProcess(config)
    img_file_path = 'surf-refl_Alessandria_2012-01-1_2022-09-30.tif'
    image_dir = config['paths'].get('surf_refl_image_dir')
    surf_refl = glob.glob(f'{image_dir}/*.tif')
    for file in surf_refl:
        p.process_image_file(file)
    logging.info(f">>>>> stage preprocessing completed!<<<<<\n")
