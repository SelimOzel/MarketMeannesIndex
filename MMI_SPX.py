import random
import statistics
import math
import csv
import collections

import plotly 		# Need to install this one with pip

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
	if(l == 1): 			# To avoid division by zero
		return 100*(th+td)
	return 100*(th+td)/(l-1)

# MMI with moving window
def MMI_Moving(timeSeries_IN, period_IN):
	queue = collections.deque()
	mmiResult = []
	for i in timeSeries_IN:
		price = float(i.replace(',',''))

		queue.append(price)
		if(len(queue)>period_IN):
			queue.popleft()
		mmiResult.append(MMI(queue))
	return mmiResult

# Obtain data for each year including 2006 and 2020 and everything between
# Example: 	priceData = ParseByYear("spx_historical.csv")
#			print(priceData[0]["2019"])
#			print(priceData[1]["2019"])
def ParseByYear(csvName_IN):
	priceDict 	= {}
	dateDict 	= {}

	with open("spx_historical.csv", newline="") as csvfile:
		reader = csv.DictReader(csvfile)

		currentYear = 0
		priceList  	= []
		dateList 	= []
		for row in reader:
			date 	= row['\ufeff"Date"'] 
			price 	= row['Price']
			year 	= date[8:12]

			if(currentYear != year):
				currentYear = year
				priceDict[str(int(year)+1)] = [i for i in reversed(priceList)]
				dateDict[str(int(year)+1)] 	= [i for i in reversed(dateList)]
				priceList 					= []
				dateList 					= []

			priceList.append(price)
			dateList.append(date)

	return [dateDict, priceDict]


# Subplot: Price on top, MMI on bottom.
def Plot_MMI_Price(priceData_IN, mmi_IN, year_IN):
	fig = plotly.tools.make_subplots(rows=2, cols=1)

	fig.add_trace(
	    plotly.graph_objs.Scatter(x=priceData_IN[0], y=priceData_IN[1], name="Price"),
	    row=1, col=1
	)

	fig.add_trace(
	    plotly.graph_objs.Scatter(x=priceData_IN[0], y=mmi_IN, name="MMI"),
	    row=2, col=1
	)
	plotly.offline.plot(fig, filename = year_IN+".html", validate = False )


def main():
	priceData = ParseByYear("spx_historical.csv")

	for year in priceData[0]:
		preiceMMI = MMI_Moving(priceData[1][year], 30)

		Plot_MMI_Price([priceData[0][year], 
						priceData[1][year]],
						preiceMMI, 
						year)

if __name__ == "__main__":
    main()
