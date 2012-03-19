from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.defaults import *
from django.views.generic import list_detail

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('diy.views',
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('diy.wizard.views',
    (r'^$', 'welcome'),
    (r'^project-details/',              'project_details'),
    (r'^mountpoint/',                   'mountpoint'),
    (r'^import-gui/',                   'import_gui'),
    (r'^import-cmd/',                   'import_cmd'),
    (r'^import-cmd-get-progress/',      'import_cmd_get_progress'),
    (r'^import-cmd-cancel/',            'import_cmd_cancel'),
    (r'^import-cmd-is-valid/',          'import_cmd_is_valid'),
    (r'^scantailor/',                   'scantailor'),
    (r'^batch-cmd/',                    'batch_cmd'),
    (r'^batch-cmd-get-progress/',       'batch_cmd_get_progress'),
    (r'^batch-cmd-cancel/',             'batch_cmd_cancel'),
)
urlpatterns += staticfiles_urlpatterns()
