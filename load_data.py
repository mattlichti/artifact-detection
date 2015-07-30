import json
import pandas as pd
import glob
import numpy as np
from skimage import io
from skimage.feature import blob_doh
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
                self.display_image(image, 'rolling detection - slice %s'
                                   % slice_index)

    def bubbles(self, filename, left_margin=500, right_margin=700,
                top_margin=0, bottom_margin=0, display=True):
        '''currently just displays image with detected bubbles highlighted

        If bubble detection was working, qould also add column to dataframe
        with number and locations of bubbles in each slice

        parameters:
        filename of image to run detection on
        margins: on top, bottom, right, left. My laptop runs out of memory
                 when running algorithm on a few million pixels which requires
                 me to run with large margins
        '''
        image = io.imread(filename)[top_margin:-bottom_margin,
                                    left_margin:-right_margin]
        bubble_locs = blob_doh(image, max_sigma=100, min_sigma=50,
                               threshold=.008)
        if display:
            title = 'bubble detection - slice %s' % filename[7:12]
            self.display_image(image, title, circles=bubble_locs)

    def display_image(self, image, title, circles=[]):
        '''
        parameters:
        image: ndarray of pixel intensities
        title: title to display on plot
        circles: list of positions to circle in image in (y, x, radius) format
        '''
        fig, ax = plt.subplots()
        ax.set_title(title)
        ax.imshow(image, cmap=cm.Greys_r)
        for circle in circles:
            y, x, r = circle
            c = plt.Circle((x, y), r, color='red', linewidth=3, fill=False)
            ax.add_patch(c)
        plt.show()
