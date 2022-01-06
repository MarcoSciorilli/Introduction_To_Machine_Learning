from pandas import DataFrame


def downloadData(api, companies, count, food_dict=None):
    '''downloads number 'count' tweets from users listed in 'companies' 
        Parameters
        ----------

        Returns
        -------

    '''

    data = DataFrame(
        columns=['tweet_id', 'text', 'favorite_count', 'retweet_count', 'created_at', 'hashtags', 'symbols',
                 'user_mentions', 'urls', 'followers_count', 'friends_count', 'listed_count', 'statuses_count',
                 'user_name'])

    # dummy var needed to create a new row in the dataframe at each step
    n_row = 0

    for company in companies:
        # loop through tweets
        for tweet in api.user_timeline(screen_name=company, count=count):
            # tweets must not be retweeted and must not be replies
            if (not tweet.retweeted) and ('RT @' not in tweet.text) and (not tweet.in_reply_to_status_id_str != None):
                # get decoded tweet's text
                tweets_encoded = tweet.text.encode('utf-8')
                tweets_decoded = tweets_encoded.decode('utf-8')
                # create row in dataframe
                data.loc[n_row] = [tweet.id, tweets_decoded,
                                   tweet.favorite_count, tweet.retweet_count,
                                   tweet.created_at,
                                   tweet.entities['hashtags'], tweet.entities['symbols'],
                                   tweet.entities['user_mentions'], tweet.entities['urls'],
                                   tweet.user.followers_count, tweet.user.friends_count, tweet.user.listed_count,
                                   tweet.user.statuses_count, tweet.user.name]
                # setting new row's index for next iteration
                n_row += 1

    return data


def dictionary_downloader(link):
    '''Function which, given a link, download the whole content of an html webpage
        Parameters
        ----------
        link: the link to the webpage
        Returns
        -------
        The content of the page as a string

    '''
    import bs4
    import urllib.request

    webpage = str(urllib.request.urlopen(link).read())
    soup = bs4.BeautifulSoup(webpage, features="html.parser")

    return soup.get_text()


def api_getter():
    import tweepy as tw
    consumer_key = 'Z1IMMbLAD2QyZ3GBKoBSFpYvt'
    consumer_secret = 'hW87sK80ZfmedsXmvDbHGxsY5aJik9r3ezw5P3oSE5tPh9Ugoc'
    access_token = '1350473122944856068-ErfdzZsziKFKpt5Gy3gh8p2PtxAiTU'
    access_token_secret = 'mp0xj17bVS865YsH0Z0qHdYUnLIQPXSZSpv7AzQzkGPgN'
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    return api


def page_analyzer(page, words_list):
    '''Fuction which analyse an html webpage dictionary in the format of a string, and return a list of the
    entries of the dictionary.
        Parameters
        ----------
        page: the string conteining the page
        word_list: list of the entries of the dictionary(can be an empty list)
        Returns
        -------
        List of the entries of the web dictionary
    '''

    for i in range(4, len(page)):
        word = ""
        j = 1
        if page[i] == 't' and page[i - 2] == 't' and page[i - 4] == 'n' and page[i - 6] == 'r' and page[i - 8] == 't':
            while page[i + j] != ":" and page[i + j] != "(" and (
                    page[i + j] == "\\" and page[i + j + 1] == "t") == False:
                if page[i + j] == "\\":
                    j += 1
                    continue
                word = word + page[i + j]
                j += 1
            words_list.append(word)
            i = i + j
    return words_list


def my_specific_dictionary():
    '''Function which specifically generate the dictionary of our interest
        Parameters
        ----------
        Returns
        -------
        The dictionary we want for our project

    '''
    import string
    alphabet = list(string.ascii_lowercase)
    del alphabet[0]
    food_words = []

    for k in alphabet:
        link = f'https://theodora.com/food/culinary_dictionary_food_glossary_{k}.html'
        page = dictionary_downloader(link)
        page_analyzer(page, food_words)

    link = "https://theodora.com/food/index.html"
    page = dictionary_downloader(link)
    page_analyzer(page, food_words)
    return food_words


def foodtweet_cleaner(dictionar, long_string):
    '''Function which, given a sting and a set of patternes, return if any of the patterns is present in the string
        Parameters
        ----------
        dictionar: List of patterns we want to find in the string
        long_string: The string we want to find patterns into
        Returns
        -------
        True or False, whether any pattern is found in the string
    '''
    import re
    word = re.compile(r'\b|\b'.join(dictionar), re.IGNORECASE).search(long_string)
    if word:
        return True
    else:
        return False
