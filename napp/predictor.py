import argparse

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier, CatBoostRegressor
from src.utils.ml import *
from src.utils.utils import *


def parse_cmdline():
    parser = argparse.ArgumentParser(description="Prediction hic-data based on dataset from preprocessing.")
    parser.add_argument("-d", "--dataset", type=str, help="dataset", required=True)
    parser.add_argument("-model", type=str, help="model", required=True)
    parser.add_argument("-o", "--output", type=str, help="name of output file with prediction", required=True)
    parser.add_argument("-m", "--ml_task", type=str, help="type of task", required=True,
                        choices=['Regression', 'Binary', 'Multiclass'])
    args = parser.parse_args()
    return args


def predict(name_model, name_dataset, ml_task):
    if ml_task == "Regression":
        model = CatBoostRegressor()
    else:
        model = CatBoostClassifier()

    model.load_model(get_path_to_models(name_model))
    test_dataset = pd.read_csv(get_path_to_common_data(name_dataset))
    return model.predict(test_dataset)


if __name__ == '__main__':
    args = parse_cmdline()
    y_pred = predict(args.model, args.dataset, args.ml_task)
    pred_path = get_path_to_predictions(args.output)
    np.save(pred_path, y_pred)
    print(f'Predictions was computed and saved into {pred_path}')
