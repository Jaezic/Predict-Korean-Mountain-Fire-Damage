import argparse

import pandas as pd
from sklearn.calibration import LabelEncoder
from sklearn.preprocessing import KBinsDiscretizer


def preprocessing(df):
    feature_Engineering(df)

    # Label Encoding
    le = LabelEncoder()
    df['diravg'] = le.fit_transform(df['diravg'])
    df['dirmax'] = le.fit_transform(df['dirmax'])
    df['ocurcause'] = le.fit_transform(df['ocurcause'])

    # Binning (scale_damage)
    discretizer = KBinsDiscretizer(
        n_bins=5, encode='ordinal', strategy='quantile')
    df['scale_damage'] = discretizer.fit_transform(
        df['scale_damage'].values.reshape(-1, 1))
    


def feature_Engineering(df):
    # Ocurcause Handling
    df['ocurcause'] = df['ocurcause'].apply(
        lambda x: x.replace('추정', '') if '추정' in x else x)
    df['ocurcause'] = df['ocurcause'].apply(
        lambda x: '담배' if '담뱃' in x or '담배' in x else x)
    df['ocurcause'] = df['ocurcause'].apply(
        lambda x: '입산자실화' if '입산자' in x or '실화' in x or '발화' in x or '행위' in x or '훈련' in x else x)
    df['ocurcause'] = df['ocurcause'].apply(lambda x: '소각' if '소각' in x else x)
    df['ocurcause'] = df['ocurcause'].apply(lambda x: '방화' if '방화' in x else x)
    df['ocurcause'] = df['ocurcause'].apply(lambda x: '미상' if '미상' in x else x)
    df['ocurcause'] = df['ocurcause'].apply(lambda x: '화재' if '화재' in x else x)
    df['ocurcause'] = df['ocurcause'].apply(
        lambda x: '불장난' if '장난' in x else x)
    cnt = df['ocurcause'].value_counts()
    df['ocurcause'] = df['ocurcause'].apply(
        lambda x: '기타' if cnt[x] < 37 else x)
