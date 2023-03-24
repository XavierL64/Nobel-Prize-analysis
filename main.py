import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# display floats with 2 digits after decimal point
pd.options.display.float_format = '{:,.2f}'.format

# read and explore dataset, check for duplicates and NaN values
df_data = pd.read_csv('nobel_prize_data.csv')

df_data.head()
df_data.info()


