import os
import numpy as np
import pandas as pd
import simplejson as json
import requests
from datetime import datetime
from flask import Flask, request, render_template, redirect
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.palettes import Viridis4 as cp

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/plot_data', methods=['GET', 'POST'])
def plot_data():
	ticker = request.form['ticker']
	columns, x, y = get_data(ticker, '2017-01-01', '2017-12-31')
	plot = get_plot(columns, x, y)

	script, div = components(plot)

	resources = INLINE.render()

	return render_template('plot_data.html', script=script, div=div, resources=resources)

def get_plot(columns, x, y):
	p = figure(x_axis_type='datetime', plot_width=600, plot_height=400)

	p.xaxis.axis_label = 'date'
	p.yaxis.axis_label = 'price'

	palette = cp[0:len(y)]
	for i, yt in enumerate(y):
		p.line(x, yt, line_color=palette[i], legend=columns[i+2])

	return p

def get_data(ticker, start, end):
	url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES?qopts.columns=ticker,date,open,adj_open,close,adj_close&ticker=%s&date.gte=%s&date.lte=%s&api_key=agvvi4s_WEGvpdNA-7Qz'%(ticker, start, end)

	r = requests.get(url)
	json_data = r.text.replace('null', '0')
	data = json.loads(json_data)['datatable']

	columns = [col['name'] for col in data['columns']]
	data_list = data['data']

	df = pd.DataFrame(data_list, columns=columns)

	x = [datetime.strptime(d, '%Y-%m-%d') for d in df['date'].as_matrix()]
	y = df[['open', 'adj_open', 'close', 'adj_close']].as_matrix().T.tolist()

	return columns, x, y

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)

