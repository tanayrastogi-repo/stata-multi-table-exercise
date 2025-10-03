# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "altair==5.5.0",
#     "duckdb==1.4.0",
#     "numpy==2.3.3",
#     "pandas==2.3.3",
#     "plotly==6.3.0",
#     "polars[pyarrow]==1.33.1",
#     "ruff==0.13.2",
#     "sqlglot==27.20.0",
# ]
# ///

import marimo

__generated_with = "0.16.4"
app = marimo.App()

with app.setup:
    # Initialization code that runs before all other cells
    import marimo as mo
    import numpy as np
    import pandas as pd
    import plotly.express as px


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    # TASK 1
    **Tabulate the frequency distribution of the number of tenders per city.**

    ***My attempt:***

    To create the frequency distribution for tender/city, I am simply counting the number of times the "city-name" is repeated in the **tender.dta** file. 

    The bar-plot below visualize the frequency distribution for the tenders for each city, with Budpest showing the highest tenders.
    """
    )
    return


@app.cell(hide_code=True)
def _(tender):
    # Frequency distribution
    tender_per_city = tender["location"].value_counts().reset_index()
    tender_per_city.columns = ["City", "Number of Tenders"]

    # Plotly bar chart
    tender_freq_plot = px.bar(
        tender_per_city,
        x="City",
        y="Number of Tenders",
        text="Number of Tenders",
        title="Frequency Distribution of Tenders per City",
        color="City",
    )

    # Layout styling
    tender_freq_plot.update_traces(textposition="outside")
    tender_freq_plot.update_layout(
        xaxis_title="City",
        yaxis_title="Number of Tenders",
        uniformtext_minsize=8,
        uniformtext_mode="hide",
    )

    tender_freq_plot
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    # TASK 2
    **Tabulate the frequency distribution of the number of bidders per tender.**

    ***My Attempt:***

    Using only the data from **bid.dta**, I grouped the table with tenders and created a list of bidders for each of the tender. This lets me know - 1). actual bidders 2). number of bidders for each tender.

    Below, bar graph shows exactly, how many bidders were there for each of the tender. Also, on hovering, shows the list of the bidders as well.
    """
    )
    return


@app.cell(hide_code=True)
def _(bid):
    # Bidder vs Tender table - This to also have the actual bidder info. Used later in plotting.
    bidders_table = (
        bid.groupby("tender_id")["bidder_id"]
        .apply(lambda s: sorted(pd.Series(s.unique()).astype(int).tolist()))
        .reset_index()
    )

    # Add count and a string version for hover
    bidders_table["Number of Bidders"] = bidders_table["bidder_id"].str.len()
    bidders_table["Bidders_str"] = bidders_table["bidder_id"].apply(
        lambda xs: ", ".join(map(str, xs))
    )

    # Ensure Tender is treated as categorical
    bidders_table["tender_id"] = bidders_table["tender_id"].astype(str)

    # Renaming for plotting
    bidders_table = bidders_table.rename(
        columns={"tender_id": "Tender", "bidder_id": "Bidders"}
    )


    # Plot
    bidder_freq_plot = px.bar(
        bidders_table,
        x="Tender",
        y="Number of Bidders",
        text="Number of Bidders",
        title="Frequency Distribution of Bidders per Tender",
        color="Tender",
    )

    # Layout styling
    bidder_freq_plot.update_traces(
        customdata=np.stack([bidders_table["Bidders_str"]], axis=-1),
        textposition="outside",
        hovertemplate=(
            "<b>Tender %{x}</b><br>"
            "Number of bidders: %{y}<br>"
            "Bidders: %{customdata[0]}"
            "<extra></extra>"
        ),
    )
    bidder_freq_plot.update_layout(
        xaxis_title="Tender",
        yaxis_title="Number of Bidders",
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        showlegend=True,
    )
    bidder_freq_plot
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    # TASK 3

    **Compute the total number of bids for each city pair. For example, how many times did a company from "Szeged" bid for a project in "Miskolc"?**

    ***My Attempt:***

    For this part, I merged the data from all the avialable data. The **bid.dta** is merged with **bidder.dta** over `bidder_id`, which then is merged with **tender.dta** over `tender_id`. This way, I have all the names of bidder_city and tender_city in one single place. 

    Later, it is just the cross-tabulation between the bidder_city and tender_city to see how may times a bidder city has bid for city in tender in particular city. In the heatmap below, we can see a compnay in "Szeged" have bid 2 times for tender in "Miskolc".
    """
    )
    return


@app.cell(hide_code=True)
def _(merged):
    # Pair-wise matrix
    tender_bidder_matrix = pd.crosstab(
        merged["bidder_city"], merged["tender_city"]
    )

    # Plot heatmap
    heatmap = px.imshow(
        tender_bidder_matrix,
        text_auto=True,
        labels=dict(x="Tender City", y="Bidder City", color="Bid Count"),
    )
    heatmap
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    ## TASK 4

    **For each potential bidder in each potential tender (not only the ones that actually bid), create a dummy variable local_experience, which takes the value 1 if the bidder has bid in the same city as the tender before the year of the tender, and 0 otherwise. Cross-tabulate the frequency distribution of this variable with the year of the tender.**

    ***My Attempt:***

    In order to do this task, I created a column in the **merged** dataframe, called "first_bid_year_in_city". This highlights the first time a bidder bid for a specific city. Using the value in this column, if the tender year is greater than first bid year, then "local_experience" has value 1. 

    Later, the frequency table for local_experience or not is created using cross-tab between columns "tender_year" and "local_experience". Below shows, the frequency for each of the fields.
    """
    )
    return


@app.cell(hide_code=True)
def _(merged):
    # Bidder’s first year in each city
    first_year_in_city = (
        merged.groupby(["bidder_id", "tender_city"], as_index=False)["tender_year"]
        .min()
        .rename(columns={"tender_year": "first_bid_year_in_city"})
    )

    # Adding this to the merged data to potential dataframe containing all the information
    potential = merged.merge(
        first_year_in_city, on=["bidder_id", "tender_city"], how="left"
    )

    # Adding Local expereince value based on if the first_bid_year_in_city is less than tender year
    potential["local_experience"] = (
        potential["first_bid_year_in_city"] < potential["tender_year"]
    ).astype(int)
    return (potential,)


@app.cell(hide_code=True)
def _(potential):
    (
        pd.crosstab(potential["tender_year"], potential["local_experience"])
        .rename(columns={0: "no_local_experience", 1: "has_local_experience"})
        .sort_index()
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    ----
    ### Data Wrangling and Setup

    * Loading of all the data.
    * Formatting of the datatypes.
    * Creating other dataframe for analysis use.
    """
    )
    return


@app.function
# Function to force datatype
def astype_columns(df: pd.DataFrame, dtype_map: dict):
    return df.astype(dtype_map)


@app.cell
def _():
    # Loading .dta files
    bid = (
        pd.read_stata("data/bid.dta").pipe(  # Reading data
            astype_columns, {"tender_id": int, "bidder_id": int}
        )  # Datatype matching
    )
    return (bid,)


@app.cell
def _():
    # Loading bidder.dta files
    bidder = pd.read_stata("data/bidder.dta").pipe(
        astype_columns, {"bidder_id": int, "city": str}
    )
    return (bidder,)


@app.cell
def _():
    # Loading tender .dta files
    tender = pd.read_stata("data/tender.dta").pipe(
        astype_columns, {"tender_id": int, "year": int, "location": str}
    )
    return (tender,)


@app.cell
def _(bid, bidder, tender):
    ## Merge the three dataset together to have one common frame.
    merged = bid.merge(
        bidder.rename(columns={"city": "bidder_city"}), on="bidder_id", how="left"
    ).merge(
        tender.rename(columns={"location": "tender_city", "year": "tender_year"}),
        on="tender_id",
        how="left",
    )
    return (merged,)


if __name__ == "__main__":
    app.run()
