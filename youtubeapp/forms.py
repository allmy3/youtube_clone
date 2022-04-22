from django import forms

from .models import Channel, Video, Comment


class NewChannelAndUpdateChannelForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = ['name', 'avatar', 'slug', 'description', 'categories']


class NewVideoForm(forms.ModelForm):

    video_file = forms.FileField(widget=forms.ClearableFileInput, required=False)

    class Meta:
        model = Video
        fields = ['video_file', 'title', 'description', 'visibility', 'thumbnail']


class NewCommentForm(forms.ModelForm):

	content = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Текст комментария'}))

	class Meta:
		model = Comment
		fields = ['content']

