from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item
from .serlializers import ItemSerializers
from rest_framework import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404

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

@api_view(['POST'])
def add_items(request):
    item = ItemSerializers(data=request.data)

    # validating for already existing data
    if Item.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data is already exist.')
    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def view_items(request):
    #checking for the parameters from the URL
    if request.query_params:
        items = Item.objects.filter(**request.query_params.dict())
    else:
        items = Item.objects.all()

    # if there is something in items else raise error
    if items:
        serializers = ItemSerializers(items, many=True)
        return Response(serializers.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def update_view(request, pk):
    item = Item.objects.get(pk=pk)
    data = ItemSerializers(instance=item, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
def delete_items(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)