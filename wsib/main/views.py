from django.shortcuts import render
from django.http import JsonResponse
import json
from . import redditsearch

def index(request):
    return render(request, 'main/index.html')

def process_input(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        input_text = data.get('input_text', '')

        recommendations = redditsearch.main(input_text)
        # sample recommendations list - [{'name': 'Product 1', 'link': 'linktobuy.com', 'image_url': 'imageurl.com'}, {'name': 'Product 2', 'link': 'linktobuy.com', 'image_url': 'imageurl.com'}]
        return JsonResponse({'recommendations': recommendations})

    else:
        return JsonResponse({'error': 'Invalid request'})