import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

IMAGES_PATH = '../images'

benchmarks_df = pd.read_csv('./data/benchmarks.csv')

def plot_benchmark(df):
    ax = sns.barplot(x="Name", y="Mean", data=df, yerr=df["Stddev"])
    ax.set_yscale('log')

plot_benchmark(benchmarks_df[30:40])

plt.show()