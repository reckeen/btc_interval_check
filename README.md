# btc_interval_check

- This project is an attempt to answer the following questions:

1. How often does the Bitcoin network see two consecutive blocks mined more than 2 hours apart from each other? We'd like to know your answer (it doesn't have to be precise) and your approach towards this solution using probability and statistics.
1. How many times has the above happened so far in the history of Bitcoin?

The first question is a bit tough to answer.  From what I've read the difficulty level of solving a block is adjusted in order to keep the solve time of a block around 10 minutes.  Given the changing # of miners, and my lack of knowledge of the algorithm, I'm having difficulty coming up with an approach that seems reasonable.  This lead me to focus on the second question.

In order to answer the second question, I thought I would try to find out what public data was available about bitcoin.  There are a number of rest apis that provide info about blocks and their solve time.  If I had approx 300GB available, I suppose I could have downloaded the blockchain data itself.

So I set about seeing if I could get the data from the API available at blockstream.info.

I was able to extract the heigh, hash, and timestamp of the blocks, so I wrote a python script to do this.
I found that there have been 151 times that consecutive blocks were solved more than 2 hours apart.
