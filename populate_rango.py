import os

def populate():
    python_cat = add_cat('Startup Tools', 128, 64)
    
    add_page(cat=python_cat,
             title='HBS Startup Tribe Tools List ',
             url='https://sites.google.com/site/startuptribe/general-information/communications')
    
    add_page(cat=python_cat,
             title='NYU Startup Resources Library',
             url='http://www.nyu.edu/about/university-initiatives/entrepreneurship-at-nyu/resources.html')
    
    add_page(cat=python_cat,
             title='Harvard Innovation Lab',
             url="http://i-lab.harvard.edu/")
    
    add_page(cat=python_cat,
             title='PBworks startup tools List',
             url="http://toolboard.org/")
    
    django_cat = add_cat('Startup Tools', 64, 32)
    
    add_page(cat=django_cat,
             title="Customer Creation",
             url="http://startuptools.pbworks.com/w/page/17974963/FrontPage")
    
    add_page(cat=django_cat,
             title="startupweekend",
             url="http://startupweekend.org/resources/")
    
    add_page(cat=django_cat,
             title="ycombinator.com Libs",
             url="http://ycombinator.com/lib.html")
    
    #frame_cat = add_cat('Other Frameworks', 32, 16)
    
    #add_page(cat=frame_cat,
     #        title="Bottle",
      #       url="http://bottlepy.org/docs/dev/")
    ##
    #add_page(cat=frame_cat,
     #        title='Flask',
      #       url='http://flask.pocoo.org')
    
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {1} - {0}".format(str(c), str(p))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, url=url, views=0)[0]
    return p

def add_cat(cat, views=0, likes=0):
    c = Category.objects.get_or_create(name=cat, views=views, likes=likes)[0]
    return c

if __name__ == '__main__':
    print "Starting Rango Population Script"
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
    from rango.models import Category, Page
    populate()
    
    
    
    
    
    
    
    
    
    
    
    
    