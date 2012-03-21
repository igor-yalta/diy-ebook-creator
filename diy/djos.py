import os, sys
from threading import Thread
from time import sleep
from django.core import serializers
import os
import shutil
from datetime import datetime
from subprocess import call    


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
    try:
        t  = Temp(p='message',v='PLEASE WAIT -- Counting and enumerating your images...').save()
        files = os.listdir(src.replace('\\','/')) # eg 'e:/dcim'
    except:
        return '{"error": "This directory does not exist."}' # JSON syntax
    
    #delete entries for this card under this project before inserting below
    pgs = Page.objects.filter(card=card,project=p).delete()
    
    types = ('jpg', 'jpeg', 'tif', 'tiff', 'png', 'jp2')
    inc_by = 2
    n = 0 # page number
    tasks  = []
    
    if card == 'left':
        n=1
    elif card == 'right':
        n=2
    elif card == 'both':
        n=1
        inc_by = 1
    else:
        return '{"error":"Your card is not left right or both!"}'
    
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
        return '{"error":"No images found!"}'
    
    total = len(tasks) 
    i     = 1
    for spath, dpath, output, log in tasks:
        # cancelled?
        c = Temp.objects.filter(p='cancel')
        if c:
            t = Temp.objects.all().delete() 
            return '{"error":"Cancelled"}'

        try:
            t = Temp.objects.all().delete() 
            p  = round((float(i)/float(total))*100) # percent complete
            t  = Temp(p=output,k=i,v=p,m=total).save()
            shutil.copy2(spath, dpath)
            #sleep(2)
            if i == total:
                sleep(1) # allows second thread to see 100 percent complete
            i += 1
        except:
            return '{"error":"An error occurred during copying and renaming. Verify your projects folder exists."}' # JSON syntax
    t = Temp.objects.all().delete() # delete temp entries
    return '{"success": "Import succeeded"}' # JSON syntax

def run_batch(Temp, Page, p, path):
    try:
        bin = [get_apps()['scantailor-cli']]
    except:
        return '{"error": "scantailor could not be found"}' # JSON
    
    path_in = path
    path_out = os.path.join(path, 'scantailor')
    flist_in = []  # eg jpgs
    flist_out = [] # eg tifs
    
    #try creating dest
    try:
        os.makedirs(path_out, 0777)
    except:
        pass
    
    opts = ['-v']
    opts.append('--layout=1')
    opts.append('--dpi=400')
    opts.append('--output-dpi=600')
    opts.append('--color-mode=mixed')
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
    opts.append('-o=project.ScanTailor')
    
    #options.append('--output-project=/somewhere') 
    
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
    opts2 = ['--content-box=100x100:2100x3900', '--alignment-vertical=top', '--alignment-horizontal=left']
    cmd = bin + opts2 + [flist_in[0]] + [path_out]
    call(cmd,cwd=path_in)

    return

    actions = ['OCR using ABBYY', 'ABBYY processed your file successfully.']
    total = len(pgs) + len(actions)
    i = 1
    for pg in pgs:
        # cancelled?
        c = Temp.objects.filter(p='cancel')
        if c:
            t = Temp.objects.all().delete() 
            return '{"error":"Cancelled"}'

        f = [pg.renamed]
        o = ['--orientation=' + pg.card]
        
        # update status in db 
        pgs = Temp.objects.all().delete()
        percent  = round((float(i)/float(total))*100) # progress
        cmd = bin + opts + o + flist_in + [path_out]
        cmd_str = 'File: ' + f[0] + '<br/><br/>  <span id="progressbar-details-command"> Command: ' + ' '.join(cmd) + '</span><br/>'
        t = Temp(p=cmd_str, k=i, v=total, m=percent).save()
        i += 1
    call(cmd,cwd=path_in)
    
    # now abbyy
    try:
        bin = [get_apps()['abbyy']]
    except:
        return '{"error": "abbyy could not be found"}' 

    opts        = ['/send','acrobat']
    opts.append('/send acrobat')  
    cmd = bin + flist_out + opts
    
    #update progress
    pgs = Temp.objects.all().delete()
    percent  = round((float(i)/float(total))*100) # progress
    t = Temp(p=actions.pop(0), k=i, v=total, m=percent).save()
    
    try:
        call(cmd,cwd=path_out)
    
        #update progress    
        i += 1
        pgs = Temp.objects.all().delete()
        percent  = round((float(i)/float(total))*100) # progress
        t = Temp(p=actions.pop(0), k=i, v=total, m=percent).save()

        return '{"success": "Scantailor and ABBYY succeeded"}'
    except:
        return '{"error": "A problem occurred with ABBYY: bin=' + ' '.join(bin) + ' flist=' + ' '.join(flist) + ' opts=' + ' '.join(opts) +' cwd=' + ' '.join(path_out) + '"}'
    
#if __name__ == '__main__':
    #drive = get_usb()
    #print drive
    
    
