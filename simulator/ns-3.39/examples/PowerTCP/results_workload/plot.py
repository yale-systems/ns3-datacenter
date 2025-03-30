#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend so nothing pops up
import matplotlib.pyplot as plt
import numpy as np

def read_qlens(filename):
    """
    Reads lines of the form: "switch 0 qlen 0 time 0.000696"
    Returns a list of queue lengths in KB (assuming 'qlen' is in bytes).
    """
    qlens_kb = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 6:
                # parts[3] should be the qlen value
                try:
                    qlen_bytes = float(parts[3])
                    qlen_kb = qlen_bytes / 1024.0
                    qlens_kb.append(qlen_kb)
                except ValueError:
                    # If there's a parsing error, skip this line
                    continue
    return qlens_kb

def plot_cdf(data, label):
    """
    Plots the empirical CDF of the data on the current figure.
    """
    sorted_data = np.sort(data)
    yvals = np.arange(1, len(sorted_data)+1) / float(len(sorted_data))
    plt.plot(sorted_data, yvals, label=label)

def main():
    # Input files and labels
    filenames = [
        "result-hpcc-0.8-0-0.buf",
        "result-powerInt-0.8-0-0.buf",
        "result-powerDelay-0.8-0-0.buf",
    ]
    labels = ["HPCC", "PowerInt", "PowerDelay"]

    # Read data and plot
    for fname, lbl in zip(filenames, labels):
        qlens_kb = read_qlens(fname)
        plot_cdf(qlens_kb, lbl)

    # Configure plot
    plt.xlim(-10, 210)  # 0 KB to 200 KB
    plt.ylim(-0.05, 1.05)
    plt.xlabel("Buffer Occupancy (KB)")
    plt.ylabel("CDF")
    plt.legend(loc="best")

    # Save the figure and close
    plt.savefig("cdf_plot_7g.png")
    plt.close()
    
    # Input files and labels
    filenames = [
        "result-hpcc-0.8-16-2000000.buf",
        "result-powerInt-0.8-16-2000000.buf",
        "result-powerDelay-0.8-16-2000000.buf",
    ]
    labels = ["HPCC", "PowerInt", "PowerDelay"]

    # Read data and plot
    for fname, lbl in zip(filenames, labels):
        qlens_kb = read_qlens(fname)
        plot_cdf(qlens_kb, lbl)

    # Configure plot
    plt.xlim(-10, 1510)  # 0 KB to 200 KB
    plt.ylim(-0.05, 1.05)
    plt.xlabel("Buffer Occupancy (KB)")
    plt.ylabel("CDF")
    plt.legend(loc="best")

    # Save the figure and close
    plt.savefig("cdf_plot_7h.png")
    plt.close()

if __name__ == "__main__":
    main()
