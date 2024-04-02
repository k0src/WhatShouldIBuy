import praw
from googleapiclient.discovery import build
import keys
import spacy
from spellchecker import SpellChecker
import re

API_KEY = keys.API_KEY
SEARCH_ENGINE_ID = keys.SEARCH_ENGINE_ID

# django html css - 
# image of product

# Prompt user for item and details
def prompt_user():
    item = input('What are you looking for? ')

    spell = SpellChecker()

    misspelled = spell.unknown(item.split())

    for word in misspelled:
        correction = spell.correction(word)
        item = item.replace(word, correction)

    details = input('Any specific specifications? ')

    spell = SpellChecker()

    misspelled = spell.unknown(details.split())

    for word in misspelled:
        correction = spell.correction(word)
        details = details.replace(word, correction)

    return item.lower().strip(), details.lower().strip()

# Use Reddit API to search reddit for item and details, and return top comments from 5 most relevant posts
def get_reddit_responses(item, details):
    subreddit_name = find_subreddit(item, details)

    reddit = praw.Reddit(client_id=keys.client_id, 
                         client_secret=keys.client_secret, 
                         user_agent='green fn')
    
    subreddit = reddit.subreddit(subreddit_name)
    query = f'{item} {details}'

    products = []

    for submission in subreddit.search(query, sort='best', time_filter='all'):
        if submission.num_comments <= 1:
            continue
        elif submission.num_comments > 1:
            for comment in submission.comments:
                if 'I am a bot, and this action was performed automatically.' in comment.body:
                    continue
                elif '[deleted]' in comment.body:
                    continue
                else:    
                    product = extract_products(comment.body)
                    if product.strip() and len(product.strip()) > 3:
                        index = product.find(']') 
                        product = product[:index]
                        products.append(product.strip())
                    else:
                        continue
                    if len(products) == 5:
                        break

        if len(products) == 5:
            break

    return products

# Use Google Custom Search API to find subreddit based on item and details
def find_subreddit(item, details):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=f"suggest a {item} {details} reddit", cx=SEARCH_ENGINE_ID).execute()

    if 'items' in res:
        first_result_url = res['items'][0]['link']
        if 'reddit.com' not in first_result_url:
            return None
        else:
            subreddit_name = first_result_url.split('/')[4]
        
        return subreddit_name
    else:
        return None
    
# Use Google Custom Search API to find store page based on product
def find_store_page(product):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=f"{product} buy", cx=SEARCH_ENGINE_ID).execute()

    if 'items' in res:
        first_result_url = res['items'][0]['link']
        return first_result_url
    else:
        return None
    
# Use spaCy to extract products from top comment
def extract_products(comment):
    product = ''

    nlp = spacy.load("en_core_web_trf")
    doc = nlp(comment)

    for entity in doc.ents:
        if entity.label_ == 'PRODUCT':
            product = entity.text

    return product

# Process responses
def process_responses(products):

    formatted_recommendations = []

    if products:
        for index, product in enumerate(products):
            formatted_recommendations.append(f'{index + 1}. {product}\nLink: {find_store_page(product)}')
    else:
        return None

    return formatted_recommendations

# Main function
def main():
    item, details = prompt_user()
    products = get_reddit_responses(item, details)
    recommendations = process_responses(products)

    if recommendations:
        print("According to the internet, you should buy:")
        for recommendation in recommendations:
            print(recommendation)
    else:
        print('No recommendations found.')

if __name__ == "__main__":
    main()