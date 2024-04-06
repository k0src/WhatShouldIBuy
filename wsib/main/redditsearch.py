import praw
from googleapiclient.discovery import build
from . import keys
import spacy
from spellchecker import SpellChecker

API_KEY = keys.API_KEY
SEARCH_ENGINE_ID = keys.SEARCH_ENGINE_ID

# Use Reddit API to search reddit for item and details, and return top comments from 5 most relevant posts
def get_reddit_responses(input_text):
    subreddit_name = find_subreddit(input_text)

    reddit = praw.Reddit(client_id=keys.client_id, 
                         client_secret=keys.client_secret, 
                         user_agent='reddit_search')
    
    subreddit = reddit.subreddit(subreddit_name)
    query = input_text

    products = []
    source_links = []

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
                        source_links.append(f'https://www.reddit.com/{comment.permalink}')
                    else:
                        continue
                    if len(products) == 5:
                        break

        if len(products) == 5:
            break

    return products, source_links

# Use Google Custom Search API to find subreddit based on item and details
def find_subreddit(input_text):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=f"suggest a {input_text} reddit", cx=SEARCH_ENGINE_ID).execute()

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
def find_store_page(product, input_text):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=f"{product} {input_text} buy", cx=SEARCH_ENGINE_ID).execute()

    if 'items' in res:
        first_result_url = res['items'][0]['link']
        return first_result_url
    else:
        return None

# Use Google Custom Search API to find image of product
def find_product_image(product, input_text):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=f'{product} {input_text}', cx=SEARCH_ENGINE_ID, searchType='image').execute()
    if 'items' in res:
        first_image_link = res['items'][0]['link']
        return first_image_link
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
            break

    return product

# Process responses
def process_responses(products, input_text, source_links):
    recommendations = []

    if products:
        for product, source_link in zip(products, source_links):
            link = find_store_page(product, input_text)
            image = find_product_image(product, input_text)
            
            product_dict = {
                'name': product,
                'link': link,
                'image': image,
                'source_link': source_link
            }
            
            recommendations.append(product_dict)
    else:
        return None

    return recommendations

# Main function
def main(input_text):
    spell = SpellChecker()

    misspelled = spell.unknown(input_text.split())

    for word in misspelled:
        correction = spell.correction(word)
        input_text = input_text.replace(word, correction)

    products, source_links = get_reddit_responses(input_text)
    recommendations = process_responses(products, input_text, source_links)

    if recommendations:
        return recommendations
    else:
        return ['No recommendations found.']

if __name__ == "__main__":
    main()