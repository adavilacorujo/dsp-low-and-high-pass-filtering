# Creator: Andres G.M. Davila Corujo
# Association: Polytechnic University of Puerto Rico 
# Description: Python interpretation of a high pass and low pass image filtering.
#   Used to either remove high frequencies or a low frequencies to blur or sharpen images, respectively.

import numpy as np 
# import numba 
import os
import math 

# from numba import jit
from PIL import Image


class Filtering():
    #-----------------------------------------------
    # __init__: Entry point of class
    #-----------------------------------------------
    def __init__(self, fname, _filter, low_high='high', directory=False):
        self._filter = _filter
        self.data_array = list()
        self.names = list()

        # Assert file exists
        if os.path.isfile(fname):
            self.data = Image.open(fname, mode='r')
            self.names.append(fname)

        # If filename provided is a directory
        elif os.path.isdir(fname):
            files = 0
            # Iterate and search for images
            for filename in os.listdir(fname):
                if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
                    self.data_array.append(np.asarray(Image.open(fname + filename, mode='r')).copy())
                    self.names.append(filename)
                    files += 1
            print(f'{files} images to be processed')
            
        else:
            print(f'\nFileNotFound: No file named \'{fname}\' found')
            exit()
        
        self.low_high = low_high

        # Dictionary to get middle of matrix easily
        self.center = dict()
        for key, idx in zip(list(range(1, 99, 2)), list(range(0, 50))):
            self.center[key] = idx
        
        self.convert(directory)

    #-----------------------------------------------
    # convert: get image pixels and assert filter is according
    #-----------------------------------------------
    def convert(self,directory):
        if not(directory):
            self.data = np.asarray(self.data).copy()
        else:
            self.data = self.data_array
        
        # Assert filter is according, provided filter is a symmetric filter 
        try:
            if self.low_high == 'low':
                assert(self._filter[0][0] == (1/(self._filter.shape[0])**2))
            else:
                assert(self._filter[0][0] == (-1/(self._filter.shape[0])**2))
        except:
            print("Verify filter")
            exit()

    #-----------------------------------------------
    # process: function to apply mask, or kernel, to the image
    #-----------------------------------------------
    def process(self, v, data):
        sumatoria = 0.0     # Sum of each matrix following the operation
                                # filter*data
        row = col = 0       # Row and column indexes to get pixel from image
        lim_row = self._filter.shape[0] # Set limit to iterate over for each pass
        lim_col = self._filter.shape[1] # Set limit to iterate over for each pass
        averages = dict()   # Average of each square matrix after operation 
                            # sum(filter*data)
        while True:
            # Variables to get each element from filter
            k, m = 0, 0
            for i in range(row, lim_row):
                m = 0
                for j in range(col, lim_col):
                    # Perform operation for each pixel with each according element of the 
                    # filter
                    sumatoria += (self._filter[k, m]*data[i, j])
                    m += 1
                k += 1

            # Save sum and center of matrix 
            averages[(lim_row - self.center[self._filter.shape[1]] - 1, lim_col - self.center[self._filter.shape[1]] - 1)] = sumatoria
            # data[(lim_row - self.center[self._filter.shape[1]] - 1, lim_col - self.center[self._filter.shape[1]] - 1)] = sumatoria
            # Move filter matrix to the right each iteration
            col += 1    
            lim_col += 1

            # Reset colums and start at second row
            if lim_col > data.shape[1]:
                row += 1 
                lim_row += 1
                col = 0 
                lim_col = self._filter.shape[1]

            # If row limit arrives at the final row of image, break loop
            if lim_row > data.shape[0]:
                break

            # print(sumatoria)
            sumatoria = 0

        # Set according pixel with sum/average of its surrounding pixels
        for j in averages.items():
            data[j[0]] = j[1]

        return data

    #-----------------------------------------------
    # filter: function to filter image according to filter given
    #-----------------------------------------------
    def filter(self):   
        # Flip the matrix 180
        self._filter = self.flip_180() 
        
        # Cast to a list, allowing for easier iteration
        if 'list' not in str(type(self.data)):
            self.data = [self.data]

        # Iterate and filter each image
        for v, data in enumerate(np.array(self.data)):
            print(f'Filtering image #{v+1}: {self.names[v]}...')

            # Pad data
            # data = self.padding(data)
            
            # If image has more than one channel, i.e. it is not greyscale,
            # apply 2D filter to each channel independently. Behavior
            # imitated from MATLABs imfilter() function.
            if len(data.shape) == 3:
                print("\tDimensions: ", data.shape[2])

                for d in range(data.shape[2]):
                    print(f'\tFiltering on dimension {d+1}')

                    temp_data = data[:, :, d]
                    temp_data = self.process(v, temp_data) 

                    # Cast image to unsigned int with 8 bits, 0 - 255
                    self.data[v][:, :, d] = np.uint8(temp_data)

            # Image is greyscale and only has one channel
            else:    
                self.data[v] = np.uint8(self.process(v, data))
        
        return self.data

    #-----------------------------------------------
    # padding: Used to add zeros in the image's outer 
    # edges allowing the mask to be applied to each 
    # pixel
    #-----------------------------------------------
    def padding(self, data):
        frows = math.floor(self._filter.shape[0] / 2)
        fcols = math.floor(self._filter.shape[1] / 2)

        if len(data.shape) > 2:
            matrix = np.zeros(shape=(data.shape[0] + frows*2, data.shape[1] + fcols*2, data.shape[2]))
            matrix[ frows  : data.shape[0] + frows, fcols : data.shape[1] + fcols, :] = data
        else:
            matrix = np.zeros(shape=(data.shape[0] + frows*2, data.shape[1] + fcols*2))
            matrix[ frows  : data.shape[0] + frows, fcols : data.shape[1] + fcols] = data
        return matrix

    #-----------------------------------------------
    # flip_180: returns a new filter flipped 180 to perform 
    # linear convolution
    #-----------------------------------------------
    def flip_180(self):
        matrix = np.ones(shape=self._filter.shape)
        i = 0
        for row in reversed(range(self._filter.shape[0])):
            matrix[i, :] = list(reversed(self._filter[row, :]))
            i += 1

        return matrix
                
#-----------------------------------------------
# Script to test the Filtering class
#-----------------------------------------------
if __name__=='__main__':
    import matplotlib.pyplot as plt 
    import pandas as pd

    original = Image.open("./../IMAGES/brainMRI_1.jpg", mode='r')

    # Define high pass filter
    high_pass_filter = np.ones((9,9))*(-1/81)
    high_pass_filter[4, 4] = 2
    high_pass_filter1 = np.ones((3,3))/-9
    high_pass_filter1[1,1] = 2
    high_pass_filter2 = np.ones((5,5))/-25
    high_pass_filter2[2,2] = 2
    high_pass_filter3 = np.ones((7,7))/-49
    high_pass_filter3[3,3] = 2
    high_pass_filter4 = np.ones((25,25))/-625
    high_pass_filter4[12,12] = 2
    high_filters = [high_pass_filter1,high_pass_filter2,high_pass_filter3,high_pass_filter , high_pass_filter4]

    # Define low pass filter
    low_pass_filter = np.ones((3,3))*(1/9)
    low_pass_filter1 = np.ones((5,5))/25
    low_pass_filter2 = np.ones((7,7))/49
    low_pass_filter3 = np.ones((9,9))/81
    low_pass_filter5 = np.ones((25,25))/625
    filters = [low_pass_filter, low_pass_filter1, low_pass_filter2, low_pass_filter3, low_pass_filter5]

    # Perform filtering
    for fltr in high_filters:
        print(fltr.shape)
        filtering = Filtering("./../IMAGES/ankle_1.jpg", fltr, low_high='high', directory=False)
        img = filtering.filter()
        plt.gray()

        # Show each filtered image
        for image in img:
            print(image.shape)
            plt.imshow(image, label='Filtered')
            plt.title("Filtered")

        # plt.legend()
        plt.show()



