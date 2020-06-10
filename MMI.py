import random
import statistics
import math
import plotly

import numpy as np
from scipy.ndimage.interpolation import shift


# Market Meanness Index
def MMI(timeSeries_IN):
	M = statistics.median(timeSeries_IN)
	l = len(timeSeries_IN)
	td = 0
	th = 0
	P_prev = timeSeries_IN[0]
	for t in range(1,l):
		P = timeSeries_IN[t]
		if(P_prev < M and P > P_prev):
			th += 1
		if(P_prev > M and P < P_prev):
			td += 1
		P_prev = P
	return 100*(th+td)/(l-1)

def fastMMI(timeSeries_IN):
	M = statistics.median(timeSeries_IN)
	l = len(timeSeries_IN)
	th = ((timeSeries_IN < M) & (timeSeries_IN > shift(timeSeries_IN, -1, cval=np.NaN))).sum()
	td = ((timeSeries_IN > M) & (timeSeries_IN < shift(timeSeries_IN, -1, cval=np.NaN))).sum()
	# See: https://stackoverflow.com/questions/30399534/shift-elements-in-a-numpy-array
	return 100 * (th + td) / (l - 1)

# Plots time series and prints MMI
def MMI_Analyze(timeSeries_IN, logName_IN):
	print("MMI "+logName_IN+": ", end=" ")
	mmi = fastMMI(timeSeries_IN)
	print(mmi)
	fig = plotly.graph_objs.Figure()
	fig.add_trace(plotly.graph_objs.Scatter(y=timeSeries_IN,
	                    mode='lines+markers',
	                    name='lines+markers', text="MMI is "+str(mmi)+"% for "+logName_IN))
	plotly.offline.plot(fig, filename = logName_IN+".html", validate = False )


def main():
	l = 200 		# Sample size
	np.random.seed(1)		# Fix samples

	# Gaussian, mean 0, variance 0.25
	seriesGaussian = np.random.normal(0.0, 0.25, l)
	# See: https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.normal.html#numpy.random.Generator.normal
	MMI_Analyze(seriesGaussian, 'gaussian')
	MMI_Analyze(sorted(seriesGaussian), 'sortedgaussian')

	# Pure full cycle sin
	seriesSin = np.sin(np.linspace(-np.pi, np.pi, l))
	print(len(seriesSin))
	# https://numpy.org/doc/1.18/reference/generated/numpy.sin.html
	MMI_Analyze(seriesSin, 'sin')

	# Noisy full cycle sin
	seriesNoisySin = seriesGaussian + seriesSin
	MMI_Analyze(seriesNoisySin, 'noisysin')

	# Pure exponential - 0.01% growth for 10 cycles and normalized by 8000
	seriesExp = np.exp(np.linspace(1.0001, 1.0010, 10)) / 8000
	MMI_Analyze(seriesExp, 'exp')

	# Noisy exponential - 0.01% growth for 10 cycles and normalized by 8000
	seriesNoisyExp = seriesGaussian[0:10] + seriesExp[0:10]
	MMI_Analyze(seriesNoisyExp, 'noisyexp')

if __name__ == "__main__":
    main()
