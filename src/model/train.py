# Import libraries

import argparse
import glob
import os
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import mlflow

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve

# define functions
def main(args):
    mlflow.autolog()

    # read data
    df = get_csvs_df(args.training_data)

    # split data
    data = split_data(df)

    # train model
    model = train_model(args.reg_rate,
                        data['train']['X_train'],
                        data['test']['X_test'],
                        data['train']['y_train'],
                        data['test']['y_test'])

    # get metrics
    evaluation_model(model, data['test']['X_test'], data['test']['y_test'])


def get_csvs_df(path):
    if not os.path.exists(path):
        raise RuntimeError(f"Cannot use non-existent path provided: {path}")
    csv_files = glob.glob(f"{path}/*.csv")
    if not csv_files:
        raise RuntimeError(f"No CSV files found in provided data path: {path}")
    return pd.concat((pd.read_csv(f) for f in csv_files), sort=False)


# Function to split data
def split_data(df):
    X = df.drop(['Diabetic'], axis=1)
    y = df.pop('Diabetic')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=False)
    data = {
        'train': {'X_train': X_train, 'y_train': y_train},
        'test': {'X_test': X_test, 'y_test': y_test}
    }
    return data
 

def train_model(reg_rate, X_train, X_test, y_train, y_test):
    # train model
    return LogisticRegression(C=1/reg_rate, solver="liblinear").fit(X_train, y_train)


def evaluation_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    # acc = np.average(y_pred == y_test)
    y_scores = model.predict_proba(X_test)
    # auc = roc_auc_score(y_test, y_score=y_scores[:,1])
    # mlflow.log_metrics({'acc': acc, 'auc': auc})
    
    # def plot_auc():
    #     # plot ROC curve
    #     fpr, tpr, thresholds = roc_curve(y_test, y_scores[:,1])
    #     fig = plt.figure(figsize=(6, 4))
    #     # Plot the diagonal 50% line
    #     plt.plot([0, 1], [0, 1], 'k--')
    #     # Plot the FPR and TPR achieved by our model
    #     plt.plot(fpr, tpr)
    #     plt.xlabel('False Positive Rate')
    #     plt.ylabel('True Positive Rate')
    #     plt.title('ROC Curve')
    # plot_auc()

def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--training_data", dest='training_data',
                        type=str,
                        default='experimentation/data/')
    parser.add_argument("--reg_rate", dest='reg_rate',
                        type=float, default=0.001)

    # parse args
    args = parser.parse_args()

    # return args
    return args

# run script
if __name__ == "__main__":
    # add space in logs
    print("\n\n")
    print("*" * 60)

    # parse args
    args = parse_args()

    # run main function
    main(args)

    # add space in logs
    print("*" * 60)
    print("\n\n")
