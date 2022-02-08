from functools import reduce
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate
import pandas as pd
from typing import List

IMAGES_PATH = '../images'
TABLES_PATH = '../tables'

def get_actions(df: pd.DataFrame, *args: List[str]):
    actions = list(map(lambda x: df["Action"] == x, args))
    combined_actions = reduce(lambda x, y: x | y, actions)
    df = df.loc[combined_actions]
    df = df.sort_values(["Amount", "Action"])
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
    plot_benchmark(actions_df, actions, xlabel, ylabel, legend_title, legend_labels)
    plt.savefig(f"{IMAGES_PATH}/{file_path}.pdf")

def format_column_sci(values: pd.Series) -> pd.Series:
    return values.apply(lambda x: "{:.3e}".format(x))

def save_table_benchmark(
    file_path: str,
    df: pd.DataFrame,
    actions: List[str], 
    xlabel: str, 
    ylabel: str, 
    legend_title: str, 
    legend_labels: List[str]
):
    actions_df = get_actions(df, *actions)
    headers = ["Amount", "Action", "Mean", "Stddev"]
    actions_df["Mean"] = format_column_sci(actions_df["Mean"])
    actions_df["Stddev"] = format_column_sci(actions_df["Stddev"])
    print(actions_df)
    table = tabulate(actions_df[headers], headers=headers, tablefmt="latex_raw", showindex=False, disable_numparse=True)
    f = open(f"{TABLES_PATH}/{file_path}.tex", "w")
    f.write(table)


if __name__ == "__main__":
    benchmarks_df = pd.read_csv('./data/benchmarks.csv')

    split_df = split_amount_into_column(benchmarks_df)

    save_plot_benchmark(
        "plot_generate_result_benchmark",
        split_df,
        ["Generate Result", "Generate (Result, Map)", "Generate (Result, Map) with Map"],
        xlabel="The Amount of Nodes (2n + 1)",
        ylabel="The Mean Execution Time in Seconds",
        legend_title="Compute Result",
        legend_labels=["cataSum", "cataMerkleTree", "cataMerkleTreeWithMap"]
    )

    save_table_benchmark(
        "plot_generate_result_benchmark",
        split_df,
        ["Generate Result", "Generate (Result, Map)", "Generate (Result, Map) with Map"],
        xlabel="The Amount of Nodes (2n + 1)",
        ylabel="The Mean Execution Time in Seconds",
        legend_title="Compute Result",
        legend_labels=["cataSum", "cataMerkleTree", "cataMerkleTreeWithMap"]
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
