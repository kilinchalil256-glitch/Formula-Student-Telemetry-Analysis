import pandas as pd

telemetry = pd.read_csv('telemetry.csv')

#print(telemetry.shape)
#print(telemetry.head())
#print(telemetry.columns)
#print(telemetry.dtypes)

nan_count = telemetry.isna().sum()

print(nan_count)

analyzed_data=telemetry.describe().loc[['mean','std','min','max']]
print (analyzed_data)