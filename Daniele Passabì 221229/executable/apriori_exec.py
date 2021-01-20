
import pandas as pd
import math
import plotly.express as px     # used to plot the data
import ast                      # used to transform string into list
from collections import Counter # used to count the occurrences of hashtags
from statistics import mean
import string                   # used to remove punctuation from text in an efficient way
import datetime
from efficient_apriori import apriori
import json
import time

print(" > All libreries imported")

###

df_path = "../data/clean_df/clean_df.pkl"
df = pd.read_pickle(df_path)

print(" > Dataset correctly imported")

###

print(" > Start of Apriori computation")

start = time.time()

curr_day = datetime.date(2020, 7, 24)  # first day of the data
last_day = datetime.date(2020, 8, 30)  # last day of the data
results_list = []

# iterate on every day of the dataset (until we reach the last one)
while (curr_day <= last_day):

    # prepare the list of item of the day
    texts_for_apriori = []
    for t in df.loc[df['date'] == curr_day]["text"]:
        texts_for_apriori.append(t)

    print(" >> Computing APriori on day: ", curr_day, " | Total tweets: ", len(texts_for_apriori))

    # computation of APriori [only if Total tweets > 0]
    if len(texts_for_apriori) > 0:
        itemsets, rules = apriori(texts_for_apriori, min_support=0.012,  min_confidence=0.8)

        # Save the results in a more convenient way
        list_of_groups = []
        for item in itemsets.values():
            list_of_groups.append(item)   # there are always groups of 1, 2 and 3 words. Sometimes more.

        threshold = 0.015
        daily_groups = []
        for group in list_of_groups:
            daily_groups.append({k: v/len(texts_for_apriori) for k, v in group.items() if v/len(texts_for_apriori) > threshold})
        
        results_list.append([curr_day, daily_groups])

    else:
        # Save the day and an empty list
        results_list.append([curr_day, [{}]])

    # add 1 day and repeat the procedure
    curr_day = curr_day + datetime.timedelta(days=1)

end = time.time()

print(" > Apriori computation completed")
print(" > Elapsed time: ", end - start)

###

print(" > Storing results...")

final_results = {}

# iterate on every [date, [[group_of_2],[group_of_3]]]
for res in results_list:

    date = res[0]           # get the date
    list_of_groups = res[1] # in pos 0 --> 1 word, in pos 1 --> 2 words, ...

    # iterate on every pair of every groups

    for group in list_of_groups:

        for key, value in group.items():

            # if the key is already in the solutions dict --> update its value with current data 
            if key in final_results:
                final_results[key][0].append(date)
                final_results[key][1].append(value)

            # if it is a new group --> create a list with the date value
            else:
                final_results[key] = [[date],[value]]

words_column = []
dates_column = []
count_column = []
for k,v in final_results.items():
    words_column.append(k)
    dates_column.append(v[0])
    count_column.append(v[1])

final_results_df = pd.DataFrame(
    {'group_of_words': words_column,
     'dates': dates_column,
     'frequencies': count_column
    })

# save the data (could be useful in the future)
final_results_df.to_csv("../data/results/apriori_df.csv")
final_results_df.to_pickle("../data/results/apriori_df.pkl")

print(" > Results correctly stored in 'data/results'")