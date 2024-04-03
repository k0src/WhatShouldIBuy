from django.shortcuts import render
from django.http import JsonResponse
import json

def index(request):
    return render(request, 'main/index.html')

def process_input(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        input_text = data.get('input_text', '')

        processed_text = input_text + 'YES'

        return JsonResponse({'processed_text': processed_text})
    else:
        return JsonResponse({'error': 'Invalid request'})