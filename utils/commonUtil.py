from django.db.models import QuerySet


class CommonUtil:
    @staticmethod
    def toString(Obj):
        objtype=type(Obj)
        print(objtype)


    @staticmethod
    def querySetToList(querySet,field=""):
        if(type(querySet)==QuerySet):
            list=[]
            list=[', '.join(x) for x in querySet]
            return list
        return None

