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

# some Nobel prizes are shared - create a new column converting prize_share (string) to percentage
def prize_share_pct(share):
    numerator = int(share.split('/')[0])
    denominator = int(share.split('/')[1])
    return numerator / denominator

df_data['share_pct'] = df_data['prize_share'].apply(prize_share_pct)

# create donut chart showing how many prizes went to men compared to how many prizes went to women
fig = px.pie(df_data[df_data['sex'].notna()],
       names='sex',
       title="Percentage of Male vs. Female Laureates",
       hole=0.4,)

fig.show()

# find details about the first 3 female Nobel laureates
df_data[df_data.sex == 'Female'].sort_values('year', ascending=True)[:3]

# find laureates who won the Nobel Prize mutliple times
multiple_winners = df_data[df_data.duplicated(subset=['full_name'], keep=False)]
multiple_winners['full_name'].unique()

# create a bar chart with the number of prizes awarded by category
cat_hist = px.histogram(df_data,x='category',color='category',title='Number of Prizes Awarded per Category')
cat_hist.update_xaxes(categoryorder='total descending')
cat_hist.show()

# create a bar chart that shows the split between men and women by category
cat_hist = px.histogram(df_data,x='category',color='sex',title='Number of Prizes Awarded per Category')
cat_hist.update_xaxes(categoryorder='total descending')
cat_hist.show()

# create a scatter plot and 5-year rolling average of number of prizes awarded every year.
prize_per_year = df_data.groupby(by='year').count()['prize']
moving_average = prize_per_year.rolling(window=5).mean()

plt.figure(figsize=(12,6), dpi=200)
plt.title('Number of Nobel Prizes Awarded per Year')
plt.xticks(ticks=np.arange(1900, 2021, step=5), rotation=45)

ax = plt.gca() 
ax.set_xlim(1900, 2020)

ax.scatter(x=prize_per_year.index,y=prize_per_year.values,c='dodgerblue',alpha=0.5)
ax.plot(moving_average.index, moving_average.values,c='crimson',linewidth=3)

plt.show()

# create a horizontal bar chart showing the number of prizes won by each country
top_countries = df_data.groupby(['birth_country_current'], as_index=False).agg({'prize': pd.Series.count})
top_countries.sort_values(by='prize', inplace=True)
top20_countries = top_countries[-20:]

h_bar = px.bar(x=top20_countries['prize'],
               y=top20_countries['birth_country_current'],
               orientation='h',
               color=top20_countries['prize'],
               color_continuous_scale='Viridis',
               title='Top 20 Countries by Number of Prizes')
 
h_bar.update_layout(xaxis_title='Number of Prizes',yaxis_title='Country',coloraxis_showscale=False)
h_bar.show()

# create a Choropleth Map to show the number of prizes Won by country
df_countries = df_data.groupby(['birth_country_current', 'ISO'], as_index=False).agg({'prize': pd.Series.count})
df_countries.sort_values('prize', ascending=False)

world_map = px.choropleth(df_countries,
                          locations='ISO',
                          color='prize', 
                          hover_name='birth_country_current', 
                          color_continuous_scale=px.colors.sequential.matter)
 
world_map.update_layout(coloraxis_showscale=True,)
 
world_map.show()

# create a horizontal bar chart showing in which categories are the different countries winning prizes
cat_country = df_data.groupby(['birth_country_current', 'category'], as_index=False).agg({'prize': pd.Series.count})
cat_country.sort_values(by='prize', ascending=False, inplace=True)

merged_df = pd.merge(cat_country, top20_countries, on='birth_country_current')
merged_df.columns = ['birth_country_current', 'category', 'cat_prize', 'total_prize'] 
merged_df.sort_values(by='total_prize', inplace=True)

cat_cntry_bar = px.bar(x=merged_df['cat_prize'],
                       y=merged_df['birth_country_current'],
                       color=merged_df['category'],
                       orientation='h',
                       title='Top 20 Countries by Number of Prizes and Category')
 
cat_cntry_bar.update_layout(xaxis_title='Number of Prizes', yaxis_title='Country')
cat_cntry_bar.show()

# create a line chart showing number of prizes won by each country over time
prize_by_year = df_data.groupby(by=['birth_country_current', 'year'], as_index=False).count()
prize_by_year = prize_by_year.sort_values('year')[['year', 'birth_country_current', 'prize']]

cumulative_prizes = prize_by_year.groupby(by=['birth_country_current', 'year']).sum().groupby(level=[0]).cumsum()
cumulative_prizes.reset_index(inplace=True) 

l_chart = px.line(cumulative_prizes,
                  x='year', 
                  y='prize',
                  color='birth_country_current',
                  hover_name='birth_country_current')
 
l_chart.update_layout(xaxis_title='Year',yaxis_title='Number of Prizes')
 
l_chart.show()

# vreate a bar chart showing the organisations affiliated with the Nobel laureates
top20_orgs = df_data['organization_name'].value_counts()[:20]
top20_orgs.sort_values(ascending=True, inplace=True)

org_bar = px.bar(x = top20_orgs.values,
                 y = top20_orgs.index,
                 orientation='h',
                 color=top20_orgs.values,
                 color_continuous_scale=px.colors.sequential.haline,
                 title='Top 20 Research Institutions by Number of Prizes')
 
org_bar.update_layout(xaxis_title='Number of Prizes', 
                      yaxis_title='Institution',
                      coloraxis_showscale=False)
org_bar.show()

# create a bar chart showing the top 20 organisation cities of the research institutions associated with a Nobel laureate
top20_org_cities = df_data['organization_city'].value_counts()[:20]
top20_org_cities.sort_values(ascending=True, inplace=True)

city_bar2 = px.bar(x = top20_org_cities.values,
                  y = top20_org_cities.index,
                  orientation='h',
                  color=top20_org_cities.values,
                  color_continuous_scale=px.colors.sequential.Plasma,
                  title='Which Cities Do the Most Research?')
 
city_bar2.update_layout(xaxis_title='Number of Prizes', 
                       yaxis_title='City',
                       coloraxis_showscale=False)
city_bar2.show()

# create a bar chart showing the top 20 birth cities of Nobel laureates
top20_cities = df_data['birth_city'].value_counts()[:20]
top20_cities.sort_values(ascending=True, inplace=True)

city_bar = px.bar(x=top20_cities.values,
                  y=top20_cities.index,
                  orientation='h',
                  color=top20_cities.values,
                  color_continuous_scale=px.colors.sequential.Plasma,
                  title='Where were the Nobel Laureates Born?')
 
city_bar.update_layout(xaxis_title='Number of Prizes', 
                       yaxis_title='City of Birth',
                       coloraxis_showscale=False)
city_bar.show()

# create a sunburst chart combining country, city, and organisation
country_city_org = df_data.groupby(by=['organization_country', 'organization_city', 'organization_name'], 
                                   as_index=False).agg({'prize': pd.Series.count})
 
country_city_org = country_city_org.sort_values('prize', ascending=False)

burst = px.sunburst(country_city_org, 
                    path=['organization_country', 'organization_city', 'organization_name'], 
                    values='prize',
                    title='Where do Discoveries Take Place?',
                   )
 
burst.update_layout(xaxis_title='Number of Prizes', 
                    yaxis_title='City',
                    coloraxis_showscale=False)
 
burst.show()

# create a histogram showing the distribution ofthe laureates' age at time of award
df_data.birth_date = pd.to_datetime(df_data.birth_date)
birth_years = df_data.birth_date.dt.year
df_data['winning_age'] = df_data.year - birth_years

plt.figure(figsize=(8, 4), dpi=200)
sns.histplot(data=df_data,x=df_data.winning_age,bins=30)
plt.xlabel('Age')
plt.title('Distribution of Age on Receipt of Prize')

plt.show()

# create a box plot showing the winning age across categories
plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("whitegrid"):
    sns.boxplot(data=df_data, x='category', y='winning_age')
 
plt.show()

# create a regression plot showing the winning agre acrosse categories
with sns.axes_style('whitegrid'):
    sns.lmplot(data=df_data,
               x='year', 
               y='winning_age',
               row = 'category',
               lowess=True, 
               aspect=2,
               scatter_kws = {'alpha': 0.6},
               line_kws = {'color': 'black'},)
 
plt.show()
