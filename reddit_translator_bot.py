# -*- coding: utf-8 -*-
"""
https://pypi.org/project/langdetect/
https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
https://pypi.org/project/googletrans/

Supported languages:
af, ar, bg, bn, ca, cs, cy, da, de, el, en, es, et, fa, fi, fr, gu, he,
hi, hr, hu, id, it, ja, kn, ko, lt, lv, mk, ml, mr, ne, nl, no, pa, pl,
pt, ro, ru, sk, sl, so, sq, sv, sw, ta, te, th, tl, tr, uk, ur, vi, zh-cn, zh-tw

"""

import praw
import re
from langdetect import detect
from googletrans import Translator
import sys
import time
from datetime import datetime
import json

def comment_vs_submission(input):
    if re.search("comment", type(input).__name__, re.IGNORECASE):
        print("comment")
        return "comment"
    else:
        print("submission")
        return "submission"

bot = praw.Reddit(user_agent='translator_bot v0.1',
                  client_id='db49X2FVKkd_Aw',
                  client_secret='PYnBy5UnWj3hKx0EgciCAHpECLc',  
                  )

subreddit = bot.subreddit('scriptBotTesting')
translator = Translator()
log_file_list = []

start_time = time.time()

# for comment in subreddit.stream.comments(skip_existing=True):
for comment in subreddit.stream.comments():
    
    
    if re.search("DeleteTranslation!", comment.body, re.IGNORECASE):
        # comment = reddit.comment(id='dj0bw7q') # assume this comment shows up in your inbox
        parent = comment.parent()  # the comment made by your bot
        grandparent = parent.parent()  # the comment that first triggered the bot
        if comment.author == grandparent.author:  # checks if the person is the one you care about
            if parent.author == "_data_mining_bot_":
                
                # parent.delete()
          
        print("Success!")
        
    #     sys.exit()
        
        
    # format is ("TranslateThis! language)
    if re.search("TranslateThis!", comment.body, re.IGNORECASE):
        
        needing_translation = comment.parent()
        comment_as_list = comment.body.split()
        
        type_of_parent = comment_vs_submission(needing_translation)
        
        if type_of_parent == "comment":
           parent = bot.comment(needing_translation)
           language_of_text = detect(parent.body)
           translation = translator.translate(parent.body, dest=comment_as_list[1])
        else:
            parent = bot.submission(needing_translation)
            language_of_text = detect(parent.title)
            translation = translator.translate(parent.title, dest=comment_as_list[1])

        
        print("Language of the text: ", language_of_text)
        print("Language to be translated into: ", comment_as_list[1])
        print("Input: ", translation.origin)
        print("Output: ", translation.text)
        now = str(datetime.now())
        entry_list = []
        entry_list.append(now)
        entry_list.append(language_of_text)
        entry_list.append(comment_as_list[1])
        entry_list.append(translation.origin)
        entry_list.append(translation.text)
        
        log_file_list.append(entry_list)
        
        
        # comment.reply("Translation: " + translation.text + 
        #               "\n\nThis is a language translation bot powered by [Google Translate](translate.google.com)"+
        #               "Find the code [here]()")
        
        # sys.exit()
        
    end_time = time.time() - start_time
    print(end_time)
    print()
    if end_time > 1.5:
        break
    
with open("log.txt", "a+", encoding='utf-8') as f:
    # f.write(str(log_file_list) + "\n")
    for listitem in log_file_list:
        f.write('%s\n' % listitem)
        