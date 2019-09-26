#!/usr/bin/env python
#Sam Wiston
#Last Edited 9/26/19 2:30PM EDT

from bs4 import BeautifulSoup
import requests
import re
import json

def getScript(url):
    urlRequest = requests.get(url)
    pageSoup = BeautifulSoup(urlRequest.text, "html.parser")
    article = pageSoup.find('div', {'class':'scrolling-script-container'})
    return article

def choseShow(term):
    #Takes a term to search for in the springfieldspringfield system.
    #I am using their search system as it can be easily accessed
    url = "https://www.springfieldspringfield.co.uk/tv_show_episode_scripts.php?search={}".format(term)
    urlRequest = requests.get(url)
    pageSoup = BeautifulSoup(urlRequest.text, "html.parser")

    #Grabs an array of all results
    results = pageSoup.find_all('a', {'class':'script-list-item'})

    #Checks number of results
    #If none, quit
    #If one, check if that's correct
    if len(results) is 0:
        print("No results found")
        quit()
    elif len(results) is 1:
        choice = input("Found \"{}\" Is this correct? (y/n): ".format(results[0].text))
        if choice is 'y':
            return results[0]['href']
        else:
            quit()
    else:
        #Prints the results for choosing
        number = 1
        for result in results:
            print("{}. {}".format(number, result.text))
            number += 1
        choice = input("Which {}? ".format(term))

        #Exceptions for inputing strings or out of range numbers
        try:
            choice = int(choice)
        except ValueError:
            print("Error: Please enter a number.")
            quit()
        try:
            return results[choice-1]['href']
        except IndexError:
            print("Error: Please enter a number 1-{}".format(len(results)))
            quit()

term = input("Input search term: ")
extension = choseShow(term)

url = "https://www.springfieldspringfield.co.uk{}".format(extension)

urlRequest = requests.get(url)
pageSoup = BeautifulSoup(urlRequest.text, "html.parser")

seasondivs = pageSoup.find_all('div', {'class':'season-episodes'})

#Episodes are listed on the main page seperated into divs based on the season they are in
for season in seasondivs:
    episodes = season.find_all('a', {'class':'season-episode-title'})
    for episode in episodes:
        extension = episode['href']
        #Gets the episode name in the format SXXEXX
        identifier = re.sub(r'^.*?(s[0-9]{2}e[0-9]{2})', r'\g<1>', extension)
        url = "https://www.springfieldspringfield.co.uk/" + extension
        f = open(identifier + ".txt", "wb")
        desc = getScript(url)
        seperatedDesc = desc.get_text(separator="\n")
        
        try:
            f.write(seperatedDesc.encode("utf-8"))
            print(identifier)
        except:
            print("Error with " + identifier)
        finally:
            f.close()