from django.shortcuts import get_object_or_404, render
from kwejk.models import Gallery, kwejkForm,requestForm, Request
from kwejk.kwejk_module import ShortGallery
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse

def load_more(request):
    if request.is_ajax():
        amount=int(request.GET['amount'])
        start_index=int(request.GET['start'])
        #change -pk to pk to get ordered from oldest to newest
        try:
            galleries=Gallery.objects.order_by('-pk')[start_index:]
        except IndexError:
            galleries=Gallery.objects.order_byb("-pk")
        template='<li><a href="{0}">{1}</a></li>'
        string=""
        for i in range(amount):
            try:
                string=string+template.format("out?url="+galleries[i].url, galleries[i].name.replace("Å","ł").replace("Ä","ę"))
            except IndexError:
                break
        return  HttpResponse(string)
    else:
        return HttpResponse("nope")
def sendRequest(request):
    form = requestForm(request.POST)
    if request.is_ajax() and form.is_valid():
        newReq=Request(page=request.POST['page'], text=request.POST['text'])
        newReq.save()
        return HttpResponse("Wysłano")
    else:
        return HttpResponse("Coś poszło nie tak ;(")
@csrf_exempt
def showGallery(request):
    url = request.GET['url']
    try:
        Gallery.objects.get(url=url)
    except:
        kwejk = ShortGallery(request.GET['url'])
        try:
            output = kwejk.run()
        except:
            return HttpResponseRedirect("/?status=0")
        newGallery = Gallery(url=url, source=output, name=kwejk.title)
        newGallery.save()
        return HttpResponse(mark_safe(output))
    else:
        return HttpResponse(mark_safe(Gallery.objects.get(url=url).source))
@csrf_exempt
def showForm(request):
    if request.method == 'POST':
        form = kwejkForm(request.POST)
        if form.is_valid():
            #kwejk=ShortGallery(request.POST['url'])
            #output=kwejk.run()
            #template = loader.get_template('polls/kwejkOutput.html')
            #context = RequestContext(request, {
            #'input':mark_safe(output),
            #  })
            return showGallery(request, request.POST['url'])
            # return redirect('file', request.POST['url'])
    else:
        try:
            stat=request.GET['status']
        except:
            stat=1
        form = kwejkForm()
        reqForm=requestForm()
        return render(request,'kwejk/form_template.html',{'form':form,'requestForm':reqForm, 'status':stat})

