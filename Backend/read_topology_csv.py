import pandas as pd

def read_topology(file_path):
    df = pd.read_csv(file_path, delimiter=';')
    return df

file_path = r'C:\Users\Piotrek\PycharmProjects\SCHT_ONOS_APP2\resources\NetworkData.csv'
df = read_topology(file_path)
print(df)