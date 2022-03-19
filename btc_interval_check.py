#!/usr/bin/env python

import requests
import time
import csv
from multiprocessing import Pool

import backoff
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")


API_URL = "https://blockstream.info/api"


def backoff_hdlr(details):
    print(
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "calling function {target} with args {args} and kwargs "
        "{kwargs}".format(**details)
    )


@backoff.on_exception(
    backoff.expo, requests.exceptions.RequestException, on_backoff=backoff_hdlr
)
def req_get_wrapper(url, content_type="text/plain"):
    _ = requests.get(url)
    _.raise_for_status()
    assert (
        _.headers.get("content-type") == content_type
    ), f"Content-type not recognized:{_.headers.get('content-type')}"
    if content_type == "text/plain":
        return _.text
    elif content_type == "application/json":
        return _.json()


def get_and_write_csv(csv_file):
    """
    Query the api and write the data to csv
    Returns True 
    """
    # determine max height of the blockchain
    max_height = int(req_get_wrapper(f"{API_URL}/blocks/tip/height"))
    print(max_height)
    pctl = int(max_height / 100)

    print("Progress:")
    first = True
    prev_block_time = 0
    records = list()
    heights_iter = range(1, max_height)

    results = list()
    with Pool(24) as p:
        results = p.map(get_block_info, heights_iter)

    df = pd.DataFrame(
        results, columns=["height", "block_hash", "block_time"]
    ).set_index("height")
    df.to_csv(csv_file)
    return True


def get_block_info(height):
    if height % 1000 == 0:
        print(f"{height}", flush=True)

    # get the hash val for each height
    block_hash = req_get_wrapper(f"{API_URL}/block-height/{height}")

    # get the details of each block
    block_details_json = req_get_wrapper(
        f"{API_URL}/block/{block_hash}", content_type="application/json"
    )
    block_time = block_details_json["timestamp"]

    # block time seems to given in seconds since EPOCH
    block_info_record = [height, block_hash, block_time]
    return block_info_record


if __name__ == "__main__":
    # takes approx 3hr to run with 24 processes
    # get_and_write_csv("btc_times.csv")
    # ensure results sorted by block_height (even though map will keep the results in sorted order)
    df = pd.read_csv("btc_times.csv").set_index("height").sort_index()

    # calculate elapsed time since previous block, in hours
    df["interval"] = df["block_time"].diff().div(60)
    fig = df.loc[:, "interval"].hist(bins=50).get_figure()
    fig.savefig("btc_block_intervals_hist.png")

    df_2hr = df.loc[df["interval"] > 120]
    df_2hr.to_csv("btc_2hr_gaps.csv")

    print(len(df.query("interval < 0")))
    figb = df.loc[:, "interval"].plot(kind="hist", bins=50, logy=True).get_figure()
    figb.savefig("btc_block_intervals_log_hist.png")

    df_2hr = pd.read_csv("btc_2hr_gaps.csv")
    print(
        f"Number of blocks that were solved more than 2 hours after the previous:{len(df_2hr)}"
    )
    fig2 = (
        df_2hr.sort_values("interval", ascending=False)
        .head(10)
        .plot(
            x="height",
            y="interval",
            kind="bar",
            xlabel="block_height",
            ylabel="time(hrs)",
        )
        .get_figure()
    )
    fig2.savefig("btc_2hr_gaps.png")
