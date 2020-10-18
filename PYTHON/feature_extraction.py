import numpy as np
import pandas as pd
import os 

from PIL import Image


class FTE():
    def __init__(self, yes_dir, no_dir, directory=True, image=None):
        if directory == True:
            self.yes = self.get_dir(yes_dir)
            self.no = self.get_dir(no_dir)
        else:
            self.image = np.asarray(Image.open(image, mode='r')).copy()

    


    def create_feature_vectors(self):
        # "Flatten" each picture multiplying pixel by pixel
        yes = [data.reshape(data.shape[0]*data.shape[1]) for data in self.yes]
        no = [data.reshape(data.shape[0]*data.shape[1]) for data in self.no]

        # Assuming all images have the same size
        yes = pd.DataFrame(yes, columns=[f'px{i}' for i in range(len(yes[0]))])


    def get_dir(self, fname):
        data = list()
        if os.path.isdir(fname):
            files = 0
            for filename in os.listdir(fname):
                if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
                    data.append(np.asarray(Image.open(fname + filename, mode='r')).copy())
                    files += 1
        else:
            print(f'No directory named {self.image}')

        return data