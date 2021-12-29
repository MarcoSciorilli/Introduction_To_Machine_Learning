import tweepy as tw
from pandas import DataFrame
import sys
sys.path.append('../')
from Final_project.tweetload import downloadData, dictionary_downloader, api_getter,page_analyzer,my_specific_dictionary

if __name__ == '__main__':

    with open("food_brands") as file:
        companies = file.readlines()
        companies = [line.rstrip() for line in companies]


    dictionar = set(my_specific_dictionary())
    print(dictionar)
import re


