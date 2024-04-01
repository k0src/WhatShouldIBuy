import praw
from googleapiclient.discovery import build
import keys

API_KEY = keys.API_KEY
SEARCH_ENGINE_ID = keys.SEARCH_ENGINE_ID

# use ai to find item name from comments LOOOL IDK HOW TO DO THIS


# Prompt user for item and details
def prompt_user():
    item = input('What are you looking for? ')
    details = input('Any specific specifications? ')
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
        if submission.num_comments > 0:
            top_comment = submission.comments[0].body
            responses.append(top_comment)
            
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

        print(first_result_url)
        print(subreddit_name)
        return subreddit_name
    else:
        return None
    
# main
def main():
    item, details = prompt_user()
    responses = get_reddit_responses(item, details)

    if responses:
        print("According to the internet, you should buy:")
        for response in responses:
            print(f"{responses.index(response)}. {response}")

    else:
        print("No recommendations found.")

if __name__ == "__main__":
    main()