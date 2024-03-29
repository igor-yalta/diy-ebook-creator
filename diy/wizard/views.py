# Create your views here.
from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core import serializers
from distutils.sysconfig import get_python_lib
import os, shutil, datetime
import djos
from models import Project, Page, Temp
from forms import ProjectForm
from django.utils import simplejson

def welcome(request):
    vars = {}
    apps = djos.get_apps()
    vars['template']   = 'content/welcome.html'
    vars['next']       = 'project-details'
    vars['scantailor'] = apps.get('scantailor',False)
    vars['abbyy']      = apps.get('abbyy', False)
    return render_to_response(vars['template'], {'vars': vars})

def mountpoint(request):
    state = request.GET.get('state','before')
    vars = {}
    vars['template']   = 'content/get-mountpoint.html'
    
    if state == 'before':
        request.session['mounted_before'] = djos.get_drives()
        vars['instructions'] = '' 
    else:
        request.session['mounted_after'] = djos.get_drives() 
        vars['path'] = djos.get_mountpoint(request)
    
    return render_to_response(vars['template'], {'vars': vars})

def project_details(request):
    vars = {}
    vars['template'] = 'content/project-details.html'
    vars['previous'] = '/'
    vars['next']     = '/import-gui'
    vars['redirect'] = vars['next'] 
    vars['path'] = request.session.get('path',djos.project_path())
    #vars['debug']    = True
    form = ProjectForm(initial={'path': vars['path'], 
                                'language1': 'English',
                                'language2': 'English',
                                'language3': 'English'}
                       )
    
    # submitting
    if request.method == 'POST':
        prev_title = request.session.get('title', False)
        curr_title = request.POST.get('title')
        
        # this title already in db?
        try: # yes
            p = Project.objects.get(title=curr_title)
            form = ProjectForm(request.POST, instance=p) # load form (from db)
        except: #no
            post2 = request.POST.copy() # immutable so copy before changing
            post2['date_created']=datetime.datetime.now()
            form = ProjectForm(post2) # create form

        if form.is_valid():  
            form.save()
            request.session['title'] = form.cleaned_data['title']
            request.session['path'] = form.cleaned_data['path']
            request.session['fullpath'] = request.session.get('path','Error') + os.sep + request.session.get('title','Error')
            return HttpResponseRedirect(vars['redirect'])
    # displaying
    elif request.session.get('title', False): # old
        try:
            p = Project.objects.get(title=request.session['title'])
            form = ProjectForm(instance=p)
        except ObjectDoesNotExist:
            vars['errors'] = {'Missing title': 'I could not find this title for some reason! Please enter a different title.'}
            request.session.pop('title')
            request.session.pop('path')
            request.session.pop('fullpath')
        except MultipleObjectsReturned:
            vars['errors'] = {'Too many titles': 'There were too many projects with this name. That should not happen. Please enter a different title.'}
            request.session.pop('title')
            request.session.pop('path')
            request.session.pop('fullpath')
        except:
            vars['errors'] = {'oops': 'I received some unexpected, unknown error. You might want to report this.'}
    else: # new
        pass
    return render_to_response(vars['template'], {'form': form, 'vars': vars})

def import_gui(request):
    vars = {}
    vars['template'] = 'content/import-gui.html'
    vars['previous'] = '/project-details'
    vars['next']     = '/scantailor'
    vars['redirect'] = vars['next']
    vars['projectpath'] = request.session.get('path','Error') + os.sep + request.session.get('title','Error')
    #vars['debug']    = True
    form             = []
    return render_to_response(vars['template'], {'form': form, 'vars': vars})

def import_cmd(request):
    t                = Temp.objects.all().delete() # in case cancel clicked after successful import
    src              = request.GET['src'] # intentionally cause error if not provided
    src              = src.replace('%3A',':').replace('%5C','\\').replace('%2F','/')
    dst              = request.session['fullpath']
    card             = request.GET['card']
    title            = request.session['title']
    p                = Project.objects.get(title=request.session['title'])
    vars             = {}
    vars['template'] = 'content/import-cmd.html'
    vars['output']   = djos.import_pages(p, Page, Temp, src, dst, card)
    return HttpResponse(vars['output'])

def import_cmd_is_valid(request):
    src              = request.GET['src'] # intentionally cause error if not provided
    src              = src.replace('%3A',':').replace('%5C','\\').replace('%2F','/').replace('+',' ')
    types            = ('jpg', 'jpeg', 'tif', 'tiff', 'png', 'jp2')
    photos           = False
    try:
        files = os.listdir(src.replace('\\','/')) # eg 'e:/dcim'
        for item in files:
            i = item.split('.')
            ext = i[-1] # -1 returns last part
            if ext.lower() in types:
                photos = True
        if photos:
            return HttpResponse('{"success": "Valid path."}') # JSON syntax
        else:
            return HttpResponse('{"error": "No images found."}') # JSON syntax
    except:
        result = '{"error": "This directory does not exist."}' # JSON syntax
    return HttpResponse(result)
    
def import_cmd_get_progress(request):
    vars             = {}
    vars['template'] = 'content/import-cmd-get-progress.html'
    vars['output'] = serializers.serialize('json', Temp.objects.filter(pk=1))[1:-1] or '{}'
    response = HttpResponse(vars['output']) # why can't IE do the following? mimetype='application/json; charset=utf8')
    response['Cache-Control'] = 'no-cache' # IE - https://docs.djangoproject.com/en/dev/ref/request-response/
    return response
 
def import_cmd_cancel(request):
    vars             = {}
    t = Temp.objects.all().delete()
    t  = Temp(p='cancel').save()
    vars['template'] = 'content/import-cmd-cancel.html'
    vars['output'] = serializers.serialize('json', Temp.objects.filter(pk=1))[1:-1] or '{}'
    response = HttpResponse(vars['output']) # why can't IE do the following? mimetype='application/json; charset=utf8')
    response['Cache-Control'] = 'no-cache'
    return response

def scantailor(request):
    vars = {}
    vars['template'] = 'content/scantailor.html'
    vars['previous'] = '/import-gui'
    vars['next']     = '/scantailor'
    vars['redirect'] = vars['next']
    vars['projectpath'] = request.session.get('path','Error') + os.sep + request.session.get('title','Error')
    #vars['debug']    = True
    form             = []
    return render_to_response(vars['template'], {'form': form, 'vars': vars})

def batch_cmd(request):
    t                = Temp.objects.all().delete() # in case cancel clicked after successful processing
    path             = request.session['fullpath']
    p                = Project.objects.get(title=request.session['title'])
    vars             = {}
    vars['template'] = 'content/scantailor-cmd.html'
    vars['output']   = djos.run_batch(Temp, Page, p, path)
    return HttpResponse(vars['output'])

def batch_cmd_get_progress(request):
    vars             = {}
    vars['template'] = 'content/batch-cmd-get-progress.html'
    proj             = Project.objects.get(title=request.session['title'])
    path             = os.path.join(request.session['fullpath'], 'scantailor')
    vars['output']   = djos.batch_progress(proj, path, Temp, Page)
    response = HttpResponse(vars['output']) # why can't IE do the following? mimetype='application/json; charset=utf8')
    response['Cache-Control'] = 'no-cache' # IE
    return response

def batch_cmd_cancel(request):
    vars             = {}
    t = Temp.objects.all().delete()
    t  = Temp(p='cancel').save()
    vars['template'] = 'content/batch-cmd-cancel.html'
    vars['output'] = serializers.serialize('json', Temp.objects.filter(pk=1))[1:-1] or '{}'
    response = HttpResponse(vars['output']) # why can't IE do the following? mimetype='application/json; charset=utf8')
    response['Cache-Control'] = 'no-cache' # IE
    return response