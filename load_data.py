import json
import pandas as pd
import glob
import numpy as np
from skimage import io


class LoadData(object):
    '''load metadata and bubble and rolling labels into dataframe'''

    def __init__(self):
        # list of properties from metadata used in analysis
        self.prop_list = ['stage_x_current', 'stage_x_position',
                          'stage_y_current', 'stage_y_position',
                          'stage_z_current', 'stage_z_position',
                          'aux_flow_level', 'aux_temp', "slice_queue",
                          'camera_lineFeedback', 'camera_temp']
        self.df = pd.DataFrame()  # dataframe of information about slices

    def load_metadata(self, filename):
        '''loads metadata as pandas dataframe'''
        f = open(filename)
        self.df = pd.DataFrame(json.loads(f.read()))
        self.df.set_index('sliceIndex', inplace=True)
        self.df = self.df[['time', 'properties']]
        self.df.time = pd.to_datetime(self.df.time, unit='ms')
        for prop in self.prop_list:
            self.df[prop] = self.df.properties.map(lambda x: x[prop])
        self.df.drop('properties', inplace=True, axis=1)

    def label_bubbles(self, bubbles={}):
        '''adds column to dataframe with number of bubbles on each image

        Input dictionary containing number of bubbles as the keys and lists of
        slice indices with that number of bubbles as the values.
        Slices not in dictionary are set to zero
        '''
        self.df['bubbles'] = 0
        for num_bubbles, slice_list in bubbles.iteritems():
            self.df.bubbles[slice_list] = num_bubbles

    def label_rolling(self, rolling=[]):
        ''' input list with indices of slices with rolling'''
        self.df['rolling'] = 0
        self.df.rolling[rolling] = 1

    def pix_intensity(self, address, cutoff=100, left_margin=500, 
                      right_margin=700):
        '''Create df column of average pixel intensity value of the tops of 
        the images. Images with rolling will be darker at the top.

        Inputs:
        address of the folder containing the images
        cutoff: number of rows of the top of the image
        left_margin: number of columns of pixels on the left to ignore
        right_margin: number of columns of pixels on the right to ignore
        '''
        self.df['pix_intensity'] = np.nan
        filelist = glob.glob(address + "/*.png")
        for file in filelist:
            image = io.imread(file)[:cutoff,left_margin:-right_margin]
            slice_index = int(file[len(address)+1:len(address)+6])
            self.df.pix_intensity[slice_index] = image.mean()

if __name__ == '__main__':
    rolling = [15462, 15502, 15552]
    bubble_dict = {1: [15022, 15042, 15052, 15062, 15092, 15122, 15142, 15152,
                       15202, 15232, 15252, 15332, 15372, 15392, 15432, 15482,
                       15512],
                   2: [15102,  15172, 15182, 15282]}
    data = LoadData()
    data.load_metadata('metadata.json')
    data.label_rolling(rolling)
    data.label_bubbles(bubbles=bubble_dict)
    data.pix_intensity('images')
    print data.df
