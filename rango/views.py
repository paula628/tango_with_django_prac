from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rango.models import Category, Page

def index(request):
    # -- <WSGIRequest: GET '/rango/'>
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict={'categories': category_list}
    
    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list
    for category in category_list:
        category.url = category.name.replace(' ', '_')
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request, 'rango/about.html')
    
    #return HttpResponse("Rango says here is the about page <br/> back to <a href=/rango/>Home</a>")
    
def category(request, category_name_slug):
    context_dict={}
    print'cc', category_name_slug
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        
        context_dict['category'] = category 
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)