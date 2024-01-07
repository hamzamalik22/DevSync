from django.forms import ModelForm
from django import forms
from .models import *


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','demo_link','source_link','featured_image','tags']

        widgets = {
            'tags' : forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({ 'class' : 'input'})

        # self.fields['title'].widget.attrs.update(
        #     { 'class' : 'input'}
        # )

        # self.fields['description'].widget.attrs.update(
        #     { 'class' : 'input'}
        # )
            

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']

        labels = {
            'value' : 'Place your Vote',
            'body' : 'Add your Comment',
        } 

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({ 'class' : 'input'})