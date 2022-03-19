# btc_interval_check

## This project is an attempt to answer the following questions:

### How often does the Bitcoin network see two consecutive blocks mined more than 2 hours apart from each other? We'd like to know your answer (it doesn't have to be precise) and your approach towards this solution using probability and statistics.

Assuming that the block creation rate is 10 minutes on average, and also assuming that the network instantly agrees on blocks, the distribution I would use to model this is the exponential distribution. Per wikipedia "exponential distribution is the probability distribution of the time between events in a Poisson point process, i.e., a process in which events occur continuously and independently at a constant average rate".  

In btc_interval_simulation.py, I used np.random.default_rng().exponential() to generate random values using the exponential distribution.

When I graph the exponential distribution vs. the real data, sorted by elapsed block creation time, the graphs agree quite well except for some outliers.
![Histogram Comparison - Log ScaleImage](./btc_expn_dist_hist_comp_log.png?raw=true)


For 50 runs of the simulation, I get an average of 4.68 block creation gaps of more than 2 hours.
Avg. 2+ hour gaps:4.68
Chance: 1:155277
Pct: 0.00064401%

_This simulation doesn't account for the network having machines with different local system times._



### How many times has the above happened so far in the history of Bitcoin?

In order to answer the second question, I thought I would try to find out what public data was available about bitcoin.  There are a number of rest apis that provide info about blocks and their solve time.  If I had approx 300GB available, I suppose I could have downloaded the blockchain data itself.

So I set about seeing if I could get the data from the API available at blockstream.info.

I was able to extract the heigh, hash, and timestamp of the blocks, so I wrote a python script to do this (btc_interval_check.py).  I have commented out the portion of the code that I used to extract the data from the api, so that I could run subsequent steps without re-extracting the data, which took about 3 hours to run using 24 processes.

I found that there have been 151 times that consecutive blocks were created more than 2 hours apart.

I think the discrepancy here between the 151 times vs. the 4.68 times expected from the simulation is due to the variation of system times in the network.
