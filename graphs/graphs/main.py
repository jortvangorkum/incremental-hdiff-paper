# Import seaborn
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

IMAGES_PATH = '../images'

x_labels = [
    100,
    1000,
    10000,
    100000,
]

original_time = [
    0.0,
    0.02,
    0.24,
    2.19,
]

original_memory = [
    13868648,
    124578128,
    1243740464,
    12433126648
]

hashmap_time = [
    0.01,
    0.08,
    2.40,
    160.94,
]

hashmap_memory = [
    35376640,
    323777104,
    3242785784,
    32447783024,
]

df_time = pd.DataFrame(
    [original_time, hashmap_time],
    columns=x_labels,
    index=pd.Index(['Original Time', 'Hash Map Time']),
).T

df_memory = pd.DataFrame(
    [original_memory, hashmap_memory],
    columns=x_labels,
    index=pd.Index(['Original Memory', 'Hash Map Memory']),
).T

def plot_time(df):
    g = sns.lineplot(data=df)
    g.set(xscale="log")
    g.set(yscale="log")
    g.set(xlabel='Amount of lines', ylabel='Amount of time (in seconds)')

def plot_memory(df):
    g = sns.lineplot(data=df)
    g.set(xscale="log")
    g.set(yscale="log")
    g.set(xlabel='Amount of lines', ylabel='Amount of memory (in bytes)')

plot_time(df_time)
plt.savefig(f"{IMAGES_PATH}/plot_time_decorate_trees.pdf")
plt.clf()

plot_memory(df_memory)
plt.savefig(f"{IMAGES_PATH}/plot_memory_decorate_trees.pdf")
plt.clf()