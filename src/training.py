import argparse
from catboost import CatBoostClassifier, CatBoostRegressor, Pool
import pandas as pd
import numpy as np
from src.utils.utils import *


def train_model(path_to_X, path_to_y, thread_count, type_task):
    """
    :param X:
    :param y:
    :param thread_count: number of thread for training
    :param type_task: maybe one of 'Regression', 'Binary', 'Multiclass'
    :return:
    """
    if type_task == "Regression":
        model = CatBoostRegressor(
            border_count=100,
            depth=7,
            thread_count=thread_count,
            l2_leaf_reg=50,
            iterations=1000,
            learning_rate=0.1,
            loss_function='RMSE'
        )
    elif type_task == "Binary":
        model = CatBoostClassifier(
            border_count=200,
            thread_count=thread_count,
            depth=9,
            l2_leaf_reg=10,
            iterations=10,
            learning_rate=0.2
        )
    elif type_task == "Multiclass":
        model = CatBoostClassifier(
            border_count=200,
            thread_count=thread_count,
            depth=9,
            l2_leaf_reg=10,
            iterations=1000,
            learning_rate=0.2
        )
    else:
        raise RuntimeError("Type target must be one of {\'Regression\', \'Binary\', \'Multiclass\'}")
    X = pd.read_csv(path_to_X)
    y = np.load(path_to_y)
    train_dataset = Pool(X, y)
    model.fit(train_dataset)
    return model


def parse_cmdline():
    parser = argparse.ArgumentParser(description="Build model based on data from preprocessing.py and extract_target.py")
    parser.add_argument("-x", "--dataset", type=str, help="dataset", required=True)
    parser.add_argument("-y", "--target", type=str, help="target for specified dataset", required=True)
    parser.add_argument("-t", "--threads", type=str, help="number of threads", required=False, default=1)
    parser.add_argument("-m", "--ml_task", type=str, help="type of task", required=True,
                        choices=['Regression', 'Binary', 'Multiclass'])
    parser.add_argument("-o", "--output", type=str, help="name of output file with model", required=True)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_cmdline()
    model = train_model(
        path_to_X=get_path_to_common_data(args.dataset),
        path_to_y=get_path_to_targets(args.target),
        thread_count=int(args.threads),
        type_task=args.ml_task
    )
    model_path = get_path_to_models(args.output)
    model.save_model(model_path)
    print(f'Model was computed and saved into {model_path}')

# -x 2R_dataset.csv
# -y 2R_target_50000.npy
# -t 4
# -m Binary
# -o 2R_model_50000_binary.bin
# python -m src.training -x 2R_dataset.csv -y 2R_target_50000.npy -t 4 -m Binary -o 2R_model_50000_binary.bin

