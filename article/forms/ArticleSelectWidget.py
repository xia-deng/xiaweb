import html
import os

from django import forms
from django.forms import widgets
from math import ceil

from article.models import Column, Article
from utils.commonUtil import CommonUtil
from xia_admin.settings import STATICFILES_DIRS, STATIC_ROOT, SELECT_INPUT_COLUMN_NUMBER


class ArticleColumnSelectWidgt(forms.Widget):
    class Media:
        js=('%s/js/jQuery-2.1.1.js' % STATICFILES_DIRS,'%s/js/article/inputAndCheckBox.js' % STATICFILES_DIRS)
    def __init__(self, attrs=None):
        super(ArticleColumnSelectWidgt,self).__init__(attrs)


    def render(self, name, value, attrs=None):
        #value=Article.objects.filter(title=value)#Column.objects.all()
        allColumn=Column.objects.all()
        names=CommonUtil.querySetToList(value.values_list("name")) if value is not None and len(value)>0 else []
        allNames=CommonUtil.querySetToList(allColumn.values_list("name"))
        # html='<div style="position: relative; display: inline-block; width:100%">'
        # html+='<input class="txtValue text validation-passed" id=%s name=%s size="30" type="text" value="">' % ('id_'+name,name+'[]')
        # html+='<ul class="more_categories" id="blog_category_checkbox">'
        # for qs in value:
        #     html+='<li><label><input type="checkbox" data-type="checkbox" data-value=%s value=%s>%s</label></li>' % (qs.name,qs.id,qs.name)
        # html+='</ul></div>'
        # return html
        print(allNames)
        number = SELECT_INPUT_COLUMN_NUMBER
        html='<table cellpadding="0" style="border:0;" cellspacing="0" class="tablist"><tr><td colspan=%s>' \
             '<input class="txtValue vTextField" maxlength="256" required type="text" id=%s name=%s value=%s /></td></tr>' % (number,'id_'+name,name, ','.join(names)+',' if len(names)>0 else '')

        rows=ceil(len(allColumn)/number);
        print('rows is %s' % rows)
        for i in range(rows):
            oneRow= len(allColumn)-(i*number) if len(allColumn)-(i*number)<=number else number
            print('i is %s' % i)
            print('oneRow is %s' % oneRow)
            html+='<tr>'
            for j in range(oneRow):
                print('j is %s' % j)
                index=i*number+j
                if value is not None and len(value)>0 and value[index].name in allNames:
                    html += '<td ><input type="checkbox" checked  data-type="checkbox" data-value=%s value=%s />%s </td>' % (
                        allColumn[index].name, allColumn[index].id, allColumn[index].name)
                else:
                    html+='<td ><input type="checkbox"  data-type="checkbox" data-value=%s value=%s />%s </td>' % (allColumn[index].name,allColumn[index].id,allColumn[index].name)
            html+='</tr>'
        html += '</table> '
        return html





