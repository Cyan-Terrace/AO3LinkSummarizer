#!/usr/bin/env python3

import ao3get
import praw
import pdb
from html.parser import HTMLParser
import requests, sys, time, os, urllib, re

def getao3(url):
    return (ao3get.main(url))

reddit = praw.Reddit('bot1')
subreddit_name = "testingground4bots"
subreddit = reddit.subreddit(subreddit_name)

if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []
else:
    with open("comments_replied_to.txt", "r") as f:
        comments_replied_to = f.read().split("\n")
        comments_replied_to = list(filter(None, comments_replied_to))

print("Comments previously replied to: ", comments_replied_to)    

fake_comments = ["[blah!](https://archiveofourown.org/works/5154329)", "[oh](https://aarchiveofourown.org/works/15029351 okay?)"]

fake_comments = ["https://aarchiveofourown.org/works/15029351"
                ,"https://archiveofourown.org/works/15095525" #4 fandoms
                ,"https://archiveofourown.org/works/12755589"   #2 fandoms
                ,"https://archiveofourown.org/works/15367428"  #~19 fandoms?
                ,"https://archiveofourown.org/works/15280989"]  #3 fandoms
#    "https://archiveofourown.org/works/15443910"  #rating T, lots of categories PASS
#   "https://archiveofourown.org/works/15445515" # rating M PASS
#    "https://archiveofourown.org/works/15005774/chapters/34780388"    #rating g PASS
#   "https://archiveofourown.org/works/11064036/chapters/24671691" #rating e PASS]

print("Watching subreddit '" + subreddit_name + "' stream for new comments")
for comment in subreddit.stream.comments():
#for comment in fake_comments:   #ALTERNATE
    text = comment.body
    #text = comment #ALTERNATE
    if re.search("archiveofourown.org/works/", text, re.IGNORECASE) and comment.id not in comments_replied_to: 
    #if re.search("archiveofourown.org/works/", text, re.IGNORECASE): #ALTERNATE
        
        idStart = text.find("archiveofourown.org/works/") + 26
        idLength = text[idStart:].find(")")
        
        values = re.findall(r'\d+', text[idStart:])
        
        if len(values) == 0:
            sys.exit("Invalid link.")
        
        url = "https://archiveofourown.org/works/" + values[0] + "?view_adult=true"
        
        print("Found AO3 works link:", url, "\t\tSending to ao3get...")
        
        reply = getao3(url)
        
        #######
        
        comment.reply(reply)
        comments_replied_to.append(comment.id)
        with open("comments_replied_to.txt", "w") as f:
            for comment_id in comments_replied_to:
                f.write(comment_id + "\n")
               
        #######
        
        print("Replied to (" + comment.body[:100].replace("\n", " ") + ") with (" + reply.replace("\n", " ") + ") \n================\n")
        #print("Replied to (OFFLINE) with (" + reply + ")\n================\n")  #ALTERNATE
        
print("ao3bot done")

