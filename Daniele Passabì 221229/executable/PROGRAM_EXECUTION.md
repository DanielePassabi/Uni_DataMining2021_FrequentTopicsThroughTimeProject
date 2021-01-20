
## How to execute the program

### Prerequisites 

1) Python 3.8.5 or more
2) List of libraries used:
    - `pandas`
    - `math`
    - `plotly.express`
    - `ast`
    - `collections`
    - `statistics`
    - `string`
    - `datetime`
    - `efficient_apriori`
    - `json`
    - `time`

### Execution with .py script

1) Download the source project folder `Daniele Passabì 221229`

2) Run the .py executable: in the command prompt the command is the following `python apriori_exec.py`, once in the `executable` directory

### Notes 
- The program takes as an input the cleaned dataset, which is found in `data/clean_df/clean_df.pkl`. 

  It is possible to use this program with other dataset than the one given, if they respect the following input format:
   - the dataset must have the column `date`, with dates in it
   - the dataset must have the column `text`, with list of words in it
- The results of the APriori algorithm can be found in `data/results/apriori_df.pkl` (or `data/results/apriori_df.csv`)