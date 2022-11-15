#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy
import pandas
from wordcloud import WordCloud 
from textblob import TextBlob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt


# In[2]:


# twitter 
consumerKey="kFPXK0r7giQHgbhPMPmERxAIT"
consumerKeySecret="qwb2stpK4LaiCiQUg2Dp7cSSs2grcWHLT6vBEkadUc4T6D5Zn9"
accessToken="1545733425616760833-96L9ethh7Tq1uxaeXG9uwnfwfxzk3M"
accessTokenSecret="qzgQQCMhHoWjHw08UlNHmFGuSXHLFUrlkOkB8CwWYTOZc"


# In[3]:


# twitter 
auth=tweepy.OAuthHandler(consumerKey,consumerKeySecret)

auth.set_access_token(accessToken,accessTokenSecret)

api=tweepy.API(auth,wait_on_rate_limit=True)


# In[4]:


# twitter
searchKey=input("Enter twitter search: ")
print(searchKey)
n=int(input("Enter no of searches: "))
print(n) 
posts=api.user_timeline(screen_name=searchKey,count=n,tweet_mode="extended")
i=1
for tweet in posts[0:n]:
    print(str(i)+tweet.full_text+'\n')
    i=i+1


# In[40]:


df=pd.DataFrame([tweet.full_text for tweet in posts],columns=['tweets'])


# In[41]:


def cleanTxt(text):
    text=re.sub(r'@[A-Za-z0-9]+','',text)
    text=re.sub(r'#','',text)
    text=re.sub(r'RT[\s]+','',text)
    text=re.sub(r'https?:\/\/\S+','',text)
    return text 


# In[42]:


# Clean Data
df['tweets']=df['tweets'].apply(cleanTxt)
df


# In[43]:


# polarity ,subjectivity,analysis
def getPolarity(text):
    return TextBlob(text).sentiment.polarity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity
def getresult(res):
    if res<0:
        return 'Negative'
    elif res==0:
        return 'Neutral'
    else:
        return 'Positive'

df['subjectivity']=df['tweets'].apply(getSubjectivity)
df['Analysis']=df['polarity'].apply(getresult)

df


# In[44]:


# plot polarity and subjectivity to analyse sentiments
plt.figure(figsize=(5,5))
for i in range(0,df.shape[0]):
    plt.scatter(df['polarity'][i],df['subjectivity'][i],color='Red')
    
plt.title('Sentiment')
plt.xlabel('polarity')
plt.ylabel('subjectivity')
plt.show()


# In[45]:


words=' '.join([tweet for tweet in df['tweets']])
wordcloud=WordCloud(width=500,height=500,random_state=20,max_font_size=120).generate(words)
plt.imshow(wordcloud,interpolation="bilinear")
plt.axis('off')
plt.show()


# In[46]:


#positive tweets
j=1
sortedframe=df.sort_values(by=['polarity'])
for i in range(0,sortedframe.shape[0]): 
    if(sortedframe['Analysis'][i]=='Positive'):
        print(str(j)+': '+sortedframe['tweets'][i]+'\n')
    j=j+1
    


# In[47]:


#negative tweets
j=1
sortedframe=df.sort_values(by=['polarity'],ascending=False)
for i in range(0,sortedframe.shape[0]): 
    if(sortedframe['Analysis'][i]=='Negative'):
        print(str(j)+': '+sortedframe['tweets'][i]+'\n')
    j=j+1


# In[35]:


# 


# In[ ]:


dt = dt.replace('#','', regex=True)

