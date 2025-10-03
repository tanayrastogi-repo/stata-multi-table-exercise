# Stata Multi-table exercise
Repo analyse the patterns with which different companies bid on tenders in different cities.

## Data
Explore the data in the `data/` folder. There are three tables.

1. `bidder.dta` - contains information about the bidders, including their unique identifier and their city
2. `tender.dta` - contains information about the tenders, including their unique identifier, the date they were opened, and the location of the project
3. `bid.dta` - contains information about the bids, including the unique identifier of the bidder and the unique identifier of the tender. The table includes all the bidders: those that are not included have not bid on that particular tender.


## Tasks

1. Tabulate the frequency distribution of the number of tenders per city.
2. Tabulate the frequency distribution of the number of bidders per tender.
3. Compute the total number of bids for each city pair. For example, how many times did a company from "Szeged" bid for a project in "Miskolc"?
4. For each potential bidder in each potential tender (not only the ones that actually bid), create a dummy variable `local_experience`, which takes the value 1 if the bidder has bid in the same city as the tender *before* the year of the tender, and 0 otherwise. Cross-tabulate the frequency distribution of this variable with the year of the tender.

## Output files
The code is built on Marimo notebook with UV backend. All the code is present in the `my_notebook.py` file.

The code/output can be access in the following way:

 * 