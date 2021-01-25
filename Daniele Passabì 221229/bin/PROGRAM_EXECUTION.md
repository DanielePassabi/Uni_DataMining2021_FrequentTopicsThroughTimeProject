
# How to execute the program

## Prerequisites 

1) Installation of `Python 3.8.5` or more
2) For the program to run correctly, it is necessary to install two libraries:
    - `pandas 1.2.1`
    - `mlxtend 0.18.0`

    It is recommended to create a virtual environment for the project, where to install the required libraries. 
    
    To install the libraries, open the command prompt and activate your virtual environment. You can install the libraries in two ways.

    Using the `requirements.txt` file, once you have navigated to the `bin` directory.
    ```
    pip install -r requirements.txt
    ```
    
    Or manually installing the libraries in your python environment.
    ```
    pip install name_of_library
    ```

---

## Execution with .py script

1) Download the source project folder `Daniele Passabì 221229`

2) Open the command prompt and navigate to the `bin` directory. Here, you will find a script named `program.py`

3) Run the `.py` script

    The user can set three parameters, which are:
    - The minimum *support* necessary for a topic to be considered frequent in the tweets of the day. The default value is 0.015.
    - The minimum *number of days* in which the topic has to compare to be in the final solution. The default value is 2.
    - The total number of topics to be present in the solution. The default value is 0, which indicates all the possible solution.

    **Important note**: all the parameters **must** be numbers and the order **is** relevant. 

    An example of execution follows. 
    ```
    python program.py 0.02 5 100
    ```

    This specific execution will return a dataset of 100 rows, where all the topics appear at least in 5 different days, with a support of at least 0.02. 


    However, it is possible to just run the program without additional arguments, with the following command:
    ```
    python program.py
    ```
    Doing so, the program will use the default parameters mentioned above.

4) Results

    The results of the algorithm can be found in `data/results/results_df_exec.pkl` (or `data/results/results_df_exec.csv`). This implies that the directories **must** exist.

---

## Notes

### Dataset
The program takes as input the cleaned dataset, which is found in `data/clean_df/clean_df.pkl`. 

  It is possible to use this program with other datasets than the one given, if they respect the following input format:
   - the dataset must have the column `date`, with dates in it;
   - the dataset must have the column `text`, with list of words in it;
   - the dataset must be in `.pkl` format, to preserve the properties of the variables.

### Execution with .exe file
During the user evaluation, it was noted that the use of an executable could make the execution of the program easier for less experienced users. For this reason, there is an `.exe` file in `src/executable/windows`.

It is possible to run the program with its default values simply by opening the `.exe` file. 

If instead the user want to use custom parameters, he has to open the cmd, navigate to the folder where the `.exe` file is and type:

```
program.exe arg1 arg2 arg3
```

Where `arg1`, `arg2`, `arg3` refer to the parameters aforementioned. The results will be found in the same dir as the `.exe`.