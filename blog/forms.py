from django import forms
from django.core.exceptions import ValidationError

from blog.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'content')

        labels = {
            'content': 'Comment'
        }

    def clean_content(self):
        content = self.cleaned_data['content']
        if content.count('\n') > 7:
            raise ValidationError('To many line breaks!')
        return content

    def save_with_post(self, post):
        comment = self.save(commit=False)
        comment.post = post
        comment.save()
        return comment

