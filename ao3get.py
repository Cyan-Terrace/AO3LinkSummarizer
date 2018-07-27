#!/usr/bin/env python3

from html.parser import HTMLParser
import requests, sys, time, os, urllib, re

class AO3Parser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.hitsDataHunting = False
        self.bookmarksDataHunting = False
        self.kudosDataHunting = False
        self.commentsDataHunting = False
        self.chaptersDataHunting = False
        self.wordsDataHunting = False
        self.publishedDataHunting = False
        
        self.fandomTagsHunting = False
        self.fandomDataHunting = False
        self.categoryTagsHunting = False
        self.categoryDataHunting = False
        self.ratingTagsHunting = False
        self.ratingDataHunting = False
        
        self.titleDataHunting = False
        self.authorDataHunting = False
        
    def handle_starttag(self, tag, attrs):
          
        if tag == "a":
            for attr in attrs:
                if attr == ("href", "/works/" + work_id + "/bookmarks"):
                    self.bookmarksDataHunting = True
                if attr == ("rel", "author"):
                    self.authorDataHunting = True
                    
            if self.fandomTagsHunting:
                for attr in attrs:
                    if attr[0] == "href":
                        self.fandomDataHunting = True
            if self.categoryTagsHunting:
                for attr in attrs:
                    if attr[0] == "href":
                        self.categoryDataHunting = True
            if self.ratingTagsHunting:
                for attr in attrs:
                    if attr[0] == "href":
                        self.ratingDataHunting = True        
                    
        if tag == "dd" or tag == "dt":
            self.fandomTagsHunting = False
            self.categoryTagsHunting = False
            self.ratingTagsHunting = False
                    
        if tag == "dd":
            for attr in attrs:
                if attr == ("class","hits"):
                    self.hitsDataHunting = True
                if attr == ("class", "kudos"):
                    self.kudosDataHunting = True
                if attr == ("class", "comments"):
                    self.commentsDataHunting = True
                if attr == ("class", "chapters"):
                    self.chaptersDataHunting = True
                if attr == ("class", "words"):
                    self.wordsDataHunting = True
                if attr == ("class", "published"):
                    self.publishedDataHunting = True
                    
                if attr == ("class", "fandom tags"):
                    self.fandomTagsHunting = True
                if attr == ("class", "category tags"):
                    self.categoryTagsHunting = True
                if attr == ("class", "rating tags"):
                    self.ratingTagsHunting = True
                    
        if tag == "h2":
            for attr in attrs:
                if attr == ("class","title heading"):
                    self.titleDataHunting = True
                    
    def handle_data(self, data):
    
        global title, author, rating, category, fandom, published, words, chapters, comments, bookmarks, kudos, hits
        data = data.replace("\n", "").strip()
    
        if self.hitsDataHunting:
            hits = data
            self.hitsDataHunting = False
        if self.kudosDataHunting:
            kudos = data
            self.kudosDataHunting = False
        if self.bookmarksDataHunting:
            bookmarks = data
            self.bookmarksDataHunting = False    
        if self.commentsDataHunting:
            comments = data
            self.commentsDataHunting = False    
        if self.chaptersDataHunting:
            chapters = data
            self.chaptersDataHunting = False    
        if self.wordsDataHunting:
            words = data
            self.wordsDataHunting = False    
        if self.publishedDataHunting:
            published = data
            self.publishedDataHunting = False
            
        if self.fandomDataHunting:
            fandom.append(data)
            self.fandomDataHunting = False
        if self.categoryDataHunting:
            category = data
            self.categoryDataHunting = False
        if self.ratingDataHunting:
            if "General" in data:
                rating = "G"
            elif "Teen" in data:
                rating = "T"
            elif "Mature" in data:
                rating = "M"
            elif "Explicit" in data:
                rating = "E"    
                
            self.ratingDataHunting = False
            
        if self.titleDataHunting:
            title = data
            self.titleDataHunting = False
        if self.authorDataHunting:
            author = data
            self.authorDataHunting = False
            
#################
#################

def main(arg):

    global fandom, title, author, rating, category, published, words, chapters, comments, bookmarks, kudos, hits, work_id
    title, author, rating, category, published, words, chapters, comments, bookmarks, kudos, hits = "?", "?", "?", "?", "?", "0", "0", "0", "0", "0", "0"
    fandom = []
    sass = ""

    headers = {"user-agent" : "ao3get/0.0.3"}

    if(arg.find("archiveofourown.org/works/") > 0):
        url = arg

    verbose = False

    for arg in sys.argv:
        if arg in ("-h", "--help", "?"):
            print ("ao3get Usage:\n NYI")
            sys.exit("\n---End of help---")
            
        if arg in ("v", "verbose", "!"):
            verbose = True
            print("Verbose Mode Enabled")   
            
        if "/works/" in arg:
            url = arg
            
    if verbose:
        def vprint(*args):
            print(args)
    else:
        vprint = lambda *a : None    
        
        
    url = url.lower()
        
    if "archiveofourown.org/works/" not in url:
        sys.exit("Invalid url.")

    id_start = url.find("/works/") + 7
    values = re.findall(r'\d+', url[id_start:])
    if len(values) == 0:
        sys.exit("Invalid url.")
    work_id = values[0]
    
    print("Work ID: ", work_id)

    parser = AO3Parser()
    vprint("Using AO3 Parser")

    print("Requesting ", url, "...")
    page = requests.get(url, headers = headers)
    print("Request Status: ", page.status_code, "\t\tResponse Length: ", len(page.text))
    mainText = page.text
    parser.feed(mainText)

    if(verbose):
        with open(os.path.expanduser('~/Workspace/AO3Thingy/') + "output.txt", "wb") as text_file:
            text_file.write((page.text).encode('utf-8'))

    s = '&nbsp;&nbsp;&nbsp;'

    fandomsItalicized = "*" + fandom[0] + "*"
    if len(fandom) == 2:
        fandomsItalicized += " and *" + fandom[1] + "*"
    if len(fandom) > 2:
        fandomsItalicized += ", *" + fandom[1] + "*, and *" + str(len(fandom) - 2) + "* more"
        sass = " Yeah, I use the serial comma.  Fite me."

    output = "**" + title + "** by *" + author + "* - Rating: *" + rating + "* - Fandom: " + fandomsItalicized + "\n\nCategory: *" + category + "*" + s + " Published: *" + published + "*" + s + "Words: *" + words + "* " + s + "Chapters: *" + chapters + "* " + s + "Bookmarks: *" + bookmarks + "* " + s + "Kudos: *" + kudos + "* " + s + "Hits: *" + hits + "*\n\n ^(I am a bot.  PM me feedback." + sass + ")"

    vprint(output)
    vprint("ao3get Done")
    return output

if __name__ == "__main__":
    main(sys.argv)

