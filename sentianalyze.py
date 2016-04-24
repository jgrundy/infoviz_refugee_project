from textblob import TextBlob


def SentiAnalyze(text):
    '''
    This function calls the TextBlob module to perform a sentiment analysis
    for the indicated string x.

    param: text: str on which the sentiment analysis is performed
    '''
    return TextBlob(text).sentiment[0]
