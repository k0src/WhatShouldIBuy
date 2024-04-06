# What Should I Buy?

This web application takes the work out of searching the internet for *real people's opinions.* Just input what you're looking for (i.e., laptop) and some specific specifications (i.e., for work and gaming), and **WSIB** will crawl Reddit for the most upvoted comments in threads from relevant subreddits! Then, it will return these results along with a convenient link to purchase.

*NPL isn't always accurate - and can slow down the process a lot.*

![img1](https://i.ibb.co/JcjCG2R/1.png)
![img2](https://i.ibb.co/0MT26Mq/2.png)
![img3](https://i.ibb.co/HqYgVCc/3.png)

*You can build the website, visit the URL here, or use the [standalone scripts](https://github.com/k0src/WhatShouldIBuy/tree/master/standalone%20scripts)*

### Required Packages:

**Reddit API:**

```pip3 install praw```

**Google Search API**

```pip3 install google-api-python-client```

**spaCy NLP**

```pip3 install -U pip setuptools wheel```

```pip3 install -U spacy```

```python3 -m spacy download en_core_web_trf```

**Spellchecker**

```pip3 install pyspellchecker```