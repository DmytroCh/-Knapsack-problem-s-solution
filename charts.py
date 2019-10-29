import pandas as pd
import plotly.express as px


df = pd.read_csv('p07csv_23-10-2019_185432_t_06_10_100_07_0025.csv')

fig = px.line(df, x = 'nr_pokolenia', y = 'najlepsza_ocena', title='Najlepsza wartość w podziale na pokolenia')
fig1 = px.line(df, x = 'nr_pokolenia', y = 'średnia_ocen', title='Średnia wartość w podziale na pokolenia')

fig.update_yaxes(rangemode='tozero', autorange=True)
fig1.update_yaxes(rangemode='tozero', autorange=True)


fig.show()
fig1.show()





