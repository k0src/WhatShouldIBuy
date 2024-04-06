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
        # recommendations = [
        #     {
        #         'name': 'Zephyrus G1',
        #         'link': 'https://rog.asus.com/us/laptops/rog-zephyrus/rog-zephyrus-g14-series/',
        #         'image': 'https://m.media-amazon.com/images/I/81o-KqoMQyL._AC_UF894,1000_QL80_.jpg',
        #         'source_link': 'https://www.reddit.com/'
        #     },
        #     {
        #         'name': 'Surface Pro',
        #         'link': 'https://www.microsoft.com/en-us/d/surface-pro-9/93vkd8np4fvk',
        #         'image': 'https://cdn0.vox-cdn.com/hermano/verge/product/image/9694/bfarsace_211004_4777_0043_sq.jpg',
        #         'source_link': 'https://www.reddit.com/'
        #     },
        #     {
        #         'name': 'Acer Aspire 5 Slim',
        #         'link': 'https://www.amazon.com/Acer-Display-Graphics-Keyboard-A515-43-R19L/dp/B07RF1XD36',
        #         'image': 'https://m.media-amazon.com/images/I/71vvXGmdKWL.jpg',
        #         'source_link': 'https://www.reddit.com/'
        #     },
        #     {
        #         'name': 'Acer Aspire 3',
        #         'link': 'https://www.reddit.com/r/SuggestALaptop/comments/xgrb3t/are_acer_laptops_really_that_bad/',
        #         'image': 'https://www.pcworld.com/wp-content/uploads/2023/07/Acer_Aspire3-4.jpg?quality=50&strip=all',
        #         'source_link': 'https://www.reddit.com/'
        #     },
        #     {
        #         'name': 'Vivobook 1',
        #         'link': 'https://www.reddit.com/r/ASUS/comments/14qe0nv/would_you_recommend_buying_an_asus_laptop_in_2023/',
        #         'image': 'https://i5.walmartimages.com/seo/ASUS-VivoBook-Flip-14-Home-Business-2-in-1-Laptop-AMD-Ryzen-5-5500U-6-Core-14-0in-60Hz-Touch-Full-HD-1920x1080-AMD-Radeon-Win-11-Home-Travel-Work-Bac_82fa3af3-de4d-432f-8ef9-e596a5366b25.0ac86952103dea05751d927c9a80eaf0.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF',
        #         'source_link': 'https://www.reddit.com/'
        #     }
        # ]
        return JsonResponse({'recommendations': recommendations})

    else:
        return JsonResponse({'error': 'Invalid request'})