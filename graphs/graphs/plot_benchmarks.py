from functools import reduce
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from typing import List

IMAGES_PATH = '../images'

def get_actions(df: pd.DataFrame, *args: List[str]):
    actions = list(map(lambda x: df["Action"] == x, args))
    combined_actions = reduce(lambda x, y: x | y, actions)
    df = df.loc[combined_actions]
    df = df.sort_values("Amount")
    return df

def split_amount_into_column(df: pd.DataFrame):
    df[["Action", "Amount"]] = df["Name"].str.split('/', expand=True)
    return df

def plot_benchmark(df: pd.DataFrame, xlabel=None, ylabel=None, legend_title=None, legend_labels=[]):
    ax = sns.barplot(x="Amount", y="Mean", hue="Action", data=df, palette="pastel")
    ax.set_yscale('log')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    leg = ax.legend()
    leg.set_title(legend_title)
    for i in range(len(legend_labels)):
        leg.get_texts()[i].set_text(legend_labels[i])

if __name__ == "__main__":
    benchmarks_df = pd.read_csv('./data/new_generate_benchmarks.csv')

    split_df = split_amount_into_column(benchmarks_df)

    df_fib_fib_map = get_actions(split_df, "Generate (Fib, Map)", "Generate (Fib, Map) with Map")
    df_fib_map_change = get_actions(split_df, "Generate (Fib, Map) with Map", "Generate (Fib, Map) with Map Single Change")

    plot_benchmark(df_fib_fib_map, "The Amount of Nodes (2n + 1)", "The Mean Execution Time in Seconds", legend_title="Compute Fibonacci and Map", legend_labels=["Without Map", "With Map"])
    plt.show()
    plt.clf()

    plot_benchmark(df_fib_map_change, "The Amount of Nodes (2n + 1)", "The Mean Execution Time in Seconds", legend_title="Compute Fibonacci and Map with Map", legend_labels=["Zero Changes", "Single Change"])
    plt.show()
    plt.clf()
    