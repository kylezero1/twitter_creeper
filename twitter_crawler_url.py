import requests
import lxml
import json
import sys
from bs4 import BeautifulSoup

if __name__ == '__main__':

    tweetNumber = 0

    file_name = str(sys.argv[1]) #gets file_name input from cmd

    jsonFile = open(file_name, 'r')    
    data = json.load(jsonFile)
    jsonFile.close()

    totalTweets = len(data)
    while tweetNumber < totalTweets:
        if ('delete' in data[tweetNumber] 
        or 'entities' not in data[tweetNumber] 
        or len(data[tweetNumber]['entities']['urls'])==0):
            print("Tweet " + str(tweetNumber) + " does not contain a URL")
            tweetNumber += 1
        else:
            if 'expanded_url' in data[tweetNumber]['entities']['urls'][0]: #expanded_url exists in tweet                
                print("Tweet #" + str(tweetNumber) + ": " + data[tweetNumber]['entities']['urls'][0]['expanded_url'])
                url = data[tweetNumber]['entities']['urls'][0]['expanded_url']
                
                try:
                    r = requests.get(url)
                except BaseException as e:
                    print("Error requesting url: %s" % str(e))
                    
                html_content = r.text

                soup = BeautifulSoup(html_content, 'lxml')
                try:
                    title = soup.title.string
                except BaseException as e:
                    print("Error soup title: %s" % str(e))
                #print(soup.title.string)

                with open(file_name, 'w') as outfile:
                    #data[0].append({'test':'123'})
                    data[tweetNumber]['title'] = title #adds title field to tweets with urls
                    #need to fix unicode in title
                    json.dump(data, outfile, indent=4)
                    outfile.close()

                tweetNumber += 1
            else: #not necessary
                print("Tweet " + str(tweetNumber) + " does not contain a URL")
                tweetNumber += 1
    
    
    #else: #expanded_url does not exist in tweet