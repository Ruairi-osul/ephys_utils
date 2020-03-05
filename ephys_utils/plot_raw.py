import numpy as np
import matplotlib.pyplot as plt


def load_dat_data(p, n_chans=32):
    """Loads dat data into a np.memmap object

    Given a path to a .dat file, infers file size and returns
    memmap object
    """
    print(f"loading temp: {p}")
    tmp = np.memmap(p, dtype=np.int16)
    shape = int(len(tmp // n_chans))
    print(f"loading for real: {p}")
    return np.memmap(p, dtype=np.int16, shape=(shape, n_chans))


def plot_raw(
    p,
    spiketimes,
    chan,
    n_chans=32,
    t_start=None,
    total_duration=5,
    ax=None,
    fs=30000,
    skip=100,
):
    """
    Plots raw spiketrain
    Given the path to raw data and an array of spiktimes, and a channel,
    plots the raw data and with the spiketimes highlighted
    """

    print("converting spiketimes")
    spiketimes *= fs
    print("loading raw data")
    raw_data = load_dat_data(p, n_chans=n_chans)[:, chan]
    print("calculating t_start")
    if not t_start:
        t_start = spiketimes[0]
    else:
        t_start *= fs
    print("getting total_durration")
    if not total_duration:
        t_stop = spiketimes[-1]
        total_duration = (t_stop - t_start) / fs
    else:
        t_stop = t_start + (total_duration * fs)
    if not ax:
        _, ax = plt.subplots()

    print("getting raw data")
    y = raw_data[t_start:t_stop:skip]
    x = np.linspace(t_start, t_stop, len(y))
    print("plotting now")
    ax.plot(x, y, alpha=0.4, color="grey")
    print("done plotting")
    return ax
