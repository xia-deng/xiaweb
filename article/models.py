from datetime import datetime

from django import forms
from django.contrib.auth.models import User
from django.db import models

# 文章管理Model.
from django.db.models.fields import CharField
from django.utils.html import format_html

from DjangoUeditor.models import UEditorField
from utils.file import FileUtil
from xia_admin.settings import IS_POLL_COMMENT_NUM_CAN_EDIT


class Column(models.Model):
    name=models.CharField('栏目名称',max_length=256)
    #db_index创建索引字段
    slug=models.CharField('栏目网址',max_length=256,db_index=True)
    intro=models.TextField('栏目简介',default='')
    #auto_now_add 用于创建；auto_now用于修改
    created=models.DateTimeField('创建时间',auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='栏目'
        verbose_name_plural='栏目'
        ordering=['created']

#扩展Article的manager
class ArticleManager(models.Manager):
    #根据文章类型来查询文章
    def query_by_column(self,column_id):
        query=self.get_queryset().filter(column_id=column_id)
        return query

    #根据用户来获取和用户相关的文章
    def query_by_user(self,user_id):
        query=User.objects.get(id=user_id)
        article_list=query.article_set.all()
        return article_list

    #根据点赞数来排行文章列表
    def query_by_polls(self):
        query=self.get_queryset().order_by('poll_num')
        return query

    # 根据发表时间来排行文章列表
    def query_by_time(self):
        query = self.get_queryset().order_by('-pub_date')
        return query

    # 根据文章标题或内容查询文章
    def query_by_keyword(self, keyword):
        query = (self.get_queryset().filter(title__contains=keyword) |
                 self.get_queryset().filter(content__contains=keyword)).distinct()
        return query


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', '丢弃'),
        ('p', '发布'),
        ('w', '草稿'),
    )
    column=models.ManyToManyField(Column,verbose_name='归属栏目')
    title=models.CharField('标题',max_length=256)
    slug=models.CharField('网址',max_length=256,db_index=True,editable=False)

    author=models.ForeignKey('auth.User',blank=True,null=True,verbose_name='作者')
    content=UEditorField('内容', height=300, width=800,
        default=u'', blank=True, imagePath="uploads/images/",
        toolbars='besttome', filePath='uploads/files/')
    publish_status=CharField('状态',max_length=1,choices=STATUS_CHOICES)

    pub_date=models.DateTimeField('发表时间',auto_now_add=True,editable=True)
    update_date=models.DateTimeField('更新时间',auto_now=True,null=True)
    poll_num=models.IntegerField('点赞数',default=0,editable=IS_POLL_COMMENT_NUM_CAN_EDIT)
    comment_num=models.IntegerField('评论数',default=0,editable=IS_POLL_COMMENT_NUM_CAN_EDIT)

    #定义发布状态的显示方式
    def publishStatus(self):
        html=""
        if(self.publish_status=='p'):
            html='<img src="/static/admin/img/icon-yes.svg" alt="True"/>发布'
        elif (self.publish_status=='d'):
            html ='<img src="/static/admin/img/icon-no.svg" alt="True"/>丢弃'
        else:
            html = "<i class='changelink'>草稿</i>"
        return format_html(html)
    publishStatus.short_description='状态'
    publishStatus.admin_order_field = 'publish_status'
    status=property(publishStatus)

    def articleContent(self):
        return FileUtil.readFileLines(self.content)
    #content = property(articleContent)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name='文章'
        verbose_name_plural='文章'

    #申明自定义的Manger管理器
    objects=ArticleManager()

#文章评论模块
class Comment(models.Model):
    author=models.CharField(null=True,max_length=128)
    article=models.ForeignKey(Article,null=True)
    content=models.CharField(max_length=500,null=False)
    pub_date=models.DateTimeField(auto_now_add=True,editable=False)
    poll_num=models.IntegerField(default=0)

    def __str__(self):
        return self.content


#点赞模块
class Poll(models.Model):
    author=models.CharField(null=True,max_length=128)
    article=models.ForeignKey(Article,null=True)
    comment=models.ForeignKey(Comment,null=True)
    pub_date=models.DateTimeField(auto_now_add=True,editable=False)



