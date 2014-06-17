from django.conf.urls import url, patterns, include

urlpatterns = patterns('',
    url(r'^$', 'rango.views.index', name='index'),
    
    url(r'^about/$', 'rango.views.about', name='about'),
    
    url(r'^category/(?P<category_name_url>\w+)/$', 'rango.views.category', name='category'),
    
    url(r'^add_category/$', 'rango.views.add_category', name='add_category'),
    
    url(r'^contact/$', 'rango.views.contact', name='contact'),
    
    url(r'^contact/thanks/$', 'rango.views.thanks', name='thanks'),
    
    url(r'^add_page/(?P<category_name_url>\w+)/$', 'rango.views.add_page', name='add_page'),
    
    url(r'^register/$', 'rango.views.register', name='register'),
    
    url(r'login/$', 'rango.views.user_login', name='login'),
    
    url(r'restricted/$', 'rango.views.restricted', name='restricted'),
    
    url(r'^logout/$', 'rango.views.user_logout', name='logout'),
    
    url(r'^page/(?P<page_id>\d+)/$', 'rango.views.page', name='page'),
    
    url(r'^template/$', 'rango.views.test_template', name='base2'),
    
    url(r'^profile/$', 'rango.views.profile', name='profile'),
    
    url(r'like_category/$', 'rango.views.like_category', name='like_category'),
    
    url(r'suggest_category/$', 'rango.views.suggest_category', name='suggest_category'),
    
    
)