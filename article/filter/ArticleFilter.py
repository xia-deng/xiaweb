from django.contrib import admin


class ArticleColumnFilter(admin.SimpleListFilter):
    #显示在过滤标题
    title=('归属栏目')
    #显示在URL参数上
    parameter_name = 'column'

    def lookups(self, request, model_admin):
        print(self)
        print(request)
        print(model_admin)
        print('nimabi')
