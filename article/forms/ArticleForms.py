from django import forms

from article.forms.ArticleSelectWidget import ArticleColumnSelectWidgt
from article.models import Article, Column


class ArticleForm(forms.ModelForm):
    column=forms.CharField(widget=ArticleColumnSelectWidgt,label="标签")

    def modelform_factory(self):
        data = self.cleaned_data['column']
        if len(data)<1:  # 如果data不满足满足条件
            raise forms.ValidationError('请选择栏目名称')
        return data

    class Meta:
        forms.model=Column
        fields = '__all__'