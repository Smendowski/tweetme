from django import forms
from .models import Tweet

MAX_TWEET_LENGTH = 240

class TweetForm(forms.ModelForm):
  # MetaClass is describing the entire form itself
  class Meta:
    model = Tweet
    # input tex field
    fields = ['content']

  def clean_content(self):
    content = self.cleaned_data.get("content")
    if len(content) > MAX_TWEET_LENGTH:
      raise forms.ValidationError("This tweet is too long")
    return content
