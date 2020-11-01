
# coding: utf-8

# # Data used is from a site that holds data on a 10K race that took place in Hillsboro, OR on June 2017

# In[39]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import lxml
import bs4

from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "http://www.hubertiming.com/results/2017GPTR10K"
html = urlopen(url)



# In[40]:


soup = BeautifulSoup(html, 'html.parser')
type(soup)


# In[41]:


title = soup.title
print(title)


# In[43]:


'''
printing out the text to look at the data 
'''
text = soup.get_text()
print(soup.text)


# In[44]:


soup.find_all('a')


# In[45]:


all_links = soup.find_all("a")
for link in all_links:
    print(link.get("href"))


# In[46]:


rows = soup.find_all('tr')
print(rows[:10])


# In[47]:


for row in rows:
    row_td = row.find_all('td')
print(row_td)
type(row_td)


# In[50]:


'''
Cleaning the data so its readable 
'''
str_cells = str(row_td)
cleantext = BeautifulSoup(str_cells, 'html.parser').get_text()
print(cleantext)


# In[52]:


import re

list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)
print(clean2)
type(clean2)


# # Starting to do more cleaning here 

# In[53]:


'''
Cleaning data and making it look pretty in dataframes.
'''
df = pd.DataFrame(list_rows)
df.head(10)


# In[54]:


df1 = df[0].str.split(',', expand=True)
df1.head(10)


# In[56]:


df1[0] = df1[0].str.strip('[')
df1.head(10)


# In[60]:


col_labels = soup.find_all('th')

all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, 'html.parser').get_text()
all_header.append(cleantext2)
print(all_header)


# In[61]:


df2 = pd.DataFrame(all_header)
df2.head()


# In[62]:


df3 = df2[0].str.split(',', expand=True)
df3.head()


# In[63]:


'''
Merging the two dataframes with concat
'''
frames = [df3, df1]

df4 = pd.concat(frames)
df4.head(10)


# In[64]:


df5 = df4.rename(columns=df4.iloc[0])
df5.head()


# In[65]:


df5.info()
df5.shape


# In[67]:


df6 = df5.dropna(axis=0, how='any')

df7 = df6.drop(df6.index[0])
df7.head()


# In[68]:


df5.info()
df5.shape


# In[69]:


df6 = df5.dropna(axis=0, how='any')

df7 = df6.drop(df6.index[0])
df7.head()


# In[70]:


'''
Doing some more cleaning renaming '[Place' and ' Team]' columns.
Also removing the closing bracket for cells in the "Team" column
'''
df7.rename(columns={'[Place': 'Place'},inplace=True)
df7.rename(columns={' Team]': 'Team'},inplace=True)
df7.head()


# In[71]:


df7['Team'] = df7['Team'].str.strip(']')
df7.head()

