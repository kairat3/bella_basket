from rest_framework import generics
from news.serializers import NewsSerializer
from news.models import News


class NewsListApiView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsRetrieveApiView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
