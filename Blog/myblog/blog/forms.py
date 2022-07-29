from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={'placeholder': 'Your name..'}))
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'mail@mail.com'})
    )
    body = forms.CharField(
        label='Comment',
        widget=forms.Textarea(attrs={'placeholder': 'comment content..'})
    )
