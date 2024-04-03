# What Should I Buy?

This web application takes the work out of searching the internet for *real people's opinions.* Just input what you're looking for (i.e., laptop) and some specific specifications (i.e., for work and gaming), and **WSIB** will crawl Reddit for the most upvoted comments in threads from relevant subreddits! Then, it will return these results along with a convenient link to purchase.

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

*You will also need to supply your own API keys.*