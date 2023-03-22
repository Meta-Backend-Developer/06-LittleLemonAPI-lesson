from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_csv.renderers import CSVRenderer
from rest_framework_yaml.renderers import YAMLRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer, BrowsableAPIRenderer, JSONRenderer
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer


class MenuItemsViewset(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price','inventory']
    search_fields = ['title','category__title']


@api_view(['Get','POST'])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer, CSVRenderer, YAMLRenderer])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price=to_price)
        if search:
            items = items.filter(title__icontains=search)        
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []

        serialized_item = MenuItemSerializer(items, many=True, context={'request': request})
        return Response(serialized_item.data)
    
    if request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data, context={'request': request})
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)

@api_view()
def single_item(request, pk):
    item = get_object_or_404(MenuItem, id=pk)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)

@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)

@api_view()
@renderer_classes([TemplateHTMLRenderer])
def menu(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemSerializer(items, many=True)
    return Response({'data':serialized_item.data}, template_name='menu-items.html')

@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def welcome(request):
    data = '<html><body><h1>Welcome To Little Lemon API Project</h1></body></html>'
    return Response(data)

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"Some secret message"})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message":"Only Manager Should See This"})
    else:
        return Response({"message":"You are not authorized"},403)
