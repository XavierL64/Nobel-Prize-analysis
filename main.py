import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# display floats with 2 digits after decimal point
pd.options.display.float_format = '{:,.2f}'.format

# read and explore dataset
df_data = pd.read_csv('nobel_prize_data.csv')
df_data.head()
df_data.info()

# check for duplicates 
df_data.duplicated().values.any() # returns False

# check for NaN values
df_data.isna().values.any() # returns True
df_data.isna().sum() # 28 entries missing data on individual laureates. 255 entries missing data on organisation name.
df_data[df_data['birth_date'].isna()]
df_data.loc[df_data['organization_name'].isna()]

# convert birth_date column to Datetime objects
df_data.birth_date = pd.to_datetime(df_data.birth_date)

# some Nobel prizes are shared - create a new column converting prize_share (string) to percentage
def prize_share_pct(share):
    numerator = int(share.split('/')[0])
    denominator = int(share.split('/')[1])
    return numerator / denominator

df_data['share_pct'] = df_data['prize_share'].apply(prize_share_pct)

# create donut chart showing how many prizes went to men compared to how many prizes went to women
sex_data = df_data['sex'].value_counts()


