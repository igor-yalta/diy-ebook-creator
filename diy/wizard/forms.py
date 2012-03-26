# Create your forms here.
from django import forms
from django.forms import ModelForm, Select
from models import Project
import djos

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'date_created', 'path', 'color_mode')
        COLORS = (
                   ('mixed', 'Mixed (i.e. some color or grayscale, some black and white)'),
                   ('color_grayscale', 'Color / Grayscale'),
                   ('black_and_white', 'Black and White only'),
                   )
        widgets = {'color_mode': Select(choices=COLORS)}
        
    def clean_path(self):
        p = self.cleaned_data.get('path', '')
        t = self.cleaned_data.get('title', '')
        valid = djos.create_project_dirs(self.cleaned_data)
        if not valid:
            raise forms.ValidationError("I could not create this path: %s. Please check the path and try different one." % (p))
        return p