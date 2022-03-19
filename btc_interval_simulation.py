#!/usr/bin/env python

import time

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")


if __name__ == "__main__":
    df_actual = pd.read_csv("btc_times.csv").set_index("height").sort_index()
    df_actual["interval"] = df_actual["block_time"].diff().div(60)
    block_height = len(df_actual)
    gaps_2hr = list()
    num_sim = 50
    for i in range(num_sim):
        df_sim = pd.DataFrame(
                {
                    "height":range(1, block_height + 1),
                    "time_est":np.random.default_rng().exponential(scale=10, size=block_height)
                    },
                ).set_index("height")
        num_gaps_2hr = len(df_sim.query("time_est > 120"))

        gaps_2hr.append(num_gaps_2hr)

    total_num_gaps = sum(gaps_2hr)
    avg = total_num_gaps / num_sim
    print(f"Avg. 2+ hour gaps:{avg}")
    print(f"Chance: 1:{block_height/avg:0.0f}")
    print(f"Pct: {100*avg/block_height:0.8f}%")


    df = pd.concat([df_actual, df_sim], axis=1)
    print(df.describe())
    figa = df.loc[:, ["time_est", "interval"]].plot(kind='hist',bins=50, alpha=0.5).get_figure()
    figa.savefig("btc_expn_dist_hist_comp.png")
    figb = df.loc[:, ["time_est", "interval"]].plot(kind='hist',bins=50, logy=True, alpha=0.5).get_figure()
    figb.savefig("btc_expn_dist_hist_comp_log.png")
    



