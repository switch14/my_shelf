from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        help_text="カンマ区切りで入力してください。（ビジネス,小説,漫画）",
        label ="タグ"
    )

    class Meta:
        model = Review
        fields = ["rating", "comment", "read_date", "tags_input"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.isinstance and self.instance.pk: #Reviewオブジェクトが存在する場合＝更新の場合
            current = list(self.instance.tags.values_list("name", flat=True))
            if current:
                self.fields["tags_input"].initial = ", ".join(current)
    