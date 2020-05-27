""" This module includes functions to load and fetch our in-house datasets. """

from keras import backend as K
from prep import constants
import scipy.io as sio
import numpy as np
import pathlib

def get_image_data_format():
    """ Return default data format convention.

    # Aruguments:

    None

    # Return:

    A string, either 'channels_first' or 'channels_last'.
    It specifics which data format convention Keras will follow. (keras.backend.image_data_format() returns it)
    """

    # Return image data format
    return K.image_data_format()

def load_input_data(num_of_cells, num_of_CUEs, num_of_D2Ds, num_of_samples, image_data_format):
    """ Return input data (channel gain matrix) in numpy array.

    # Aruguments:

    num_of_cells: int
        Number of the cells in the cellular system.
    num_of_CUEs: int
        Number of the CUEs in each cell.
    num_of_D2Ds: int
        Number of the D2D pairs in each cell.
    num_of_samples: int or tuple
        Number of the random channel realizations according to the above parameters setting.
    image_data_format: string
        Either 'channels_first' or 'channels_last'.
        It specifics which data format convention Keras will follow. (keras.backend.image_data_format() returns it)

    # Return:

    input_data: 4-D numpy array with shape (batch_size, rows, cols, channels) or (batch_size, channels, rows, cols)
        Input data in given .mat file. Each element in input_data stands for channel gain matrix, 
        which is the 3-D numpy array with shape (channels, rows, cols) if data_format is "channels_first",
        or 3-D numpy array with shape (rows, cols, channels) if data_format is "channels_last".
    """

    # Insert debugging assertions
    assert num_of_cells in constants.cell_range, f"The 'num_of_cells' must be element in {constants.cell_range}."
    assert num_of_CUEs in constants.CUE_range, f"The 'num_of_CUEs' must be element in {constants.CUE_range}."
    assert num_of_D2Ds in constants.D2D_range, f"The 'num_of_D2Ds' must be element in {constants.D2D_range}."

    # Define inner function
    def inner(num_of_samples):

        # Initialization of variables
        batch_size = num_of_samples
        rows = num_of_cells * (num_of_CUEs + num_of_D2Ds)
        cols = 1 + num_of_D2Ds
        channels = num_of_cells

        # Get the filname of the desired .mat file from the directory
        dataset_dir = pathlib.Path.cwd().joinpath('dataset')
        cell_dir = '{} cell'.format(num_of_cells)
        dataset_dir = dataset_dir.joinpath(cell_dir)
        filename = 'data_Cell_{}_CUE_{}_D2D_{}_{}.mat'.format(num_of_cells, num_of_CUEs, num_of_D2Ds, num_of_samples)
        mat_fname = dataset_dir.joinpath(filename)

        # Load the .mat file contents
        mat_content = sio.loadmat(mat_fname)
        input_data = mat_content['input_data']

        # Flatten the 2-D numpy array to 1-D numpy array
        input_data = np.ndarray.flatten(input_data)

        # Each element in the flattened 1-D numpy array is a Python list
        # Convert the numpy array of lists to the numpy array
        if image_data_format == 'channels_first':
            input_data = np.vstack(input_data)
            input_data = np.reshape(input_data, (batch_size, channels, rows, cols))
        elif image_data_format == 'channels_last':
            input_data = np.vstack(input_data)
            input_data = np.reshape(input_data, (batch_size, rows, cols, channels))
        else:
            raise ValueError("'image_data_format' must be 'channels_first' or 'channels_last'.")

        # Return input data
        return input_data

    if type(num_of_samples) is int:    
        return inner(num_of_samples)

    elif type(num_of_samples) is tuple:
        return np.concatenate(list(map(inner, num_of_samples)), axis = 0) 

    else:
        raise TypeError("'num_of_samples' must be integer or tuple.")

def load_target_data(num_of_cells, num_of_CUEs, num_of_D2Ds, num_of_samples):
    """ Return target data (power allocation vector) in numpy array.

    # Arguments:

    num_of_cells: int
        Number of the cells in the cellular system.
    num_of_CUEs: int
        Number of the CUEs in each cell.
    num_of_D2Ds: int
        Number of the D2D pairs in each cell.
    num_of_samples: int or tuple
        Number of the random channel realizations according to the above parameters setting.

    # Return:

    target_data: 2-D numpy array with shape (batch_size, CUE_output_dim + D2D_output_dim)
        Target data in given .mat file. Each element in target_data stands for the power allocation vector, 
        which is the 1-D numpy array with shape (CUE_output_dim + D2D_output_dim, ).
    """

    # Insert debugging assertions
    assert num_of_cells in constants.cell_range, f"The 'num_of_cells' must be element in {constants.cell_range}."
    assert num_of_CUEs in constants.CUE_range, f"The 'num_of_CUEs' must be element in {constants.CUE_range}."
    assert num_of_D2Ds in constants.D2D_range, f"The 'num_of_D2Ds' must be element in {constants.D2D_range}."

    # Define inner function
    def inner(num_of_samples):
        
        # Initialization of variables
        batch_size = num_of_samples
        CUE_output_dim = num_of_CUEs * num_of_cells
        D2D_output_dim = num_of_D2Ds * num_of_CUEs * num_of_cells

        # Get the filname of the desired .mat file from the directory  
        dataset_dir = pathlib.Path.cwd().joinpath('dataset')
        cell_dir = '{} cell'.format(num_of_cells)
        dataset_dir = dataset_dir.joinpath(cell_dir)
        filename = 'data_Cell_{}_CUE_{}_D2D_{}_{}.mat'.format(num_of_cells, num_of_CUEs, num_of_D2Ds, num_of_samples)
        mat_fname = dataset_dir.joinpath(filename)

        # Load the .mat file contents
        mat_content = sio.loadmat(mat_fname)
        target_data = mat_content['target_data']
        optimal_CUE_power = target_data[0]
        optimal_D2D_power = target_data[1]

        # Each element in the numpy array is a Python list
        # Convert the numpy array of lists to the numpy array
        optimal_CUE_power = np.vstack(optimal_CUE_power)
        optimal_CUE_power = np.reshape(optimal_CUE_power, (batch_size, CUE_output_dim))
        optimal_D2D_power = np.vstack(optimal_D2D_power)
        optimal_D2D_power = np.reshape(optimal_D2D_power, (batch_size, D2D_output_dim))

        # Return target data
        target_data = np.hstack((optimal_CUE_power, optimal_D2D_power))
        return target_data

    if type(num_of_samples) is int:
        return inner(num_of_samples)

    elif type(num_of_samples) is tuple:
        return np.concatenate(list(map(inner, num_of_samples)), axis = 0) 

    else:
        raise TypeError("'num_of_samples' must be integer or tuple.")