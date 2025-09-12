from django import forms
from .models import Review, Tag

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment", "read_date", "tags"]
        widgets = {
            "read_date": forms.DateInput(attrs={"type": "date"}),
            "tags": forms.SelectMultiple,
        }
    
    def __init__(self, *args, **kwargs):
        """タグの選択肢をログインユーザーのタグに限定"""
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        if self.request:
            self.fields["tags"].queryset = Tag.objects.filter(owner=self.request.user).order_by('name')