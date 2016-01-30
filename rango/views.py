from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserProfileForm, UserForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

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
    return render(request, 'rango/about.html', {})
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
        context_dict['category_name_slug'] = category_name_slug 
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print 'error' ,form.errors
    
    else:
        form = CategoryForm()
        
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug=None):
    print 'add_page', request, category_name_slug
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None
    #print 'cat', cat, '--cat.id', cat.id
    if request.method == 'POST':
        form = PageForm(request.POST)
        print 'form-- POST', form
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                #return category(request, category_name_slug)
                return HttpResponseRedirect(reverse('rango:category', args=(cat.slug,)))
            else:
                 form.save(commit=True)
                 return index(request)
        else:
            print 'error' ,form.errors
    
    else:
        print 'GET'
        if cat:
            form = PageForm(initial={'category': cat.id})
            #form.fields['category'].initial = cat.id
        else:
            form = PageForm()
    
    context_dict = {'form': form, 'category': cat}
    url = 'rango/add_page.html'
    return render(request, url , context_dict)

def register(request):
    registered = False
    print 'reg', request.method
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES('picture')
            profile.save()
            registered = True
        
        else:
            print 'user profile form errors', user_form.errors, profile_form.errors
    else:
        user_form=UserForm()
        profile_form = UserProfileForm()
    context = {'user_form': user_form, 'profile_form': profile_form,'registered': registered}
    print 'context', context
    return render(request, 'rango/register.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your rango account is disabled")
        else:
            print "Invalid login details"
            return HttpResponse("Invalid login details")
    else:
        return render(request, 'rango/login.html', {})
    
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this :D ")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')
    
    
        