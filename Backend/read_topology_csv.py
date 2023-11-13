import pandas as pd

def read_topology(file_path):
    df = pd.read_csv(file_path, delimiter=';')
    return df
