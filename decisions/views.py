# Create your views here.

from django.shortcuts import render
import urllib2


def google_maps(request):

    get_str = request.GET

    print get_str
    print "meta req: \n", request.META.get('QUERY_STRING', '')
    #print "req:", request
    post_string = "http://maps.google.com/maps/geo?output=csv&q=blah"
    result = urllib2.urlopen(post_string).read()
    print "result:"
    print result
    return render(request, "base.html")

    pass