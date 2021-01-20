
# How to execute the program

---

## Prerequisites 

1) Installation of Python 3.8.5 or more
2) For the program to run correctly, it is necessary to install some libraries. Below is the list of used libraries:
    - `pandas`
    - `math`
    - `plotly.express`
    - `ast`
    - `collections`
    - `statistics`
    - `string`
    - `datetime`
    - `time`
    - `json`
    - `sys`
    - `mlxtend`

    You can install new libraries with the following command, within the command prompt: `pip install name_of_library`

---

## Execution with .py script

1) Download the source project folder `Daniele Passabì 221229`

2) Open the command prompt and navigate to the `executable` directory. Here, you will find a script named `program.py`

3) Run the `.py` script: in the command prompt the command is the following `python program.py arg`
    - `arg` is the external parameter to be passed to the script via the command line. It represents the number of itemsets we want the solution to return, so it **must** be a number. If you want all possible itemsets, enter 0.

    Example: `python program.py 50` will return the 50 most frequent itemset in time, based on the total number of dates in which the itemset is present.  

---

## Notes 
- The program takes as input the cleaned dataset, which is found in `data/clean_df/clean_df.pkl`. 

  It is possible to use this program with other datasets than the one given, if they respect the following input format:
   - the dataset must have the column `date`, with dates in it
   - the dataset must have the column `text`, with list of words in it
   - the dataset must be in `.pkl` format, to preserve the properties of the variables
- The results of the APriori algorithm can be found in `data/results/results_df_exec.pkl` (or `data/results/results_df_exec.csv`)