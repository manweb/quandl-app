import os
import numpy as np
from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/plot_data')
def plot_data():
	plot = get_plot()

	script, div = components(plot)

	resources = INLINE.render()

	return render_template('plot_data.html', script=script, div=div, resources=resources)

def get_plot():
	x = np.arange(1000)
	y = np.random.random(1000)

	p = figure()
	p.line(x, y, line_color='blue')

	return p

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)

