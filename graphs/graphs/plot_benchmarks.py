from functools import reduce
import seaborn as sns
import matplotlib.ticker as tck
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

def plot_benchmark(df: pd.DataFrame, actions=[], xlabel=None, ylabel=None, legend_title=None, legend_labels=[]):
    ax = sns.barplot(x="Amount", y="Mean", hue="Action", data=df, palette="pastel", hue_order=actions)
    ax.set_yscale('log')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    leg = ax.legend()
    leg.set_title(legend_title)
    for i in range(len(legend_labels)):
        leg.get_texts()[i].set_text(legend_labels[i])

def show_plot_benchmark(
    df: pd.DataFrame, 
    actions: List[str], 
    xlabel: str, 
    ylabel: str, 
    legend_title: str, 
    legend_labels: List[str]
):
    actions_df = get_actions(df, *actions)
    plot_benchmark(actions_df, actions, xlabel, ylabel, legend_title, legend_labels)
    plt.show()
    plt.clf()

def save_plot_benchmark(
    file_path: str,
    df: pd.DataFrame, 
    actions: List[str], 
    xlabel: str, 
    ylabel: str, 
    legend_title: str, 
    legend_labels: List[str]
):
    actions_df = get_actions(df, *actions)
    print(actions_df)
    plot_benchmark(actions_df, actions, xlabel, ylabel, legend_title, legend_labels)
    plt.savefig(f"{IMAGES_PATH}/{file_path}.pdf")

if __name__ == "__main__":
    benchmarks_df = pd.read_csv('./data/benchmarks.csv')

    split_df = split_amount_into_column(benchmarks_df)

    split_df
    print(split_df)

    save_plot_benchmark(
        "plot_generate_result_benchmark",
        split_df,
        ["Generate Result", "Generate (Result, Map)", "Generate (Result, Map) with Map"],
        xlabel="The Amount of Nodes (2n + 1)",
        ylabel="The Mean Execution Time in Seconds",
        legend_title="Compute Result",
        legend_labels=["Only Sum", "Sum and Map", "Sum and Map with Map"]
    )

    # show_plot_benchmark(
    #     split_df,
    #     ["Generate (Fib, Map)", "Generate (Fib, Map) with Map"],
    #     xlabel="The Amount of Nodes (2n + 1)",
    #     ylabel="The Mean Execution Time in Seconds",
    #     legend_title="Compute Fibonacci and Map",
    #     legend_labels=["Without Map", "With Map"]
    # )

    # show_plot_benchmark(
    #     split_df,
    #     ["Generate (Fib, Map) with Map", "Generate (Fib, Map) with Map Single Change"],
    #     xlabel="The Amount of Nodes (2n + 1)",
    #     ylabel="The Mean Execution Time in Seconds",
    #     legend_title="Compute Fibonacci and Map with Map", 
    #     legend_labels=["Zero Changes", "Single Change"]
    # )
