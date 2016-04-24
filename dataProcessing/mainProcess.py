#!/usr/bin/env python
import pandas as pd
import numpy as np
import re
from sentianalyze import SentiAnalyze
from countrytocity import CountryToCity
from wordcount import WordCount
import pickle


def main():
    data = pd.read_csv('../output/twitterDB_all.csv', header=None)  # read data
    data.columns = ['tweet', 'city']
    data_clean = data.dropna()  # drop na
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
    data_city.loc[:, 'country'] = data_city.loc[:, 'city'] \
                                           .apply(lambda x: CountryToCity(x))
    data_country = data_city[['country', 'senti_score', 'tweet_content']]
    data_country.to_csv('../output/{0}'.format(raw_input('File Name:\n')))
    # word count
    count = WordCount(data_country, 'country', 'tweet_content')
    with open('../output/{0}'.format(raw_input('WordCount Name:\n')), 'w') as fh:
        pickle.dump(count, fh)


if __name__ == '__main__':
    main()
