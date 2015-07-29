import json
import pandas as pd
import glob
import numpy as np
from skimage import io
import matplotlib.cm as cm
from matplotlib import pyplot as plt


class LoadData(object):
    '''load metadata, artifact labels, and pixel intensity of images'''

    def __init__(self):
        # list of properties from metadata used in analysis
        self.prop_list = ['stage_x_current', 'stage_x_position',
                          'stage_y_current', 'stage_y_position',
                          'stage_z_current', 'stage_z_position',
                          'aux_flow_level', 'aux_temp', "slice_queue",
                          'camera_lineFeedback', 'camera_temp']
        self.df = pd.DataFrame()  # dataframe of information about slices

    def load_metadata(self, filename='metadata.json'):
        '''loads metadata as pandas dataframe

        Paramater filename: address of metadata json file
        '''
        f = open(filename)
        self.df = pd.DataFrame(json.loads(f.read()))
        self.df.set_index('sliceIndex', inplace=True)
        self.df = self.df[['time', 'properties']]
        self.df.time = pd.to_datetime(self.df.time, unit='ms')
        for prop in self.prop_list:
            self.df[prop] = self.df.properties.map(lambda x: x[prop])
        self.df.drop('properties', inplace=True, axis=1)

    def label_artifacts(self, bubbles={}, rolling=[]):
        '''Manually label artifacts to train detection algorithms

        Parameters:
        rolling: list of slice indices with rolling.
        bubbles: dictionary containing number of bubbles as the keys and lists
                 of slice indices with that number of bubbles as the values.
                 Slices not in dictionary are set to 0 bubbles.
        '''
        self.df['bubbles'] = 0
        self.df['rolling'] = False
        self.df.rolling[rolling] = True
        for num_bubbles, slice_list in bubbles.iteritems():
            self.df.bubbles[slice_list] = num_bubbles

    def pix_intensity(self, address='images', cutoff=500, left_margin=500,
                      right_margin=700, display=False):
        '''Create df column of average pixel intensity of tops of the images
        Images with rolling will be much darker on top
        
        Parameters:
        address: address of folder containing the images. Assumes the first
                 five characters of each image filename is the slice index.
        cutoff: number of rows of pixels at the top of the image used
        left_margin: number of columns of pixels on the left to ignore
        right_margin: number of columns of pixels on the right to ignore'
        display: boolean - display images of the selected top sections
        '''
        self.df['pix_intensity'] = np.nan
        filelist = glob.glob(address + "/*.png")
        for filename in filelist:
            image = io.imread(filename)[:cutoff, left_margin:-right_margin]
            slice_index = int(filename[len(address)+1:len(address)+6])
            self.df.pix_intensity[slice_index] = image.mean()
            if display:
                self.display_image(image)

    def display_image(self, image):
        '''displays black and white image

        Parameter: image as ndarray of pixel intensities
        '''
        plt.imshow(image,cmap = cm.Greys_r)
        plt.show()



