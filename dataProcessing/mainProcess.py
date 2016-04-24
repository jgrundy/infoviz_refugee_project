#!/usr/bin/env python
import pandas as pd
import numpy as np
import re
from sentianalyze import SentiAnalyze
from countrytocity import CountryToCity
from wordcount import WordCount
import pickle


def main():
    print 'cleaning data.'
    data = pd.read_csv('../output/twitterDB_all.csv', header=None)  # read data
    data.columns = ['tweet', 'city']
    data_clean = data.dropna()  # drop na
    print 'sentiment analysis.'
    data_clean.loc[:, 'senti_score'] = np.nan
    regex = '(\shttp[s]:\\\\)'
    data_clean.loc[:, 'tweet_content'] = data_clean.tweet \
                                                   .apply(lambda x:
                                                          re.split(regex,
                                                                   x)[0])
    regex2 = '\s@.+\:\s'
    data_clean.loc[:, 'tweet_content'] = data_clean.tweet_content \
                                                   .apply(lambda x:
                                                          re.split(regex2,
                                                                   x)[-1])
    # sentimental analysis
    data_clean.loc[:, 'senti_score'] = data_clean.tweet_content \
                                                 .apply(lambda x:
                                                        SentiAnalyze(x))
    data_city = data_clean[['city', 'senti_score', 'tweet_content']]
    data_city.reset_index(drop=True, inplace=True)
    # geocode the country name
    print 'convert city to country.'
    data_city.loc[:, 'country'] = np.nan
    city_names = data_clean.city.unique()
    city_country = {}
    print 'call google api'
    for city in city_names:
        city_country[city] = CountryToCity(city)
    print 'city country matching.'

    def f(x):
        if x in city_country.keys():
            return city_country[x]
        else:
            return x
    data_city['country'] = data_city.city.apply(f)
    data_country = data_city[['country', 'senti_score', 'tweet_content']]
    print 'save the dataframe with sentimental score.'
    data_country.to_csv('../output/{0}.csv'.format(raw_input('File Name:\n')))
    # word count
    print 'word count.'
    count = WordCount(data_country, 'country', 'tweet_content')
    print 'save the word count pickle file'
    filename = raw_input('WordCount Name:\n')
    with open('../output/{0}.pkl'.format(filename), 'w') as fh:
        pickle.dump(count, fh)


if __name__ == '__main__':
    main()
