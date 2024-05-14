import pandas as pd
import numpy as np

from collections import Counter
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, 
                            classification_report,
                            recall_score, precision_score, f1_score,
                            confusion_matrix)

from sklearn.ensemble import ExtraTreesClassifier

from prefect import task, flow

def ordinal_encoder(df, feats): 
    for feat in feats:    
        feat_val = list(np.arange(df[feat].nunique()))
        feat_key = list(df[feat].sort_values().unique())
        feat_dict = dict(zip(feat_key, feat_val))
        df[feat] = df[feat].map(feat_dict)
    return df

@task
def load_data():
    df = pd.read_csv("RTA Dataset.csv")
    impute_cols = [x for x in df.isna().sum()[df.isna().sum() != 0].index.tolist()]
    for feat in impute_cols:
        mode = df[feat].mode()[0]
        df[feat].fillna(mode, inplace=True)
    df.drop(columns = ['Vehicle_driver_relation'], inplace=True)
    return df

@task
def encode_data(df):
    df = ordinal_encoder(df, df.drop(['Accident_severity'], axis=1).columns)
    return df

@task
def upsample(df):
    X = df.drop('Accident_severity', axis=1)
    y = df['Accident_severity']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    counter = Counter(y_train)

    for k,v in counter.items():
        per = 100*v/len(y_train)
        # print(f"Class= {k}, n={v} ({per:.2f}%)")

    oversample = SMOTE()
    X_train, y_train = oversample.fit_resample(X_train, y_train)

    counter = Counter(y_train)

    for k,v in counter.items():
        per = 100*v/len(y_train)
        # print(f"Class= {k}, n={v} ({per:.2f}%)")

    y_test = ordinal_encoder(pd.DataFrame(y_test, columns = ['Accident_severity']), pd.DataFrame(y_test, columns = ['Accident_severity']).columns)['Accident_severity']
    y_train = ordinal_encoder(pd.DataFrame(y_train, columns = ['Accident_severity']), pd.DataFrame(y_train, columns = ['Accident_severity']).columns)['Accident_severity']

    return X_train,X_test,y_train,y_test


@task
def model(X_train,X_test,y_train,y_test):
    extree = ExtraTreesClassifier(n_estimators = 400)
    extree.fit(X_train, y_train)
    y_pred = extree.predict(X_test)

    return accuracy_score(y_test, y_pred)


@flow
def workflow():
    df = load_data()
    df2 = encode_data(df)
    X_train,X_test,y_train,y_test = upsample(df2)
    accuracy = model(X_train,X_test,y_train,y_test)
    print('Accuracy',accuracy)


workflow()

# prefect server start
# prefect deployment build main.py:workflow -n deployment -q dev
# prefect deployment apply workflow-deployment.yaml
# prefect agent start -q dev
