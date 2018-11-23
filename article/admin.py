from datetime import datetime
from uuid import UUID, uuid1

from django.contrib import admin

# Register your models here.
from django.db.models import QuerySet

from article.forms.ArticleForms import ArticleForm
from article.models import Column, Article, Poll, Comment
from utils.datetime import DateTimeUtil
from utils.file import FileUtil
from xia_admin import settings
from xia_admin.settings import STATIC_PAGE


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name','slug','intro','created')
    list_per_page = settings.PER_PAGE_SHOW

# class PollInline(admin.StackedInline):
#     model = Poll
#     exclude = ('comment',)
#     extra=1
#
# class CommentInline(admin.StackedInline):
#     model = Comment
#
#     extra = 1

class ArticleAdmin(admin.ModelAdmin):
    list_display=('title','slug','author','pub_date','update_date','status')
    #date_hierarchy 新增一个时间过滤分类功能,添加这个功能要注释掉setting.py中的时区自动获取
    date_hierarchy = 'pub_date'
    #filter_horizontal 左右过滤器的
    #filter_horizontal=['column']
    list_per_page=settings.PER_PAGE_SHOW
    list_filter=('publish_status','update_date')
    radio_fields = {"publish_status": admin.HORIZONTAL}
    #raw_id_fields = ("author",)
    search_fields = ['title','content']
    form = ArticleForm
    # inlines = [PollInline,CommentInline]

    #重写搜索函数
    def get_search_results(self, request, queryset, search_term):
        queryset=Article.objects.query_by_keyword(search_term)
        queryset, use_distinct = super(ArticleAdmin, self).get_search_results(request, queryset, search_term)
        print(queryset)
        print(search_term)
        print(use_distinct)
        return queryset,use_distinct

    #重写列表的获取函数
    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        print(qs)
        print('登陆用户是不是超级用户？%s' % request.user.is_superuser)
        if(request.user.is_superuser):
            return qs
        else:
            return qs.filter(author=request.user)

    # 重写修改文章详情页面的内容
    def get_fields(self, request, obj=None):
        if(obj is not None):
            obj.content=FileUtil.readFileLines(obj.content)
        return super().get_fields(request, obj)

    # def get_fields(self, request, obj):
    #     obj.content = FileUtil.readFileLines(obj.content)
    #     super(ArticleAdmin, self).get_fields(request, obj)

    def get_column_id(self,column_names):
        column_names= column_names.replace('，',',').replace(' ',',');
        column_names_list=column_names.split(',')
        for name in column_names_list:
            name=name.strip()
            if len(name)>0:
                Column.objects.get_or_create(name=name,slug=name.strip().lower())
        qs= Column.objects.filter(name__in=column_names_list)
        return qs




    #重写保存方法
    def save_model(self, request, obj, form, change):
        print(form.data['column'])
        #form.data['column']= self.get_column_id(form.data['column'])
        #
        #qs=Column.objects.filter(id=4)

        form.cleaned_data['column']=self.get_column_id(form.data['column'])
        fileName=obj.title
        if(obj.id is None):
            obj.slug=uuid1()
        path=STATIC_PAGE+'\\'+str(datetime.now().year)+'\\'+str(datetime.now().month)
        print(path)
        FileUtil.mkdir(path,True)
        path+='\\'+fileName+'.html'
        FileUtil.writeFileBytes(path,obj.content)
        obj.content=path

        #super(ArticleAdmin, self).save_model(self, request, obj, form, change)
        obj.save()



    #自定义操作
    actions = ['make_publish','make_drop','make_write']
    def make_publish(self,request,queryset):
        rows_updated=queryset.update(publish_status='p')
        message_bit='%s 篇文章' % rows_updated
        self.message_user(request,"%s 被发布" % message_bit)
    make_publish.short_description = "发布所选的 文章"

    def make_drop(self,request,queryset):
        rows_updated = queryset.update(publish_status='d')
        message_bit = '%s 篇文章' % rows_updated
        self.message_user(request, "%s 被丢弃" % message_bit)
    make_drop.short_description = "丢弃所选的 文章"

    def make_write(self,request,queryset):
        rows_updated = queryset.update(publish_status='w')
        message_bit = '%s 篇文章' % rows_updated
        self.message_user(request, "%s 被保存为草稿" % message_bit)
    make_write.short_description = "草稿所选的 文章"

    #修改文章状态的显示方式

    #修改TextFiled的显示方式
    formfield_overrides = {
    }


admin.site.register(Column,ColumnAdmin)
admin.site.register(Article,ArticleAdmin)
