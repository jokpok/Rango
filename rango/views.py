# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from datetime import datetime

from rango.bing_search import run_query
from rango.models import Category, Page, UserProfile

from rango.forms import CategoryForm, PageForm, ContactForm, ContactFormAgent, UserForm, UserProfileForm

def index(request):
    
    #version 1:
    #t = loader.get_template('rango/index.html')
    #c = RequestContext(request, {'boldmessage':'DANCE!'})
    #response = t.render(c)
    #return HttpResponse(response)
    #version2:
    #return render(request, 'rango/index.html', {'boldmessage':'DANCE!'})
    #version3:
    #return render_to_response(template_name ='rango/index.html', dictionary= {'boldmessage':'DANCE!'}, context_instance=RequestContext(request))
    context = RequestContext(request)
    cat_list = get_category_list()
    
    category_list=Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {'categories': category_list}
    context_dict['pages'] = page_list
    context_dict['cat_list'] = cat_list
    
    for category in category_list:
        category.url = category.name.replace(' ', '_')
         
    
    if request.session.get('last_visit'):
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0)
        
        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] += 1
            request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1
      
    return render_to_response('rango/index.html', context_dict, context)



def about(request):
    
    context = RequestContext(request)
    cat_list = get_category_list()
    dic = {'dance':'Dancing all night!'}
    dic['cat_list'] = cat_list
    
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0
    
    dic['count'] = count
    
    return render_to_response('rango/about.html', dic, context)

def category(request, category_name_url):
    context = RequestContext(request)
    cat_list = get_category_list()
    
    category_name = category_name_url.replace('_', ' ')
    context_dict = {'category_name': category_name}
    context_dict['cat_list'] = cat_list
    
    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        category.views += 1
        category.save()
        #pages = Category.page_set
        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_url'] = category_name_url
    except Category.DoesNotExist:
        pass
    
    return render_to_response('rango/category.html', context_dict, context)

def page(request, page_id):
    
    try:
        page = Page.objects.get(id=page_id)
        page.views += 1
        page.save()
        return HttpResponseRedirect(page.url)
    except Page.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))

@login_required
def add_category(request):
    context = RequestContext(request)
    cat_list = get_category_list()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            
            return HttpResponseRedirect(reverse('index'))
        else:
            print form.errors
    
    else:
        form = CategoryForm()
        
    return render_to_response('rango/add_category.html', {'form':form, 'cat_list' : cat_list}, context)

@login_required
def add_page(request, category_name_url):
    context = RequestContext(request)
    category_name = category_name_url.replace('_', ' ')
    cat_list = get_category_list()
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            page = form.save(commit=False)
            
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                return HttpResponseRedirect(reverse('add_category'))
            
            page.views = 0
            page.save()
            
            return HttpResponseRedirect(reverse('category', args=[category_name_url]))
        else:
            print form.errors
    else:
        form = PageForm()
    
    return render_to_response('rango/add_page.html', {'form':form,
            'category_name_url': category_name_url, 'category_name': category_name,
            'cat_list': cat_list}, context)
        
        
def contact(request):
    
    context = RequestContext(request)
    
    if request.method == 'POST':
        
        form = ContactForm(request.POST)
        form_agent = ContactFormAgent(request.POST)
        if form.is_valid() and form_agent.is_valid():
            
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            
            return HttpResponseRedirect(reverse('thanks'))
    else:
        form = ContactForm(initial = {'message':'Move!', 'subject':'Dancing'}, auto_id='yerzat_%s', label_suffix=": ")
        form_agent = ContactFormAgent()
    return render_to_response('rango/contact.html', {'form':form, 'form_agent':form_agent}, context)
    #return HttpResponse(form.as_p())

def thanks(request):
    return HttpResponse('Thank you!')


def register(request):
    
    context = RequestContext(request)
    cat_list = get_category_list()
    
    registered = False
    
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
                profile.picture = request.FILES['picture']
            
            profile.save()
            
            registered = True
        
        else:
            print user_form.errors, profile_form.errors
        
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render_to_response('rango/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered,
         'cat_list': cat_list},
        context)


def user_login(request):
    
    context = RequestContext(request)
    cat_list = get_category_list()
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("You rango account is disabled")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details applied.")

    else:
        return render_to_response('rango/login.html', {'cat_list': cat_list}, context)

@login_required    
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text")

def user_logout(request):
    logout(request)
    
    return HttpResponseRedirect(reverse('index'))

def search(request):
    context = RequestContext(request)
    result_list = []
    
    if request.method == 'POST':
        query = request.POST['query'].strip()
        
        if query:
            result_list = run_query(query)
    
    return render_to_response('rango/search.html', {'result_list': result_list}, context)

    
def test_template(request):
    context = RequestContext(request)
    return render_to_response('rango/base5.html', {}, context)

def get_category_list(max_result=0, starts_with=''):
    cat_list = []
    
    if starts_with:
        cat_list = Category.objects.filter(name__starts_with=starts_with)
    else:
        cat_list = Category.objects.all()
    
    if max_result > 0:
        if len(cat_list) > max_result:
            cat_list = cat_list[:max_result]
    
    for cat in cat_list:
        cat.url = cat.name.replace(' ', '_')
    
    return cat_list
    
@login_required
def profile(request):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {'cat_list': cat_list}
    
    u = User.objects.get(username=request.user)
    
    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None
    
    context_dict['user'] = u
    context_dict['userprofile'] = up
    
    return render_to_response('rango/profile.html', context_dict, context)

@login_required
def like_category(request):
    context = RequestContext(request)
    cat_id = None
    
    if request.method == 'GET':
        cat_id = request.GET['category_id']
    
    likes = 0
    
    if cat_id:
        category = Category.objects.get(id=int(cat_id))
        if category:
            category.likes += 1
            likes = category.likes
            category.save()
    
    return HttpResponse(likes)


def suggest_category(request):
    context = RequestContext(request)
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        
    cat_list = get_category_list(8, starts_with)
    
    return render_to_response('rango/categoty_list.html', {'cat_list':cat_list}, context)
















