from django.db import models
from django.contrib import admin

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200, help_text="the title of this project, usually the same as the book, e.g. Schaum's German Grammar")
    path = models.CharField(max_length=254, help_text="the path where copied images from the cameras will be stored")
    book_isbn = models.CharField(max_length=20, null=True, blank=True)
    book_title = models.CharField(max_length=254, null=True, blank=True)
    book_website = models.URLField(null=True, blank=True)
    date_created = models.DateTimeField(null=True, blank=True, help_text="the date this project was created")
    total_pages = models.CharField(max_length=5,null=True, blank=True, help_text='total number of pages') 
    def __unicode__(self):
        return '%s %s %s %s %s %s %s' % (self.id, self.title, self.path, self.book_isbn, self.title, self.book_website, self.date_created)
    class Admin(admin.ModelAdmin):
        list_display = ('title', 'date_created', 'path', 'book_isbn')
        list_filter = ('title', 'path')
        ordering = ['title']
        search_fields = ['title']
    class Meta:
        ordering = ['title']
    
class Page(models.Model):
    card = models.CharField(max_length=10, help_text='the card this page to which this card belongs')
    renamed = models.CharField(max_length=5,null=True, blank=True, help_text='total number of pages')
    xfer_date = models.DateTimeField(null=True, blank=True, help_text="the date this file was transferred")
    cleanup_split = models.CharField(max_length=100,null=True, blank=True, help_text='split details')
    cleanup_deskew = models.CharField(max_length=100,null=True, blank=True, help_text='deskewed details')
    cleanup_margin = models.CharField(max_length=100,null=True, blank=True, help_text='margin details')
    cleanup_content = models.CharField(max_length=100,null=True, blank=True, help_text='content selection details')
    status = models.CharField(max_length=100,null=True, blank=True, help_text='status details')
    project = models.ForeignKey(Project)
    class Admin(admin.ModelAdmin):
        list_display = ('renamed', 'card', 'xfer_date', 'status', 'project')
        list_filter = ('renamed', 'card', 'xfer_date', 'project')
        ordering = ['xfer_date']
        search_fields = ['renamed']

class Logs(models.Model):
    entry = models.CharField(max_length=254)
    class Admin(admin.ModelAdmin):
        pass
    
class Temp(models.Model):
    p = models.CharField(max_length=254,null=True, blank=True, help_text='parent thingy if needed') 
    k = models.CharField(max_length=254,null=True, blank=True, help_text='key thingy if needed') 
    v = models.CharField(max_length=254,null=True, blank=True, help_text='value thingy if needed') 
    m = models.CharField(max_length=254,null=True, blank=True, help_text='misc thingy if needed') # misc
    def __unicode__(self):
        return '%s %s %s %s' % (self.p, self.k, self.v, self.m)
    class Admin(admin.ModelAdmin):
        list_display = ('p', 'k', 'v', 'm')
        list_filter = ('p', 'k')
        ordering = ['v']
        search_fields = ['p', 'k', 'v', 'm' ]
    

#https://docs.djangoproject.com/en/dev/ref/contrib/admin/
#register these items for the /admin GUI
admin.site.register(Project, Project.Admin)
admin.site.register(Page, Page.Admin)
admin.site.register(Logs, Logs.Admin)
admin.site.register(Temp, Temp.Admin)