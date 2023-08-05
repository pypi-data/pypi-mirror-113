import pandas as pd
import numpy as np
from feature_engine.selection import DropConstantFeatures
from feature_engine.selection import DropDuplicateFeatures
from feature_engine.selection import DropCorrelatedFeatures, SmartCorrelatedSelection
from mlxtend.feature_selection import SequentialFeatureSelector as SFS

def dropconstant(df, tol=0.998, variables=[]):
    """
    Drop constant features

    _____Parameters_____

    -df: dataframe
        Dataframe to drop the constant features

    -tol: tolerance. Default=0.998
        Tolerance of the constant features

    -variables: list. Optional
        List of features of the dataframe

    _______Return_______

    Dataframe
    """
    if(len(variables)==0):
        sel = DropConstantFeatures(tol=tol, variables=None, missing_values='raise')
        sel.fit(df)
        tmp = sel.transform(df)
        return tmp
    if(len(variables)!=0):
        sel = DropConstantFeatures(tol=tol, variables=variables, missing_values='raise')
        sel.fit(df)
        tmp = sel.transform(df)
        return tmp


def dropduplicated(df, variables=[]):
    """
    Drop duplicated features

    _____Parameters_____

    -df: dataframe
        Dataframe to drop the duplicated features

    -variables: list. Optional
        List of features of the dataframe

    _______Return_______

    Dataframe
    """
    if(len(variables)==0):
        sel = DropDuplicateFeatures(variables=None, missing_values='raise')
        sel.fit(df)
        tmp = sel.transform(df)
        return tmp
    if(len(variables)!=0):
        sel = DropDuplicateFeatures(variables=variables, missing_values='raise')
        sel.fit(df)
        tmp = sel.transform(df)
        return tmp


def dropcorrelated(df, threshold=0.8):
    """
    Drop correlated features

    _____Parameters_____

    -df: dataframe
        Dataframe to drop the correlated features

    -threshold: Default=0.8

    _______Return_______

    Dataframe
    """
    sel = DropCorrelatedFeatures(threshold=threshold, method='pearson', missing_values='raise')
    sel.fit(df)
    tmp = sel.transform(df)
    return tmp



def step_forward(features,target,model,kfeatures, info=False):
    """
    Step forward method

    Display a step forward method to select the best
    features for the model

    _____Parameters_____

    -features: X_train dataset

    -target: y_train dataset

    -model: model

    -kfeatures: number of features

    -info: If True, return a list with the features
        Default=False

    _______Return_______

    List if info is True
    """
    sfs = SFS(model, k_features=kfeatures, forward=True, floating=False, verbose=2, scoring='roc_auc',cv=3)
    sfs = sfs.fit(np.array(features), target)
    if(info):
        selected_feat = features.columns[list(sfs.k_feature_idx_)]
        return selected_feat.to_list()


