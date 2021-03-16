from django.contrib.auth.models import User, Group
from .models import Article
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ArticleSerializer
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins

"""
The generic views provided by REST framework 
allow you to quickly build API views that map 
closely to your database models
"""
class GenericAPIView(generics.GenericAPIView, 
                    mixins.ListModelMixin, 
                    mixins.CreateModelMixin, 
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin):

    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    lookup_field = 'id'

    def get(self, request, id = None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


"""
Using the APIView class is pretty much the 
same as using a regular View class, as usual,
the incoming request is dispatched to an appropriate 
handler method such as .get() or .post().
"""

# APIView class
class ArticleAPIView(APIView):
    def get(self, request):
        queryset = Article.objects.all()
        serializer = ArticleSerializer(queryset, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetails(APIView):
    def get_object(self, id):
        try:
            return Article.objects.get(id = id)

        except Article.DoesNotExist:
            return HttpResponse(status = 404)

    def get(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)

    def put(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


# View classes
@api_view(['GET', 'POST'])
@csrf_exempt
def article(request):
    if request.method == 'GET':
        queryset = Article.objects.all()
        serializer = ArticleSerializer(queryset, many = True)
        return JsonResponse(serializer.data, safe = False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk = pk)

    except Article.DoesNotExist:
        return HttpResponse(status = 404)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data = data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status = 204)