import argparse
from datetime import datetime, timedelta
import json

import bokeh.plotting as bkh
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from pandas.io.json import json_normalize

parser = argparse.ArgumentParser(description='Plot call duration per day. First run parse_data.py to generate the json file.')
parser.add_argument('-f', '--file', dest='file', help='Name of the generated file')
parser.add_argument('--frequency', dest='frequency', default='D', help='Group data by H, D, W, M or A')
args = parser.parse_args()

if args.file is None:
	parser.print_help() 
	exit(0)

data = pd.read_json(args.file, encoding='UTF-8')
data = json_normalize(data["calls"])

df_calls = data[['date', 'duration']]
df_calls['date'] = pd.to_datetime(df_calls['date']) # convert date to datetime obj
df_calls['duration'] = df_calls['duration'].apply(pd.Timedelta)
df_calls.set_index('date', inplace=True)
df_calls = df_calls.resample(args.frequency).sum() # group by day and sum values per day (sum of 1's in each column)
df_calls.reset_index(inplace=True)

colors = ['#686de0', '#ffbe76']

if args.frequency in ['H', 'D']:
	fig = bkh.figure(x_axis_type='datetime', y_axis_type='datetime', title="Call duration per day", width=1200, height=480)
	fig.vbar(x='date', top='duration', width=timedelta(days=0.6),source=df_calls, color=colors[0])
else:
	fig = bkh.figure(x_axis_type='datetime', y_axis_type='datetime', title="Call duration over time", width=1200, height=480)
	fig.vbar(x='date', top='duration', width=timedelta(days=7), source=df_calls, color=colors[0])

fig.xaxis.axis_label = 'Date'
fig.yaxis.axis_label = 'Call duration'
bkh.show(fig)