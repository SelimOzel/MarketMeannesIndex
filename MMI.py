import random
import statistics
import math
import plotly

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

# Plots time series and prints MMI
def MMI_Analyze(timeSeries_IN, logName_IN):
	print("MMI "+logName_IN+": ", end=" ")
	mmi = MMI(timeSeries_IN)
	print(mmi)
	fig = plotly.graph_objs.Figure()
	fig.add_trace(plotly.graph_objs.Scatter(y=timeSeries_IN,
	                    mode='lines+markers',
	                    name='lines+markers', text="MMI is "+str(mmi)+"% for "+logName_IN))
	plotly.offline.plot(fig, filename = logName_IN+".html", validate = False )


def main():
	l = 200 			# Sample size
	random.seed(1)		# Fix samples

	# Gaussian, mean 0, variance 0.25
	seriesGaussian = [random.gauss(0.0, 0.25) for i in range(l)]
	MMI_Analyze(seriesGaussian, 'gaussian')
	MMI_Analyze(sorted(seriesGaussian), 'sortedgaussian')

	# Pure full cycle sin
	seriesSin = [math.sin((i/l)*2.0*math.pi ) for i in range(l)]
	MMI_Analyze(seriesSin, 'sin')

	# Noisy full cycle sin
	seriesNoisySin = [seriesGaussian[i]+seriesSin[i] for i in range(l)]
	MMI_Analyze(seriesNoisySin, 'noisysin')	

	# Pure exponential - 0.01% growth for 10 cycles and normalized by 8000
	seriesExp = [math.exp(1.0001*i)/8000 for i in range(10)]
	MMI_Analyze(seriesExp, 'exp')

	# Noisy exponential - 0.01% growth for 10 cycles and normalized by 8000
	seriesNoisyExp = [seriesGaussian[i]+seriesExp[i] for i in range(10)]
	MMI_Analyze(seriesNoisyExp, 'noisyexp')		

if __name__ == "__main__":
    main()
