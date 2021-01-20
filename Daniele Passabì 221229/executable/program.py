import pandas as pd
import math
import plotly.express as px     # used to plot the data
import ast                      # used to transform string into list
from collections import Counter # used to count the occurrences of hashtags
from statistics import mean
import string                   # used to remove punctuation from text in an efficient way
import datetime
import time
import json
import sys

# MLXTEND APRIORI
from mlxtend.frequent_patterns import apriori as mlxtend_apriori
from mlxtend.preprocessing import TransactionEncoder

print(" > All libreries imported")

###

number_of_itemsets = int(sys.argv[1]) # if 0 --> all

###

df_path = "../data/clean_df/clean_df.pkl"
df = pd.read_pickle(df_path)

print(" > Dataset correctly imported")

###

print(" > Start of Apriori computation")

start = time.time()

results_list = []
curr_day = datetime.date(2020, 7, 24)  # first day of the data
last_day = datetime.date(2020, 8, 30)  # last day of the data

# iterate on every day of the dataset (until we reach the last one)
while (curr_day <= last_day):

    # prepare the list of item of the day
    texts_for_apriori = []
    for t in df.loc[df['date'] == curr_day]["text"]:
        texts_for_apriori.append(t)

    print(" >> Computing APriori on day:", curr_day, "| Total tweets:", len(texts_for_apriori))

    te = TransactionEncoder()
    te_ary = te.fit(texts_for_apriori).transform(texts_for_apriori)
    mlxtend_input = pd.DataFrame(te_ary, columns=te.columns_)

    # computation of APriori [only if Total tweets > 0]
    if len(texts_for_apriori) > 0:
        daily_groups = mlxtend_apriori(mlxtend_input, min_support=0.015, use_colnames=True)
        results_list.append([curr_day, daily_groups])
    
    else:
        results_list.append([curr_day, []])

    # add 1 day and repeat the procedure
    curr_day = curr_day + datetime.timedelta(days=1)

end = time.time()
mlxtend_apriori_time = end - start

print(" > Apriori computation completed")
print(" > Elapsed time:", "%.2f" % round(mlxtend_apriori_time, 2), "seconds")

###

print(" > Storing results...")

final_results = {}

# iterate on every [date, [[group_of_2],[group_of_3]]]
for res in results_list:

    date = res[0]    # get the date
    df = res[1]      # get the df with all the itemsets

    # iterate on every row of the df
    n = len(df)
    
    if n > 0: # we ignore empty dataset

        i = 0
        while i < n:

            key = df["itemsets"][i]
            support = df["support"][i]

            # if the key is already in the solutions dict --> update its value with current data
            if key in final_results:
                final_results[key][0].append(date)
                final_results[key][1].append(support)

            # if it is a new group --> create a list with the date value
            else:
                final_results[key] = [[date],[support]]

            i = i+1

words_column = []
dates_column = []
count_column = []
for k,v in final_results.items():
    words_column.append(k)
    dates_column.append(v[0])
    count_column.append(v[1])

final_results_df = pd.DataFrame(
    {'itemsets': words_column,
     'dates': dates_column,
     'supports': count_column
    })

count_dates = []
for l in final_results_df["dates"]:
    count_dates.append(len(l))

final_results_df["tot_dates"] = count_dates
final_results_df = final_results_df.loc[final_results_df['tot_dates'] > 1]
final_results_df = final_results_df.sort_values(by=['tot_dates'], ascending=False)

# select only the requested number of itemsets (if requested)
if number_of_itemsets != 0 and number_of_itemsets < len(final_results_df):
    final_results_df = final_results_df[0:number_of_itemsets]

# save the data (could be useful in the future)
final_results_df.to_csv("../data/results/results_df_exec.csv")
final_results_df.to_pickle("../data/results/results_df_exec.pkl")

print(" > Results correctly stored in 'data/results'")