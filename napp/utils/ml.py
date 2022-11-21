import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
import catboost as cb


def get_train_test(dataset):
    X_train, X_test, y_train, y_test = train_test_split(
        dataset.drop(["hic-data"], axis=1),
        dataset["hic-data"],
        test_size=0.33, random_state=42
    )
    return X_train, X_test, y_train, y_test


def get_train_test_pool(X_train, X_test, y_train, y_test):
    return cb.Pool(X_train, y_train), cb.Pool(X_test, y_test)


def tune_regression_model(model, train_dataset):
    grid = {'depth': [6, 4, 5, 7, 8, 9, 10],
            'iterations': [100],
            'learning_rate': [0.01, 0.05, 0.1, 0.2, 0.3],
            'l2_leaf_reg': [3, 1, 5, 10, 50, 100],
            'border_count': [32, 5, 10, 20, 50, 100, 200],
            'thread_count': [4]}
    model.randomized_search(grid, train_dataset, n_iter=20, plot=True, verbose=False)


def tune_classification_model(model, train_dataset):
    grid = {'depth': [6, 4, 5, 7, 8, 9, 10],
            'iterations': [100],
            'learning_rate': [0.1, 0.2, 0.3],
            'l2_leaf_reg': [3, 1, 5, 10, 50, 100],
            'border_count': [32, 5, 10, 20, 50, 100, 200],
            'thread_count': [4]}
    return model.randomized_search(grid, X=train_dataset, n_iter=20, plot=True, verbose=False)


def print_regression_testing_performance(y_pred, y_test):
    rmse = (np.sqrt(mean_squared_error(y_test, y_pred)))
    r2 = r2_score(y_test, y_pred)
    print("Testing performance")
    print('RMSE: {:.2f}'.format(rmse))
    print('R2: {:.2f}'.format(r2))


def print_classification_testing_performance(y_test, y_pred):
    print("Testing performance")
    print('Accuracy: {:.2f}'.format(accuracy_score(y_test, y_pred)))
    print('Precision: {:.2f}'.format(precision_score(y_test, y_pred)))
    print('Recall: {:.2f}'.format(recall_score(y_test, y_pred)))
    print('F1-score: {:.2f}'.format(f1_score(y_test, y_pred)))


def search_optimized_parameters(model, train_dataset, tune_function=tune_classification_model):
    """
    Search oprimized parameters
    :param model: model for tuning
    :param train_dataset:
    :param tune_function: maybe tune_classification_model, tune_regression_model or smth else
    :return: optimized parameters
    """
    return tune_function(model, train_dataset)['params']


BOUND_1 = 10
BOUND_2 = 23
BOUND_3 = 100


def assign_class(num):
    if num < BOUND_1:
        return 0
    elif num < BOUND_2:
        return 1
    elif num < BOUND_3:
        return 2
    return 3


def print_multiclassification_testing_performance(y_test, y_pred, average):
    labels = [0, 1, 2, 3]
    print("Testing performance")
    print('Accuracy: {:.2f}'.format(accuracy_score(y_test, y_pred)))
    print(f'Precision: {precision_score(y_test, y_pred, labels=labels, average=average)}')
    print(f'Recall: {recall_score(y_test, y_pred, labels=labels, average=average)}')
    print(f'F1-score: {f1_score(y_test, y_pred, labels=labels, average=average)}')