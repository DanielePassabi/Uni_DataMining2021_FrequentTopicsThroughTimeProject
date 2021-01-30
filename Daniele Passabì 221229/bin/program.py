import pandas as pd
import datetime
import time
import sys

# MLXTEND APRIORI
from mlxtend.frequent_patterns import apriori as mlxtend_apriori
from mlxtend.preprocessing import TransactionEncoder

print("\n > All libreries imported")

###

# all the arguments must be passed, the order IS relevant
if len(sys.argv) == 4: # NB: 4 because argv[0] is the name of the script
    # minimum support
    min_supp = float(sys.argv[1])

    # minimum number of dates in which the itemset has to compare (if 0 --> all)
    min_dates = int(sys.argv[2])

    # number of total rows in the solution (if 0 --> all)
    number_of_itemsets = int(sys.argv[3])
else:
    # Default parameters
    min_supp = 0.015
    min_dates = 2
    number_of_itemsets = 0 # all

print("\n > Parameters setted")
print(" >> Support:", min_supp)
print(" >> Minimum number of dates per topic:", min_dates)

if number_of_itemsets == 0:
    print(" >> Total number of topics in the results: max")
else:
    print(" >> Total number of topics in the results:", number_of_itemsets)

###

df_path = "../data/clean_df/clean_df.pkl"
df = pd.read_pickle(df_path)

print("\n > Dataset correctly imported")

###

print("\n > Start of Apriori computation")

start = time.time()

results_list = []

curr_day = min(df['date'])  # first day of the data
last_day = max(df['date'])  # last day of the data

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
        daily_groups = mlxtend_apriori(mlxtend_input, min_support=min_supp, use_colnames=True)
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

print("\n > Obtaining results...")

final_results = {}

# iterate on every [date, df]
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

# select only the results with the requested number of min_dates
if min_dates == 0:
    final_results_df = final_results_df.loc[final_results_df['tot_dates'] > 1]
else:
    final_results_df = final_results_df.loc[final_results_df['tot_dates'] >= min_dates]

# order the results by total dates
final_results_df = final_results_df.sort_values(by=['tot_dates'], ascending=False)

# select only the requested number of itemsets (if requested)
if number_of_itemsets != 0 and number_of_itemsets < len(final_results_df):
    final_results_df = final_results_df[0:number_of_itemsets]

# save the data (could be useful in the future)
final_results_df.to_csv("../data/results/results_df_exec.csv")
final_results_df.to_pickle("../data/results/results_df_exec.pkl")

print("\n > Results correctly stored in 'data/results'")