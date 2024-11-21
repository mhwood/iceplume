
import os
import numpy as np
import argparse

def modify_pickup(pickup_file, Nr, rows, cols):

    grid = np.fromfile(pickup_file,'>f8').reshape((8*Nr+3,rows,cols))

    new_grid = np.concatenate([grid[:8*Nr,:,:], np.zeros((Nr,rows,cols)), grid[-3:,:,:]],axis=0)

    output_file_parts = pickup_file.split('.')
    output_file_parts[-3] = output_file_parts[-3].replace('pickup','pickup_with_addmass')
    output_file = '.'.join(output_file_parts)

    new_grid.ravel(order='C').astype('>f8').tofile(output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--pickup_file", action="store",
                        help="Path to the pickup file (ending in .data).", dest="pickup_file",
                        type=str, required=True)

    parser.add_argument("-r", "--rows", action="store",
                        help="The number of rows in the model domain.", dest="rows",
                        type=int, required=True)

    parser.add_argument("-c", "--cols", action="store",
                        help="The number of columns in the model domain.", dest="cols",
                        type=int, required=True)

    parser.add_argument("-k", "--Nr", action="store",
                        help="The number of depth levels in the model domain.", dest="Nr",
                        type=int, required=True)

    args = parser.parse_args()
    pickup_file = args.pickup_file
    rows = args.rows
    cols = args.cols
    Nr = args.Nr

    modify_pickup(pickup_file, Nr, rows, cols)