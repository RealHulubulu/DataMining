# -*- coding: utf-8 -*-
"""
This is code that counts all of the normal words found within a subreddit. Yes, all of them. I 
have not removed filler words yet. Each run creates a log file that keeps track of the start and
end times for each run. It also creates a csv file with all of the counts. Each run adds the counts
from the previous run.
"""

import praw
import pdb
import re
import os
import time
import sys
from string import ascii_letters, digits
from operator import itemgetter
from datetime import datetime


def special_match(strg, search=re.compile(r'[^a-zA-Z]').search):
    return not bool(search(strg))

# print(special_match("Discord**](https://discord.gg/Rainbow6"))

#%%

if not os.path.isfile("log.txt"):
    with open("log.txt", "a") as f:
        f.write("StartEnd, EndTime\n")

now = str(datetime.now())
with open("log.txt", "a") as f:
    f.write("\n" + now)
    

bot = praw.Reddit(user_agent='mine_post_data v0.1',
                  client_id='db49X2FVKkd_Aw',
                  client_secret='PYnBy5UnWj3hKx0EgciCAHpECLc',
                   username='_data_mining_bot_',
                  )

subreddit = bot.subreddit('all')
how_long_to_count = 8
the_big_string = ""
wordfreq = []
posts_read = []
comments_read = []

if not os.path.isfile("words_in_reddit.txt"):
    words_in_reddit = []   
else:
    with open("words_in_reddit.txt", "r") as f:
        words_in_reddit = f.read()
        words_in_reddit = words_in_reddit.split("\n")
        # print(len(words_in_reddit))
        words_in_reddit = list(filter(None, words_in_reddit))
        # print(len(words_in_reddit))

        posts_read = (words_in_reddit[0])
        comments_read = (words_in_reddit[1])
        
        
        for i in range(len(words_in_reddit)-2):
            words_in_reddit[i+2] = words_in_reddit[i+2].replace("(", "").replace(")", "").replace("'", "").split(",")        
    
        posts_read = posts_read.replace("[", "").replace("]", "").replace("'", "").split(",")
      
        comments_read = comments_read.replace("[", "").replace("]", "").replace("'", "").split(",")
        
        
        words_in_reddit.pop(0)
        words_in_reddit.pop(0)
    
        
        # sys.exit()
        
       
       
# subreddit = bot.subreddit('learnpython')
# subreddit = bot.subreddit('all')

submissions = subreddit.stream.submissions(skip_existing=True) #pulls last 100
comments = subreddit.stream.comments(skip_existing=True) #pulls last 100

start_time = time.time()


# for submission, comment in zip(subreddit.hot(limit=100), subreddit.comments(limit=100)):
for submission, comment in zip(submissions, comments):
    if submission.id not in posts_read:
        
        the_big_string = the_big_string + submission.title
        posts_read.append(submission.id)
        
    if comment.id not in comments_read:
        
        the_big_string = the_big_string + comment.body
        comments_read.append(comment.id)
    
    end_time = time.time() - start_time
    if end_time > how_long_to_count:
        break    

wordlist = the_big_string.split()
for word in wordlist:
    wordfreq.append(wordlist.count(word))

pairs = list(zip(wordlist, wordfreq))


print()

print(pairs[0])
print(pairs[0][0])

for char in pairs[0][0]:
    print(char)


   
new_pairs_list = []
     
for item in pairs:
    if special_match(item[0]) == True:
        new_pairs_list.append(item)
  
new_pairs_list = set(new_pairs_list)
new_pairs_list = list(new_pairs_list)



words_in_reddit_dict = {}
for entry in words_in_reddit:
    key, value = entry[0], entry[1]
    words_in_reddit_dict[key] = int(value)
# print(words_in_reddit_dict)
    

words_in_reddit_dict2 = {}
for entry in new_pairs_list:
    key, value = entry[0], entry[1]
    words_in_reddit_dict2[key] = int(value)
print(words_in_reddit_dict2)

print()
print()
    
for key in words_in_reddit_dict: #old one
    if key in words_in_reddit_dict2:
        words_in_reddit_dict2[key] = int(words_in_reddit_dict2[key]) + int(words_in_reddit_dict[key])
    else:
        words_in_reddit_dict2[key] = int(words_in_reddit_dict[key])
print(words_in_reddit_dict2)


sorted_final = {k: v for k, v in sorted(words_in_reddit_dict2.items(), key=lambda item: item[1], reverse=True)}


    
# Write our updated list back to the file
with open("words_in_reddit.txt", "w") as f:
    f.write(str(posts_read))
    f.write("\n")
    f.write(str(comments_read))
    f.write("\n")
    for word_count in sorted_final:
        f.write(str(word_count) + "," + str(sorted_final[word_count]))
        f.write("\n")
        
now = str(datetime.now())
with open("log.txt", "a") as f:
    f.write(", " + now)


 