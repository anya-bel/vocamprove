from math import sqrt
import numpy as np
import pandas as pd

file = "survey_results.csv"


def score_table(path):
    df = pd.read_csv(path)
    df = df.T
    df = df.reset_index(drop=True)
    df = df.drop(0)

    df = df.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna()

    df = df.reset_index(drop=True)

    q_weight = [0.5, 0.5, 0.2, 0.2, 0.2, 0.2, 0.2, 0.25, 0.25, 0.25, 0.25, 1, 0.5, 0.5, 1, 1, 1, 1, 0.25, 0.25, 0.25,
                0.25, 1]
    factor = [1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 5, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    f_weight = [1 for i in range(len(q_weight))]
    dimension = [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3]

    df['avg'] = df.mean(numeric_only=True, axis=1) * 20
    df['q_weight'] = q_weight
    df['factor'] = factor
    df['f_weight'] = f_weight
    df['dimension'] = dimension
    header = list(df)
    print(df)
    return df


def get_factor_score(df):
    factor_score = []
    prod = df.avg * df.q_weight
    for i in set(df.factor):
        index = df.factor == i
        divid = np.sum(prod[index])
        divis = np.sum(df.q_weight[index])
        factor_score.append(divid / divis)
    return np.array(factor_score)

def get_factor_weight(df):
    current_factor = int(df.factor[0])
    indexes = [0]
    for i in range(len(df.factor)):
        if df.factor[i] != current_factor:
            indexes.append(i)
        current_factor=df.factor[i]
    return np.array(df.f_weight[indexes])

def get_dim_score(df, factor_scores):
    dim_score = []
    prod = get_factor_weight(df) * factor_scores

    current_dim =  df.dimension[0]
    indexes = [0]
    for i in range(len(set(df.dimension))):
        if df.dimension[i] != current_dim:
            indexes.append(i)
        current_dim=df.dimension[i]

    dim_score.append(prod[indexes])
    return np.array(dim_score)


def get_human_evaluation_score(df):
    factor_scores = get_factor_score(df)
    dim_scores = get_dim_score(df, factor_scores)
    D = np.sqrt(np.sum(1 - (dim_scores / 100)))
    n = len(set(df.dimension))
    q = (1-(D/np.sqrt(n)))
    return q


if __name__ == "__main__":
    df = score_table(file)
    print(get_human_evaluation_score(df))

