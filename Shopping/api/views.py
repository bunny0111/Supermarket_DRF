from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item
from .serlializers import ItemSerializers

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_items' : '/',
        'Search by Category' : '/?category=category_name',
        'Search by Subcategory' : '/?subcategory=category_name',
        'Add' : '/create',
        'Update' : '/update/pk',
        'Delete' : '/item/pk/delete'
    }
    return Response(api_urls)

'''
In the above code, the api_view decorator takes a list of HTTP methods that a views should response to. Other methods will response with the Method Not Allowed.
'''