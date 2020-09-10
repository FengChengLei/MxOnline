from django import forms

from apps.operations.models import UserFavourite, CourseComments


class UserFavForm(forms.ModelForm):
    class Meta:
        model = UserFavourite
        fields = ['fav_id', 'fav_type']


class CommentsForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ['course', 'comments']