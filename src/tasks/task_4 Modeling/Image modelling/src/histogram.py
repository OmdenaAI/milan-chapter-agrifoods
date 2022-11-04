import logging,os,math
from utils import read_config,create_dir
from pathlib import Path
import glob
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 


logging.basicConfig(
    filename=os.path.join("logs", 'histogram.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    ) 

class Histogram:
    def __init__(self,config):
        self.npy_dir = Path(config['paths'].get('preproc_dir'))
        self.hist = Path(config['paths'].get('hist_dir'))
        self.yield_data = pd.read_csv(Path(config['paths'].get('yield_file')))
        
        
    def get_files(self):
        files = []
        for file in glob.glob(f'{self.npy_dir}/*/*.npy'):
            files.append(os.path.split(file)[1])
        return files    
    
    @staticmethod
    def filter_timespan(imcol, start_day=49, end_day=305, composite_period=8, bands=9):
        """
        Image collection data of one year,
        filter it between start_day and end_day. If end_day is later than the date
        for which we have data, the image collection is padded with zeros.
      
        """
        start_index = int(math.floor(start_day / composite_period)) * bands
        end_index = int(math.floor(end_day / composite_period)) * bands

        if end_index > imcol.shape[2]:
            padding = np.zeros(
                (imcol.shape[0], imcol.shape[1], end_index - imcol.shape[2])
            )
            imcol = np.concatenate((imcol, padding), axis=2)
        return imcol[:, :, start_index:end_index]

        # pass

    def process(self):
        num_bands =9
        generate = 'histogram'
        num_bins =32
        max_bin_val = 4999
        channels_first=True

        # define all the outputs of this method
        output_images = []
        yields = []
        years = []
        locations = []
        state_county_info = []
        
        processed_files = self.get_files()
        for yield_data in self.yield_data.itertuples():
            year = int(yield_data.Year)
            city = yield_data.City
            reg = yield_data.COD_REG
            uts = yield_data.COD_UTS
            file_name = f"{city}_{year}.npy"
            if file_name in processed_files:
                image = np.load(f"{self.npy_dir}/{city}/{file_name}")
                image = self.filter_timespan(
                    image, start_day=49, end_day=305, bands=num_bands
                )
            # m =np.mean(image,axis=(0,1))
                if generate == "mean":
                    image = (np.sum(image, axis=(0, 1))/ np.count_nonzero(image)* image.shape[2])
                    image[np.isnan(image)] = 0
                elif generate == 'histogram':
                    image = self._calculate_histogram(
                        image,
                        bands=num_bands,
                        num_bins=num_bins,
                        max_bin_val=max_bin_val,
                        channels_first=channels_first,
                        )
                output_images.append(image)
                yields.append(yield_data.value)
                state_county_info.append(np.array([int(reg),int(uts)]))
                years.append(year)
                try:
                    lat, lon = float(yield_data.lat), float(yield_data.lng)
                except ValueError:
                    lat = float(yield_data.lst[:-1])
                    lon = -float(yield_data.lng)
                locations.append(np.array([lon, lat]))
                    
                print(
                        f"City: {city}, Year: {year}, Output shape: {image.shape}"
                    )
       
        np.savez(
            self.hist/f'histogram_all_{"mean" if (generate == "mean") else "full"}.npz',
            output_image=np.stack(output_images),
            output_yield=np.array(yields),
            output_year=np.array(years),
            output_locations=np.stack(locations),
            output_index=np.stack(state_county_info),

        )
        print(f"Finished generating image {generate}s!")
    def _calculate_histogram(self,imagecol, num_bins=32, bands=9, max_bin_val=4999, channels_first=True):
        """
        Given an image collection, turn it into a histogram.
        """
        bin_seq = np.linspace(1, max_bin_val, num_bins + 1)

        hist = []
        for im in np.split(imagecol, imagecol.shape[-1] / bands, axis=-1):
            imhist = []
            for i in range(im.shape[-1]):
                density, _ = np.histogram(im[:, :, i], bin_seq, density=False)
                # max() prevents divide by 0
                imhist.append(density / max(1, density.sum()))
            if channels_first:
                hist.append(np.stack(imhist))
            else:
                hist.append(np.stack(imhist, axis=1))
              
        return np.stack(hist, axis=1)

if __name__ == "__main__":
    config = read_config('./config/config.yaml')
    h = Histogram(config)
    h.process()

