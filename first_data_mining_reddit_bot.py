# -*- coding: utf-8 -*-
"""
This is code to count the number of words in a subreddit. The inputs are the subreddit, word to count,
and duration of counting. It counts the number of times the word is found in both submissions and 
comments.
"""

    
import praw
import pdb
import re
import os
import time

bot = praw.Reddit(user_agent='mine_post_data v0.1',
                  client_id='db49X2FVKkd_Aw',
                  client_secret='PYnBy5UnWj3hKx0EgciCAHpECLc',
                   username='_data_mining_bot_',
                  )

# these are the inputs
subreddit = bot.subreddit('all')
word_to_count = "python"
how_long_to_count = 180


count_python_submissions = 0
count_python_comments = 0

if not os.path.isfile("posts_read.txt"):
    posts_read = []   
else:
    with open("posts_read.txt", "r") as f:
       posts_read = f.read()
       posts_read = posts_read.split("\n")
       posts_read = list(filter(None, posts_read))
       count_python_submissions = posts_read[0]
       print(count_python_submissions)
       
if not os.path.isfile("comments_read.txt"):
    comments_read = []   
else:
    with open("comments_read.txt", "r") as f:
       comments_read = f.read()
       comments_read = comments_read.split("\n")
       comments_read = list(filter(None, comments_read))
       count_python_comments = comments_read[0]
       print(count_python_comments)
       
# subreddit = bot.subreddit('learnpython')
# subreddit = bot.subreddit('all')

submissions = subreddit.stream.submissions(skip_existing=True) #pulls last 100
comments = subreddit.stream.comments(skip_existing=True) #pulls last 100

start_time = time.time()

for submission, comment in zip(submissions, comments):
    if submission.id not in posts_read:
        if re.search(word_to_count, submission.title, re.IGNORECASE):
            print("\nnew submission with python: ", submission.title)
            
            wordlist = submission.title.split
            for word in wordlist:
                if word.lower() == word_to_count:
                    count_python_submissions += 1
                    
            posts_read.append(submission.id)
            # count_python_submissions += 1
    if comment.id not in comments_read:
        if re.search(word_to_count, comment.body, re.IGNORECASE):  
            print("\nnew comment with python: ", comment.body)
            
            wordlist = comment.body.split
            for word in wordlist:
                if word.lower() == word_to_count:
                    count_python_comments += 1
            
            comments_read.append(comment.id)
    end_time = time.time() - start_time
    if end_time > how_long_to_count:
        break    
        
# comments = subreddit.stream.comments() #pulls last 100
# comments = subreddit.stream.comments(skip_existing=True)
# for comment in comments:
#     text = comment.body
#     author = comment.author
#     print(author, text)


        
# Write our updated list back to the file
with open("posts_read.txt", "w") as f:
    f.write(str(count_python_submissions) + "\n")
    for post_id in posts_read:
        f.write(post_id + "\n")
        
with open("comments_read.txt", "w") as f:
    f.write(str(count_python_comments) + "\n")
    for comment_id in comments_read:
        f.write(comment_id + "\n")        
        
print(count_python_comments + count_python_submissions)        
        
