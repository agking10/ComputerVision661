import math
import numpy as np


def Regionify(img, instrument='drums'):
    def regionsFunc(img_array, regions):
        # Assign intrument regions
        assign = 0
        for region in regions:
            assign += 1
            # Loop over rows to assign
            for i in range(region[0][0], region[1][0]):
                # Loop over cols to assign
                for k in range(region[0][1], region[1][1]):
                    img_array[i][k] = assign
        return img_array

    def scale(xarray, yarray, dimx, dimy):
        scaled_x = np.zeros((len(xarray)))
        scaled_y = np.zeros((len(yarray)))

        # Scale x coordinates and fill in scaled_x array
        index = 0
        for x in xarray:
            scaled_x[index] = int(math.floor((dimx / 1000) * x))
            index += 1

        # Scale y coordinates and fill in scaled_y array
        index = 0
        for y in yarray:
            scaled_y[index] = int(math.floor((dimy / 1000) * y))
            index += 1

        return scaled_x, scaled_y

    # Obtain dimensions of image
    rows, cols = img.shape

    if instrument == 'drums':

        # Determine coords to be scaled, assuming 1000x1000
        velx = 10
        vely = 10
        wanted_x = [333, 666, 1000, velx]
        wanted_y = [666, 1000, vely]

        # Scale the coords
        scaled_x, scaled_y = scale(wanted_x, wanted_y, cols, rows)

        # Define sound reference dictionary
        references = {1: ('drums1.wav', [-scaled_x[-1], -scaled_y[-1]]),
                      2: ('drums2.wav', [-scaled_x[-1], -scaled_y[-1]]),
                      3: ('drums3.wav', [-scaled_x[-1], -scaled_y[-1]])}

        # DEFINE REGIONS
        regions = np.array([[[scaled_y[0], 0], [scaled_y[1], scaled_x[0]]]
                               , [[scaled_y[0], scaled_x[0]], [scaled_y[1], scaled_x[1]]]
                               , [[scaled_y[0], scaled_x[1]], [scaled_y[1], scaled_x[2]]]
                            ]).astype(np.int)

        # Populate instrument regions array
        img_array = np.zeros((rows, cols))
        img_array = regionsFunc(img_array, regions)

    elif instrument == 'xylophone':
        # Determine coords to be scaled, assuming 1000x1000
        velx = 5
        vely = 5
        wanted_x = [200, 400, 600, 800, 1000, velx]
        wanted_y = [666, 1000, vely]

        # Scale the coords
        scaled_x, scaled_y = scale(wanted_x, wanted_y, cols, rows)

        # Define sound reference dictionary
        references = {1: ('xylophone1.wav', [-scaled_x[-1], -scaled_y[-1]]),
                      2: ('xylophone2.wav', [-scaled_x[-1], -scaled_y[-1]]),
                      3: ('xylophone3.wav', [-scaled_x[-1], -scaled_y[-1]]),
                      4: ('xylophone4.wav', [-scaled_x[-1], -scaled_y[-1]]),
                      5: ('xylophone5.wav', [-scaled_x[-1], -scaled_y[-1]])}

        # DEFINE REGIONS
        regions = np.array([[[scaled_y[0], 0], [scaled_y[1], scaled_x[0]]]
                               , [[scaled_y[0], scaled_x[0]], [scaled_y[1], scaled_x[1]]]
                               , [[scaled_y[0], scaled_x[1]], [scaled_y[1], scaled_x[2]]]
                               , [[scaled_y[0], scaled_x[2]], [scaled_y[1], scaled_x[3]]]
                               , [[scaled_y[0], scaled_x[3]], [scaled_y[1], scaled_x[4]]]
                            ]).astype(np.int)

        # Populate instrument regions array
        img_array = np.zeros((rows, cols))
        img_array = regionsFunc(img_array, regions)


    elif instrument == 'snare':

        # Determine coords to be scaled, assuming 1000x1000
        velx = 10
        vely = 10
        wanted_x = [300, 700, velx]
        wanted_y = [500, 800, vely]

        # Scale the coords
        scaled_x, scaled_y = scale(wanted_x, wanted_y, cols, rows)

        # Define sound reference dictionary
        references = {1: ('snare1.wav', [-scaled_x[-1], -scaled_y[-1]])}

        # DEFINE REGIONS
        regions = np.array([[[scaled_y[0], scaled_x[0]], [scaled_y[1], scaled_x[1]]]
                            ]).astype(np.int)

        # Populate instrument regions array
        img_array = np.zeros((rows, cols))
        img_array = regionsFunc(img_array, regions)

    return img_array, references
