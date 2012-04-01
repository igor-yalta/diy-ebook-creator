import os, sys
from threading import Thread
from time import sleep
from django.core import serializers
import os
import shutil
from datetime import datetime
from subprocess import call    
from PIL import Image
import json

def is_scantailor():
    ''' 
    this crude function checks to see if scantailor is installed
    '''
    
    # can somebody fill in non-windows paths? 3-2-2012
    result = False
    
    if sys.platform == 'win32': #Windows
        dirs = [
               'c:/Program Files/Scan Tailor/',
               'c:/Program Files (x86)/Scan Tailor/',
               ]
    elif sys.platform == 'darwin': # OsX
        dirs = ['',]
    elif sys.platform == 'linux2': #Ubuntu Linux
        dirs = ['',]
    
    #if one of these paths exists, assume scan tailor is installed
    for dir in dirs:
        if os.path.isdir(dir):
            result = True
            
    return result

def get_apps():
    ''' 
    this admittedly crude function checks and returns paths for popular diy book scanner software
    '''
    # can somebody fill in non-windows paths? 3-2-2012
    result = {}

    if sys.platform == 'win32': #Windows
        apps = {'scantailor' :    ['C:/Program Files (x86)/Scan Tailor/scantailor.exe',
                                   'C:/Program Files/Scan Tailor/scantailor.exe',
                                  ],
                'scantailor-cli': ['C:/Program Files (x86)/Scan Tailor/scantailor-cli.exe',
                                   'C:/Program Files/Scan Tailor/scantailor-cli.exe',
                                  ],
                'abbyy':          ['C:/Program Files/ABBYY FineReader 5/finereader.exe',
                                   'C:/Program Files/ABBYY FineReader 6/finereader.exe',
                                   'C:/Program Files/ABBYY FineReader 7/finereader.exe',
                                   'C:/Program Files/ABBYY FineReader 8/finereader.exe',
                                   'C:/Program Files/ABBYY FineReader 9/finereader.exe',
                                   'C:/Program Files/ABBYY FineReader 10/finereader.exe',
                                   'C:/Program Files/ABBYY FineReader 11/finereader.exe',
                                   'C:/Program Files (x86)/ABBYY FineReader 5/finereader.exe',
                                   'C:/Program Files (x86)/ABBYY FineReader 6/finereader.exe',
                                   'C:/Program Files (x86)/ABBYY FineReader 7/finereader.exe',
                                   'C:/Program Files (x86)/ABBYY FineReader 8/finereader.exe',
                                   'C:/Program Files (x86)/ABBYY FineReader 9/finereader.exe',
                                   'C:/Program Files (x86)/ABBYY FineReader 10/finereader.exe',
                                   'C:/Program Files (x86)/ABBYY FineReader 11/finereader.exe',
                                  ]
                }  
        for app in apps:
            for p in apps[app]:
                if os.path.isfile(p):
                    result[app] = p
    elif sys.platform == 'darwin': # OsX
        dirs = ['',]
        result = None
    elif sys.platform == 'linux2': #Ubuntu Linux
        dirs = ['',]
        result = None
    
    return result

def get_drives():
    '''     
    http://stackoverflow.com/questions/827371/is-there-a-way-to-list-all-the-available-drive-letters-in-python
    '''
    import string
    from ctypes import windll
    import time
    import os
    #time.sleep(1) # for good measure
    
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    return set(drives)

def get_mountpoint(request):
    '''
    Sorry, this is windows-only currently 3-6-2012 Sean Wingert Paper Upgrade Project
    Sean's post here: http://stackoverflow.com/questions/1968539/how-to-detect-flash-drive-plug-in-in-windows-using-python/9578439#9578439
    '''
    before = request.session['mounted_before']
    after = request.session['mounted_after']
    drives = after - before
    delta = len(drives)
    result = 'Could not autodetect drive. Please enter manually'

    if (delta):
        for drive in drives:
            if os.system("cd " + drive + ":/100CANON") == 0: # try CHDK dir 
                result = drive + ':\\100CANON\\'
            if os.system("cd " + drive + ":/DCIM") == 0: # try DCIM 
                result = drive + ':\\DCIM\\'
            elif os.system("cd " + drive + ":/") == 0: # otherwise root
                result = drive + ':\\'
    else:
        result = "Unable to autodetect path"
    return result

def project_path():
    return os.path.join(os.path.dirname(__file__),'wizard','projects')

def create_project_dirs(cleaned_data):
    ''' create the project dirs, return True or False for validation '''
    title = cleaned_data.get('title', '')
    main = cleaned_data.get('path', '').replace('\\','/')
    sub  = os.path.join(main,title).replace('\\','/')
    sub_exists = os.path.isdir(sub)
    
    if sub_exists:
        pass
    else:
        try: # creating
            os.makedirs(sub, 0777)
        except:
            return False
    return True

def import_pages(p, Page, Temp, src, dst, card='left'):
    ''' copy and rename from card to computer '''
    
    # clean up progress table
    t = Temp.objects.all().delete()
    try:
        t  = Temp(p='message',k='notice', v='PLEASE WAIT -- Enumerating your images. The speed of this operation depends on image count, PC, and card(s), so please be patient!').save()
        files = os.listdir(src.replace('\\','/')) # eg 'e:/dcim'
    except:
        t  = Temp(p='message',k='error', v='This directory does not exist.').save()
        return '{"error": "This directory does not exist."}' # JSON syntax
    
    #delete entries for this card under this project before inserting below
    pgs = Page.objects.filter(card=card,project=p).delete()
    
    n = 0 # page number
    tasks  = []
    inc_by = 2
    types = ('jpg', 'jpeg', 'tif', 'tiff', 'png', 'jp2')
    
    if card == 'left':
        n=1
    elif card == 'right':
        n=2
    elif card == 'both':
        n=1
        inc_by = 1
    else:
        t  = Temp(p='message',k='error', v='Your card is not left right or both!').save()
        return '{"error":"Your card is not left right or both!"}'
    
    # list the commands
    for item in files:
        i = item.split('.')
        ext = i[-1] # -1 returns last part
        if ext.lower() in types:
            ns = '%(#)04d' % {'#':n} # n as string
            spath = src + os.sep + item
            renamed = ns + os.extsep + ext
            dpath = dst + os.sep + renamed
            task = "shutil.copy2('" + spath + "', '" + dpath + "')"
            n += inc_by
            output = "copied " + str(item) + " as " + renamed
            tasks.append([spath,dpath,output,task])
            pg = Page(card=card,renamed=renamed,status='xfer and rename',xfer_date=datetime.now(),project=p).save()
    
    if not len(tasks):
        t  = Temp(p='message',k='error', v='No images found!').save()
        return '{"error":"No images found!"}'

    # total pages
    total = len(tasks)
    
    # update total pages in db    
    if card=='both':
        p.total_pages=(total*2)   # count all images on 1 camera rigs
    else:
        p.total_pages=(total*2)-2 # count all but first and last images in 2 camera rigs 
    p.save() # store count in total to db

    # execute commands, show progress
    i     = 1
    for spath, dpath, output, log in tasks:
        # cancelled?
        c = Temp.objects.filter(p='cancel')
        if c:
            t = Temp.objects.all().delete()
            t  = Temp(p='message',v='Cancelled!').save()
            return '{"error":"Cancelled"}'
        try:
            t        = Temp.objects.all().delete()            
            percent  = format(float(i)/float(total)*100,'.2f')[0:-3] # percent complete - don't use round()!
            Temp(p=output,k=i,v=percent,m=total).save()
            shutil.copy2(spath, dpath)
         
            if i == total:
                sleep(1) # allows progress thread to see 100 percent complete
            i += 1
        except:
            t  = Temp(p='message',k='error', v='An occurred during copying and renaming. Verify that your projects folder exists.').save()
            return '{"error":"An error occurred during copying and renaming. Verify that your projects folder exists."}'
    t = Temp.objects.all().delete() # delete temp entries
    return '{"success": "Import succeeded"}'

def run_batch(Temp, Page, p, path):
    # clean the progress table
    t = Temp.objects.all().delete()
    
    # scantailor installed?
    try:
        bin = [get_apps()['scantailor']]
    except:
        t  = Temp(p='message',k='error', v='Scantailor could not be found. Is it installed? Sorry, only Windows is supported currently. Please see the forums (link below) to help us fix this!').save()
        return '{"error": "scantailor could not be found. Is it installed?"}'
    
    # scantailor-cli installed?
    try:    
        bin_cli = [get_apps()['scantailor-cli']]
    except:
        t  = Temp(p='message',k='error', v='Scantailor-cli (command line version) could not be found. Is it installed? Sorry, only Windows is supported currently. Please see the forums (link below) to help us fix this!').save()
        return '{"error": "scantailor-cli (command line version) could not be found. Is it installed?"}'
    
    # abbyy installed?
    try:
        bin_abbyy = [get_apps()['abbyy']]
    except:
        t  = Temp(p='message',k='error', v='ABBYY FineReader could not be found. Is it installed? Sorry, only Windows is supported currently. Please see the forums (link below) to help us fix this!').save()
        return '{"error": "ABBYY FineReader could not be found. Is it installed?"}' 
    
    path_in = path
    path_out = os.path.join(path, 'scantailor')
    flist_in = []  # eg jpgs
    flist_out = [] # eg tifs
    fn = 'project.ScanTailor'
    ppath = [os.path.join(path_out,fn)] # project path
    
    # try creating dest
    if os.path.exists(path_out):
        pass # if re-running this script
    else:
        try:
            os.makedirs(path_out, 0777)
        except:
            t  = Temp(p='message', k='error', v='I could not create the directory you requested. Does it already exist? That directory was: ' + path_out + '. Please try again.').save()
            return '{"error": "I could not create the directory you requested. Does it already exist? Please try again"}'
    
    # scantailor options
    opts = ['-v']
    opts.append('--layout=1')
    opts.append('--dpi=400')
    opts.append('--output-dpi=600')
    opts.append('--color-mode=' + p.color_mode)
    opts.append('--white-margins=true')
    opts.append('--normalize-illumination=true')
    opts.append('--threshold=1')
    opts.append('--match-layout-tolerance=1') # http://www.diybookscanner.org/forum/viewtopic.php?f=8&t=870&start=10
    opts.append('--margins-left=5')
    opts.append('--margins-bottom=5')
    opts.append('--margins-left=10')
    opts.append('--margins-right=10')
    opts.append('--alignment-vertical=center')
    opts.append('--alignment-horizontal=center')
    opts.append('-o=scantailor/project.ScanTailor') # project

    # get files and their paths    
    pgs = Page.objects.filter(project=p).order_by('renamed')
    flist_in  = [x.renamed for x in pgs] # 0001.jpg, 0002.jpg, ...
    flist_out = [os.path.splitext(x.renamed)[0] + os.extsep + 'tif' for x in pgs] # 0001.tif, 0002.tif, ...
        
    # if using L and R cards, delete first and last pages, which are probably blanks in dual rigs
    if pgs[0].card!='both':
        flist_in.pop(0)
        flist_in.pop(-1)
        flist_out.pop(0)
        flist_out.pop(-1)

    #select content of first and last pages
    # BROKEN!? # opts2 = ['--content-box=100x100:2100x3900', '--alignment-vertical=top', '--alignment-horizontal=left']
    #command = ' '.join(flist_in).replace('\\','/')
    
    # prepare
    if p.auto_mode == 'manual':
        auto_txt = 'When done, Scantailor will open. Once that happens, make any adjustments, clicking Output per adjusted image, then close Scantailor, saving your changes.'
    else:
        auto_txt = ''
        
    msg      = 'Please wait. Scantailor-cli may take a long time before generating the first TIFs. This is normal. ' + auto_txt + ' ABBYY Finereader will start afterwards.'
    tasks    = ['scantailor_cli','abbyy']
    if p.auto_mode=='manual':
        tasks.append('scantailor_gui')
    total    = len(flist_in) + len(tasks)
    percent  = 0 
    step     = 0
    t         = Temp(p=msg, k=step, v=percent, m=total, o='start', o2=json.dumps([None])).save()
    
    #rotate
    angles = {'right': 270, 'left': 90, 'both':0}
    for pg in pgs:
        if pg.status != 'rotate':
            ip = os.path.join(path,pg.renamed).replace('\\','/')
            im = Image.open(ip)
            im.rotate(angles[pg.card]).save(ip)
            pg.status='rotate'
            pg.save()
                          
    # run scantailor_cli
    try:
        cmd = bin_cli + opts + flist_in + [path_out]
        call(cmd,cwd=path_in) # process
        sleep(4) # without sleeping, below msg won't appear. why?
        t = Temp.objects.get(o='last')
        t.k = int(t.k)+1
        t.v = format(float(t.k)/float(t.m)*100,'.2f')[0:-3] # percent
        if p.auto_mode=='manual':
            auto_txt = 'I opened Scantailor. Please manually switch to that program. Per image, make any changes and click Output. When done, close Scantailor.'
        else:
            auto_txt = ''
        t.p = 'Scantailor-CLI completed successfully. ' + auto_txt
        t.save()
    except:
        t  = Temp(p='message',k='error', v='Something broke trying to open the Scantailor-cli (command line version) application. Command was "' + ' '.join(cmd))
        return "{'error': 'something broke during scantailor-cli processing. sorry.'}"
    
    # run scantailor GUI
    if p.auto_mode=='manual':
        try:
            cmd = bin + ppath
            call(cmd) # open result
            t = Temp.objects.get(o='last')
            t.k = int(t.k)+1
            t.v = format(float(t.k)/float(t.m)*100,'.2f')[0:-3] # percent
            t.p = 'Scantailor-GUI completed successfully. I am now running ABBYY Finereader.'
            t.save()
        except:
            t  = Temp(p='message',k='error', v='Something broke trying to open the scantailor application. Command was "' + ' '.join(bin + ppath))
            return "{'error': 'something broke trying to the open the scantailor application'}"

    # now abbyy
    try:
        opts = ['/send','acrobat']
        cmd  = bin_abbyy + flist_out + opts
        call(cmd, cwd=path_out)
        t = Temp.objects.get(o='last')
        t.k = int(t.k)+1
        t.v = format(float(t.k)/float(t.m)*100,'.2f')[0:-3] # percent
        t.p = 'ABBYY Finereader completed succesfully. Enjoy your e-book!'
        t.save()
    except:
        t  = Temp(p='message',k='error', v='I could not run ABBYY. The command was probably incorrect. It was "' + ' '.join(cmd))
        return '{"error": "I could not run ABBYY. The command was probably incorrect. It was "' + ' '.join(cmd) + '}'
     
    #Temp.objects.all().delete()
    t  = Temp(p='complete').save()
    
def batch_progress(proj, path, Temp, Page):
    from PIL import Image

    ''' return current status to the view '''
    # which state?
    try:
        t = Temp.objects.get(o='last')
    except:
        try:
            t = Temp.objects.get(o='start')
        except:
            try:
                t = Temp.objects.get(o='cancel')
                return ('')
            except:
                Temp.objects.filter(p='message').delete()
                Temp(p='message', k='error', v='Not processing').save()
                return serializers.serialize('json', Temp.objects.filter(p='message'))[1:-1] or '{}'

    # get listing
    listing  = os.listdir(path)
    newtifs  = []

    for item in listing:
        i = item.split('.')
        ext = i[-1] # -1 returns last part
        if ext.lower() == 'tif':
            url = os.path.join(path,item).replace('\\','/').split('/')
            url.pop(0) # remove root drive, replace with /root -- see MEDIA_URL
            url = '/root/' + '/'.join(url)
            newtifs.append(url)

    oldtifs = json.loads(t.o2) # unserialize from db
    delta = list(set(newtifs) - set(oldtifs))

    if delta:
        total   = t.m
        step    = len(newtifs)
        percent = format(float(step)/float(total)*100,'.2f')[0:-3]
        tif_url = delta[-1]
        tif_name= os.path.split(tif_url)[-1]
        Temp.objects.filter(o='initial').delete()
        Temp.objects.filter(o='last').delete()
        
        #create thumbnail dir
        cdir = os.path.join(path, 'cache')
        if os.path.isdir(cdir):
            pass # st-cli in mixed mode
        else:
            os.makedirs(cdir, 0777) # st-cli in color_grayscale

        #create thumbnails
        size = 300, 441
        t_in = os.path.join(path,tif_name).replace('\\','/')
        t_out= os.path.join(path,'cache', tif_name).replace('tif','jpg').replace('\\','/')
        im   = Image.open(t_in)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(t_out, "JPEG")
        j_out= t_out.split('/')
        j_out.pop(0)
        j_out= '/root/' + '/'.join(j_out)
        j_in = j_out.replace('/scantailor/cache/','/')
        
        t = Temp(p='Current file: ' + tif_name, k=step, v=percent, m=total, o='last', o2=json.dumps(newtifs), o3=j_in, o4=j_out).save()
        return serializers.serialize('json', Temp.objects.filter(o='last'))[1:-1] or '{}'
    else:
        if t.o == 'last':
            return serializers.serialize('json', Temp.objects.filter(o='last'))[1:-1] or '{}'
        elif t.o == 'start':
            return serializers.serialize('json', Temp.objects.filter(o='start'))[1:-1] or '{}'
        else:
            return('{}')