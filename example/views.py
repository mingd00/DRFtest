from rest_framework import viewsets, permissions, status, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework import mixins
from .models import Book
from .serializers import BookSerializer
from rest_framework import generics
from rest_framework import viewsets

@api_view(['GET'])
def helloAPI(request):
    return Response("hello world!")


class HelloAPI(APIView):
    def get(self, request, format=None):
        return Response("hello world")


@api_view(['GET', 'POST'])
def booksAPI(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def bookAPI(request, bid):
    book = get_object_or_404(Book, bid=bid)
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)



class BooksAPI(APIView):
    # 도서 전체 목록 가져오기
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 도서 1권 정보 등록하기
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookAPI(APIView):
    def get(self, request, bid):
        book = get_object_or_404(Book, bid=bid)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)


# DRF mixins 사용
class BooksAPIMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # GET 메소드 처리 함수(전체 목록 가져오기)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    # POST 메소드 처리 함수(1권 정보 등록하기)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class BookAPIMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid' # Django 기본 모델 pk가 아닌 bid를 pk로 사용하고 있으니 lookup_field로 설정

    #GET 메소드 처리 함수(1권 정보 가져오기)
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    #PUT 메소드 처리 함수(1권 수정하기)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    #DELETE 메소드 처리 함수(1권 삭제하기)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# DRF generics 사용
# 전체 목록 수정
class BooksAPIGenerics(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# 1개 + 1개 수정 + 1개 삭제
class BookAPIGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'

# DRF Viewset & Router
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

