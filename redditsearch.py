import praw
from googleapiclient.discovery import build
import keys
import spacy
from spellchecker import SpellChecker

API_KEY = keys.API_KEY
SEARCH_ENGINE_ID = keys.SEARCH_ENGINE_ID

# Using spaCy's Entity Recognition to identify products
# butttt - it kinda sucks ass
# throws out a lot of products
# ['Zephyrus G14', '', 'The', '', 'Vivobook 14'] Lol
# i either have to find a way to make it better or just return the comment idek
# can just google the product and use thta to get link

# todo - fix thing or just do comment
# buy link
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

    responses = []

    for submission in subreddit.search(query, sort='relevance', time_filter='month'):
        if submission.num_comments > 1:
            if 'I am a bot, and this action was performed automatically.' in submission.comments[0].body:
                top_comment = submission.comments[1].body

                responses.append(extract_products(top_comment))
            else:    
                top_comment = submission.comments[0].body

                responses.append(extract_products(top_comment))
            
            if len(responses) == 5:
                break

    return responses

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
    
# Use spaCy to extract products from top comment
def extract_products(top_comment):
    products = ''

    nlp = spacy.load("en_core_web_trf")
    doc = nlp(top_comment)

    for entity in doc.ents:
        if entity.label_ == 'PRODUCT':
            products = entity.text
            break

    return products
# main
def main():
    item, details = prompt_user()
    responses = get_reddit_responses(item, details)

    print(responses) # Test

    filtered_responses = []

    if responses:
        for response in responses:
            if len(response.strip()) >= 3:
                filtered_responses.append(response)
    else:
        print('No recommendations found.')

    if filtered_responses:
        print("According to the internet, you should buy:")
        for index, response in enumerate(filtered_responses):
            print(f'{index + 1}. {response}')
    else:
        print('No recommendations found.')

if __name__ == "__main__":
    main()