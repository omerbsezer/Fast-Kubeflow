import json

import argparse
from pathlib import Path

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

def _download_data(args):

    # Gets data from sklearn library and split dataset
    x, y = load_breast_cancer(return_X_y=True)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    # Creates `data` structure to save 
    data = {'x_train' : x_train.tolist(),
            'y_train' : y_train.tolist(),
            'x_test' : x_test.tolist(),
            'y_test' : y_test.tolist()}

    # Creates a json object based on `data`
    data_json = json.dumps(data)

    # Saves the json object into a file
    with open(args.data, 'w') as output_file:
        json.dump(data_json, output_file)

if __name__ == '__main__':
    
    # This component does not receive any input, it only outputs one artifact which is `data`.
    parser = argparse.ArgumentParser()
    # Output argument: data
    parser.add_argument('--data', type=str)
    
    args = parser.parse_args()
    
    # Creating the directory where the OUTPUT file will be created, (the directory may or may not exist).
    # This will be used for other component's input (e.g. decision tree, logistic regression)
    Path(args.data).parent.mkdir(parents=True, exist_ok=True)

    _download_data(args)
    