# Workflow of the project

## 01 - Preliminary analysis and DF cleaning
1. I started analysing the dataset provided and removed the columns that I found not useful for our objective.
2. Hashtags were stored as characters, I turned them into lists.
3. Brief analysis on hashtags, in order to understand which were the most used of all.
4. In-depth analysis on text, from which I understood that:
    - text aren't complete
    - at the end of each text there's an URL to the complete source
    - there are references to other users (use of @)
    - there are, of course, hashtags (use of #)
    - there was the necessity to remove stopwords
    - about numbers, I thought I could ignore them, but due to future results where they provide no useful information (almost the opposite) I went back and decided to remove them from the text.

    As a consequence of those observations:
    - I saved the URL for possible future analysis with the complete text
    - I removed from the text:
        - links
        - punctuation and symbols
        - stopwords
        - numbers (after not doing it the first time) 

    I also realised that for the day-by-day analysis that I wanted to do I did not need the exact hours of the tweet posted, but just the day, so I cleaned the column `date` of the hours.

    Finally, i saved the df in two formats:
    - `.csv`, since it is easily readable and known
    - `.pkl`, since it is really useful in maintaining all the properties of the dataset

    The cleaned dataframes can be found in the `data/clean_df` directory.

### Update of 24/12
- use of `apply` function instead of `for` to enhance performances in cleaning text procedure
- added a `stemming` procedure in the cleaning of the data to get better results

---

## 02 - First test with the APriori algorithm
The first part of the solution implies the finding of frequent itemsets for each day of the dataset. I decided to use the APriori algorithm.

I chose to use two different implementations, to see which was better.
  - Efficient APriori [https://pypi.org/project/efficient-apriori/] since I have used it in the past and I knew it was fast and reliable.
  - mlxtend Apriori [https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/], found searching for other options

I did two test for each implementation:
- the 1st one was on a day with a small number of tweets
- the 2nd one was on a day with a large number of tweets

From those tests I understood two main things:
- I could not use the absolute value of the support. The percentage on the total tweets of the day was more appropriate for a uniform analysis.
- Numbers create problems and provide no information, so I took the decision to remove them from the tweets.
- The two implementations provide the same results, but the mlxtend is much faster. For this reason its APriori implementation was used in the main solution.

---

## 03 - Use of APriori on the whole dataset, day by day + final solution
Here I computed the APriori on each day of the dataset. 

After the computation was complete, I stored the results in the following way.

| itemsets        | dates                 | supports            | tot_dates   |
|-----------------|-----------------------|---------------------|-------------|
| (word1, word2)  | [date1, date4, date6] | [0.02,0.03,0.015]   | 3           |
| (word2, word7)  | [date2, date14]       | [0.016,0.018]       | 2           |
| ...             | ...                   | ...                 | ...         |

As I did for the dataset, I then saved the results as `results_df.csv` and `results_df.pkl`.

The results are stored in the `data/results` directory.

---

## 04 - Plot of the results
We have all the results, but I thought it could be more meaningful to plot them.

Here I understood that:
- for the `supports` value it makes little sense to use the absolute value. It's better to use *count/total_tweets_of_the_day*

---

## 05 - Comparison with some baseline method

- I compared the `mlxtend` algorithm implementation with the `efficient APriori` implementation
- I run them both on the clean dataframe n = 100 times and confronted the mean time needed to compute the results
- They provide the same results, but the `mlxtend` implementation is much faster

---

## 06 - Scalability test

I run the algorithm on an increasing number of tweets and compared the times, to understand if we could use this solution with a very large amount of data. 


