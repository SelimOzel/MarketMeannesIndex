# Market Meannes Index
Analysis of MMI from Financial Hacker

## A Github Study of Market Meanness Index
This analysis is based on market meanness index (MMI) as explained in Financial Hacker [1].

First, I will apply the index to a randomly generated gaussian series and a full cycle of a sine wave with the same type of gaussian added as noise on top. The hypothesis is that MMI should roughly tell me that 75% of samples in both cases will revert to median. Next, I will apply the same MMI to an exponential growth function with same gaussian noise. I would expect a smaller MMI.

Later on, I will be applying the index over one year periods going back to 2006 based on OHLC obtained from [2].

Finally, I’ll decide if we are any smarter for having done (or read in case of readers) this analysis.

## What is MMI?
According to financial hacker if price change (the difference between P(t) and P(t-1) ) is completely independent of previous members each quarter should have %25 of the values. These quarters are defined as below.

### Four Quarters as Sets
	
> Quarter 1		: (P(t) < M and P(t-1) < M)  
	
> Quarter 2		: (P(t) < M and P(t-1) > M)  
	
> Quarter 3		: (P(t) > M and P(t-1) < M)  
	
> Quarter 4		: (P(t) > M and P(t-1) > M)

The crucial point is that price reversion happens in exactly %75 of the cases. Why is that? To understand that, they create two more sets based on quarters.

### Revert to Median Sets
> Revert Up	: (P(t-1) < M and P(t) > P(t-1)) 	

> Revert Down	: (P(t-1) > M and P(t) < P(t-1))

Following their logic, it is trivial to see Quarter 1 represents only half of the values for “Revert Up” set and all the members of Quarter 3. Therefore 0.5*0.25 + 0.25 = 3/8. Same arithmetic works for “Revert Down” and therefore tells us that 6/8 (75%) of total values are reverting to median in a set that has no trend (i.e. price change is completely independent of previous prices).


——————————————————————————————
### MMI on Gaussian Series
Assume that we have the following time series sampled from a gaussian distribution with mean 0.0 and deviation 1.0:
1.29 1.45 0.07 -0.76 -1.09 

Median is 0.07. P(0) is 1.29, and P(1) is 1.45. Therefore when I select t as 1, P(t) becomes 1.45 and P(t-1) becomes 1.29. So and so forth … Computing this would result in an MMI of %25. Why is that? Because my sample length is too low. As I increase the sample length I can easily see that MMI converges to 75%.

### MMI on Gaussian Series with Sine Wave
Interestingly I observed MMI for pure sine-wave to be 50%. When mixed with Gaussian noise the MMI changed between 50 and 75% depending on the variance of the noise. For example at 0.25 variance MMI of the mix was observed to be 55%. I would say that median value is changing during cycles and not set as zero at the beginning. That might be the explanation for MMI discovering a trend.

[1] https://financial-hacker.com/the-market-meanness-index/#more-250
[2] https://www.investing.com/indices/us-spx-500-historical-data
