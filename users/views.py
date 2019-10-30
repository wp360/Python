from .serializers import BookSerializer,BookModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProfile,Book

from rest_framework import mixins
from rest_framework import generics

from rest_framework import viewsets
from rest_framework.permissions import BasePermission

class BookAPIView1(APIView):
    """
    使用Serializer
    """
    def get(self, request, format=None):
        APIKey=self.request.query_params.get("apikey", 0)
        developer=UserProfile.objects.filter(APIkey=APIKey).first()
        if developer:
            balance=developer.money
            if balance>0:
                isbn = self.request.query_params.get("isbn", 0)
                books = Book.objects.filter(isbn=int(isbn))
                books_serializer = BookSerializer(books, many=True)
                developer.money-=1
                developer.save()
                return Response(books_serializer.data)
            else:
                return Response("兄弟，又到了需要充钱的时候！好开心啊！")
        else:
            return Response("查无此人啊")

class BookAPIView2(APIView):
    """
    使用ModelSerializer
    """
    def get(self, request, format=None):
        APIKey=self.request.query_params.get("apikey", 0)
        developer=UserProfile.objects.filter(APIkey=APIKey).first()
        if developer:
            balance=developer.money
            if balance>0:
                isbn = self.request.query_params.get("isbn", 0)
                books = Book.objects.filter(isbn=int(isbn))
                books_serializer = BookModelSerializer(books, many=True)
                developer.money-=1
                developer.save()
                return Response(books_serializer.data)
            else:
                return Response("兄弟，又到了需要充钱的时候！好开心啊！")
        else:
            return Response("查无此人啊")

# 用mixins.ListModelMixin + GenericAPIView的方式实现视图封装
# ListModelMixin：用于显示所有图书
# CreateModelMixin：添加一本书
# GenricAPIView：继承自APIView，提供as_view()等，获取当前视图类中queryset和serializer_class ，用于给ListModelMixin和CreateModelMixin使用。
class BookMixinView1(mixins.ListModelMixin,generics.GenericAPIView):
    queryset=Book.objects.all()
    serializer_class = BookModelSerializer
    # 如果这里不加get函数，代表默认不支持get访问这个api，所以必须加上
    def get(self,request,*args,**kwargs):
        APIKey = self.request.query_params.get("apikey", 0)
        developer = UserProfile.objects.filter(APIkey=APIKey).first()
        if developer:
            balance=developer.money
            if balance>0:
                isbn = self.request.query_params.get("isbn", 0)
                developer.money -= 1
                developer.save()
                self.queryset = Book.objects.filter(isbn=int(isbn))
                return self.list(request, *args, **kwargs)
            else:
                return Response("兄弟，又到了需要充钱的时候！好开心啊！")
        else:
            return Response("查无此人啊")

# 用generics.ListAPIView的方式实现视图封装
class BookMixinView2(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer
    def get(self,request,*args,**kwargs):
        APIKey = self.request.query_params.get("apikey", 0)
        developer = UserProfile.objects.filter(APIkey=APIKey).first()
        if developer:
            balance=developer.money
            if balance>0:
                isbn = self.request.query_params.get("isbn", 0)
                developer.money -= 1
                developer.save()
                self.queryset = Book.objects.filter(isbn=int(isbn))
                return self.list(request, *args, **kwargs)
            else:
                return Response("兄弟，又到了需要充钱的时候！好开心啊！")
        else:
            return Response("查无此人啊")

# 用viewsets+Router的方式实现视图封装
class IsDeveloper(BasePermission):
    message='查无此人啊'
    def has_permission(self,request,view):
        APIKey = request.query_params.get("apikey", 0)
        developer = UserProfile.objects.filter(APIkey=APIKey).first()
        if developer:
            return True
        else:
            print(self.message)
            return False
class EnoughMoney(BasePermission):
    message = "兄弟，又到了需要充钱的时候！好开心啊！"
    def has_permission(self,request,view):
        APIKey = request.query_params.get("apikey", 0)
        developer = UserProfile.objects.filter(APIkey=APIKey).first()
        balance = developer.money
        if balance > 0:
            developer.money -= 1
            developer.save()
            return True
        else:
            return False
class BookModelViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = [IsDeveloper, EnoughMoney]
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer
    def get_queryset(self):
        isbn = self.request.query_params.get("isbn", 0)
        books = Book.objects.filter(isbn=int(isbn))
        queryset=books
        return queryset
