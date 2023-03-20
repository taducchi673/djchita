from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from .serializers import *
# from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly ,AllowAny
# from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.serializers import Serializer
# from .mixins import *
from rest_framework import viewsets
from rest_framework.decorators import action
# from rest_framework.permissions import IsAdminUser, SAFE_METHODS
# from django.db.models import Count
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly ,AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from datetime import datetime
from datetime import timedelta
from django.utils import timezone


class IsAdminUserOrAuthor(IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super(
            IsAdminUserOrReadOnly, 
            self).has_permission(request, view)
        # Python3: is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin


class UserViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        query = self.queryset.all()
        id = self.request.query_params.get('id')
        if id:
            query = query.filter(id=id)
        return query

    def get_permissions(self):
        if self.action in ['get_info', "retrive", "update", "partial_update", "profile", "create"]:
            return [IsAuthenticated()]
        elif self.action in ["destroy", "list"]:
            return [IsAdminUser()]
        return [AllowAny()]

    
    def profile(self, request):
        query = User.objects.filter(user = request.user)
        serializer = UserSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def list(self, request):
        query = self.queryset.all()
        serializer = UserSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        user = get_object_or_404(query, pk=pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def create(self, request, pk=None):
        query = request.user
        serializer = UserSerializer(query, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        user = get_object_or_404(query, pk=pk)
        serializer = UserSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        user = get_object_or_404(query, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        user = get_object_or_404(query, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlogViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    

    def get_permissions(self):
        if self.action in ['get_info', "retrive", "update", "partial_update","destroy", "post"]:
            return [IsAuthenticated()]
        elif self.action in []:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request):
        queryset = self.queryset.all()
        if 'topic_id' in self.request.query_params:

            topic_id = self.request.query_params.get("topic_id").split(',')
            queryset = queryset.filter(Q(topic_id__in = topic_id))
            
        serializer = BlogSerializer(queryset, many=True, context={'request': request})
    
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        user = get_object_or_404(query, pk=pk)
        serializer = BlogSerializer(user, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        
        query = self.queryset.all()
        blog = get_object_or_404(query, pk=pk)
        
        serializer = BlogSerializer(blog, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        user = get_object_or_404(query, pk=pk)
        serializer = BlogSerializer(user, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        user = get_object_or_404(query, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request): 
        serializer = self.serializer_class(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            self.queryset = Blog.objects.all() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path='comments')
    def get_comments(self, request, pk):
        # c = Course.objects.get(pk=pk)
        comments = self.get_object().blog_comments

        return Response(data=CommentSerializer(comments, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    
    
    @action(methods=['post'], url_path='comments', detail=True)
    def post(self, request, pk):
        
        blog = self.get_object()
        user = request.user 

        comment  = Comment.objects.create(user = user, blog = blog)
        
        comment.content = request.data['content']
        comment.save()
        return Response(status = status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ["retrive", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        elif self.action in []:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request):
        query = self.queryset.all()
        serializer = CommentSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        comment = get_object_or_404(query, pk=pk)
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        comment = get_object_or_404(query, pk=pk)
        # comment.content = request.data["content"]
        # comment.save()
        
        serializer = CommentSerializer(comment, data = request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        user = get_object_or_404(query, pk=pk)
        serializer = CommentSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        user = get_object_or_404(query, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)


    def get_permissions(self):
        if self.action in ['get_info', "retrive", "update", "partial_update","post", "get"]:
            return [IsAuthenticated()]
        elif self.action in ["destroy"]:
            return [IsAdminUser()]
        return [AllowAny()]

    
    def list(self, request):
        queryset = self.queryset.all()

        if 'subject_id' in self.request.query_params:

            subject_id = self.request.query_params.get("subject_id").split(',')
            queryset = queryset.filter(Q(subject_id__in = subject_id))
            print(queryset)

        if 'grade_id' in self.request.query_params:
            grade_id = self.request.query_params.get("grade_id").split(',')
            queryset = queryset.filter(Q(grade_id__in = grade_id) )
            print(queryset)


        if 'teacher_id' in self.request.query_params:
            teacher_id = self.request.query_params.get("teacher_id").split(",")
            queryset = queryset.filter(Q(teacher_id__in = teacher_id) )
            print(queryset)


        serializer = CourseSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        Course = get_object_or_404(query, pk=pk)
        serializer = CourseSerializer(Course, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        Course = get_object_or_404(query, pk=pk)
        serializer = CourseSerializer(Course, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            self.queryset = Course.objects.all() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.data)
        return Response({'status': 'Bad Request',
                         'message': serializer.is_valid()},
                          status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        Course = get_object_or_404(query, pk=pk)
        serializer = CourseSerializer(Course, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        Course = get_object_or_404(query, pk=pk)
        Course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get', "post"], detail=True, url_path='chapters')
    def getc(self, request, pk):
        if request.method == "GET":
        # c = Course.objects.get(pk=pk)
            chapters = self.get_object().course_chapter

            return Response(data=ChapterSerializer(chapters, many=True, context={'request': request}).data,
                            status=status.HTTP_200_OK)

        elif request.method == "POST":
            course = self.get_object()
                
            chapter  = Chapter.objects.create(course = course)
                
            chapter.name = request.data['name']

            chapter.save()
            return Response(status = status.HTTP_201_CREATED)
    
    
        

    @action(methods=['get', "post"], detail=True, url_path='comments')
    def get(self, request, pk):
        # c = Course.objects.get(pk=pk)
        if request.method == "GET":
            comments = self.get_object().course_comments

            return Response(data=CommentSerializer(comments, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

        elif request.method == "POST":
            course = self.get_object()
            user = request.user 

            comment  = Comment.objects.create(user = user, course = course)
            print(request.data)
            comment.content = request.data['content']

            comment.save()
            return Response(status = status.HTTP_201_CREATED)

   

    @action(methods=['get', "post"], detail=True, url_path='check-enrolled')
    def check_enrolled(self, request, pk):
        # c = Course.objects.get(pk=pk)
        if (request.method == "GET"):
            user = request.user 
            expiry = timezone.now() - timedelta(days = 365)
            enrolled = Enrolled.objects.filter(user = user, course_id = pk, created_date__gte=expiry)
            return Response(data=EnrolledSerializer(enrolled, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)
        elif request.method == "POST":
            user = request.user 
            course = self.get_object()
            # expiry = timezone.now() - timedelta(days = 365)
            enrolled, _ = Enrolled.objects.get_or_create(user = user, course = course)
            if _:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status = status.HTTP_400_BAD_REQUEST)
            

class CourseCategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer

    def get_permissions(self):
        if self.action in ['get_info', "retrive", "update", "partial_update"]:
            return [IsAuthenticated()]
        elif self.action in ["destroy"]:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request):
        query = self.queryset.all()
        serializer = CourseCategorySerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        CourseCategory = get_object_or_404(query, pk=pk)
        serializer = CourseCategorySerializer(CourseCategory, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        CourseCategory = get_object_or_404(query, pk=pk)
        serializer = CourseCategorySerializer(CourseCategory, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        CourseCategory = get_object_or_404(query, pk=pk)
        serializer = CourseCategorySerializer(CourseCategory, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        CourseCategory = get_object_or_404(query, pk=pk)
        CourseCategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LessonViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)


    def get_permissions(self):
        if self.action in ['get_info', "retrive", "update", "partial_update", "postv", "post", "destroy", "test"]:
            return [IsAuthenticated()]
        elif self.action in []:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request):
        query = self.queryset.all()
        serializer = LessonSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        Lesson = get_object_or_404(query, pk=pk)
        serializer = LessonSerializer(Lesson, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        Lesson = get_object_or_404(query, pk=pk)
        serializer = LessonSerializer(Lesson, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        Lesson = get_object_or_404(query, pk=pk)
        serializer = LessonSerializer(Lesson, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        Lesson = get_object_or_404(query, pk=pk)
        Lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get', "post"], detail=True, url_path='videolessons')
    def getVideolesson(self, request, pk):
        
        if request.method == "GET":
            videolessons = self.get_object().lesson_videolesson
            return Response(data=VideoLessonSerializer(videolessons, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

        elif request.method == "POST":
            print(request.data)
            serializer = VideoLessonSerializer(data=request.data, context={'request': request})
        
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)    
        
    

    @action(methods=['get', "post"], detail=True, url_path='tests')
    def test(self, request, pk):
        if request.method == "GET":
        # c = Course.objects.get(pk=pk)
            tests = self.get_object().lesson_test

            return Response(data=TestSerializer(tests, many=True, context={'request': request}).data,
                            status=status.HTTP_200_OK)

        elif request.method == "POST":
            lesson = self.get_object()
            print(request.data)

            if request.data["questions"] != []:
                test, _ = Test.objects.get_or_create(time_limit = request.data["time_limit"], lesson = lesson, name = request.data["name"])
                if _:
                    arr_questions = []
                    for q in request.data["questions"]:
                        x, __ = Question.objects.get_or_create(
                            question = q["question"] ,
                            answer1 = q["answer1"],
                            answer2 = q["answer2"],
                            answer3 = q["answer3"] ,
                            answer4 = q["answer4"] ,
                            correct_answer = q["correct_answer"]
                        )
                        arr_questions.append(x)
                
                    test.questions.set(arr_questions)
            
                    test.save()
                    return Response(status = status.HTTP_201_CREATED)
                else:
                    return Response(status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status = status.HTTP_400_BAD_REQUEST)
    
    
    
    @action(methods=['get'], detail=True, url_path='notebooklessons')
    def getNotebooklesson(self, request, pk):
        # c = Course.objects.get(pk=pk)
        notebooklessons = self.get_object().lesson_notebooklesson

        return Response(data=NotebookLessonSerializer(notebooklessons, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    
    
    @action(methods=['post'], url_path='notebooklessons', detail=True)
    def post(self, request, pk):
        
        lesson = self.get_object()
        # user = request.user 
        print(request.data)
        nb  = NotebookLesson.objects.create(lesson=lesson, content=request.data["content"], name =request.data["name"])
        nb.save()
        return Response(status = status.HTTP_201_CREATED)


class NotebookLessonViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = NotebookLesson.objects.all()
    serializer_class = NotebookLessonSerializer

    def get_permissions(self):
        if self.action in ['get_info', "retrive", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        elif self.action in []:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request):
        query = self.queryset.all()
        serializer = NotebookLessonSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        NotebookLesson = get_object_or_404(query, pk=pk)
        serializer = NotebookLessonSerializer(NotebookLesson, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        NotebookLesson = get_object_or_404(query, pk=pk)
        serializer = NotebookLessonSerializer(NotebookLesson, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        NotebookLesson = get_object_or_404(query, pk=pk)
        serializer = NotebookLessonSerializer(NotebookLesson, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        NotebookLesson = get_object_or_404(query, pk=pk)
        NotebookLesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True, url_path='comments')
    def get_comments(self, request, pk):
        # c = Course.objects.get(pk=pk)
        comments = self.get_object().notebooklesson_comments

        return Response(data=CommentSerializer(comments, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)
    
    
    @action(methods=['post'], url_path='comments', detail=True)
    def post(self, request, pk):
        
        notebooklesson = self.get_object()
        user = request.user 

        comment  = Comment.objects.create(user = user, notebooklesson = notebooklesson)
        print(request.data)
        comment.content = request.data['content']

        comment.save()
        return Response(status = status.HTTP_201_CREATED)

    # @action(methods=['put'], url_path='put_comment', detail=True)
    # def put(self, request, pk):
    #     comment = self.get_object().notebooklesson_comments.get_object(pk)
    #     serializer = CommentSerializer(comment, data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=['patch'], url_path='put_comment', detail=True)
    # def patch(self, request, pk):
    #     comment = self.get_object().notebooklesson_comments.get_object(pk)
    #     serializer = CommentSerializer(comment, data=request.data, partial = True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # @action(methods=['delete'], url_path='put_comment', detail=True)
    # def patch(self, request, pk):
    #     comments = self.get_object().notebooklesson_comments.get_object(pk)
    #     serializer = CommentSerializer(comment, data=request.data, partial = True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.action in ['get_info', "retrive", "update", "partial_update"]:
            return [IsAuthenticated()]
        elif self.action in ["destroy", "list"]:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request):
        query = self.queryset.all()
        serializer = QuestionSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        Question = get_object_or_404(query, pk=pk)
        serializer = QuestionSerializer(Question, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        Question = get_object_or_404(query, pk=pk)
        serializer = QuestionSerializer(Question, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        
        Question = get_object_or_404(query, pk=pk)
        serializer = QuestionSerializer(Question, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        Question = get_object_or_404(query, pk=pk)
        Question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['get'], detail=True, url_path='comments')
    def get_comments(self, request, pk):
        # c = Course.objects.get(pk=pk)
        comments = self.get_object().question_comments

        return Response(data=CommentSerializer(comments, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='comments', detail=True)
    def post(self, request, pk):
        
        question = self.get_object()
        user = request.user 

        comment  = Comment.objects.create(user = user, question = question)
        print(request.data)
        comment.content = request.data['content']

        comment.save()
        return Response(status = status.HTTP_201_CREATED)

    

class TestViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def get_permissions(self):
        if self.action in ['get_info', "retrive", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        elif self.action in []:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request):
        query = self.queryset.all()
        serializer = TestSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, pk=None):
        if request.data["questions"] != []:
            test, _ = Test.objects.get_or_create(time_limit = request.data["time_limit"], lesson_id = request.data["lesson"], name = request.data["name"])
            if _:
                arr_questions = []
                for question in request.data["questions"]:
                    q = Question.objects.create(
                        question = question["question"] ,
                        answer1 = question["answer1"],
                        answer2 = question["answer2"],
                        answer3 = question["answer3"] ,
                        answer4 = question["answer4"] ,
                        correct_answer = question["correct_answer"],
                        
                    )
                    q.save()
                    arr_questions.append(q)
            
                test.questions.set(arr_questions)
        
                test.save()
                return Response(status = status.HTTP_201_CREATED)
            else:
                return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        Test = get_object_or_404(query, pk=pk)
        serializer = TestSerializer(Test, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        Test = get_object_or_404(query, pk=pk)
        serializer = TestSerializer(Test, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        print(request.data)
        Test = get_object_or_404(query, pk=pk)
        if request.data["questions"] != []:
            arr_questions = []
            for question in request.data["questions"]:
                q, __ = Question.objects.get_or_create(
                    question = question["question"] ,
                    answer1 = question["answer1"],
                    answer2 = question["answer2"],
                    answer3 = question["answer3"] ,
                    answer4 = question["answer4"] ,
                    correct_answer = question["correct_answer"])
                q.save()
                arr_questions.append(q)
            
                Test.questions.set(arr_questions)
                Test.save()
        else: 
            return Response(status = status.HTTP_400_BAD_REQUEST)
        if "name" in request.data:
            Test.name = request.data["name"]
            Test.save()
        if "time_limit" in request.data:
            Test.time_limit = request.data["time_limit"]
            Test.save()
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        Test = get_object_or_404(query, pk=pk)
        Test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True, url_path='comments')
    def get_comments(self, request, pk):
        # c = Course.objects.get(pk=pk)
        comments = self.get_object().test_comments

        return Response(data=CommentSerializer(comments, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='comments', detail=True)
    def post(self, request, pk):
        
        test = self.get_object()
        user = request.user 

        comment  = Comment.objects.create(user = user, test = test)
        print(request.data)
        comment.content = request.data['content']

        comment.save()
        return Response(status = status.HTTP_201_CREATED)
    
    @action(methods=['get', 'post'], detail=True, url_path='questions')
    def get_questions(self, request, pk):
        if request.method == "GET":
        # c = Course.objects.get(pk=pk)
            questions = self.get_object().questions

            return Response(data=QuestionSerializer(questions, many=True, context={'request': request}).data,
                            status=status.HTTP_200_OK)

        elif request.method == "POST": 
            test = self.get_object()
            comment  = Comment.objects.create(user = user, test = test)
            print(request.data)
            comment.content = request.data['content']

            comment.save()
            return Response(status = status.HTTP_201_CREATED)
       

    @action(methods=['get'], url_path='checktests', detail=True)
    def postQuestion(self, request, pk):
        
        test = self.get_object()
        user = request.user 

        usertest, _ = UserTest.objects.get_or_create(user = user, test = test)
        # print(request.data)
        # comment.content = request.data['content']

        # comment.save()
        if _:
            	return Response(status = status.HTTP_201_CREATED)
        else: 
                return Response(status = status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['get'], url_path='posttests', detail=True)
    def postUserTest(self, request, pk):
        
        test = self.get_object()
        user = request.user 
        
        usertest, _ = UserTest.objects.get_or_create(user = user, test = test)
        
        # print(request.data)
        # comment.content = request.data['content']

        # comment.save()
        if not _:
            usertest["result"] = request.data["result"]
            usertest.save()
            return Response(status = status.HTTP_201_CREATED)
        else: 
            return Response(status = status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['get', 'post'], detail=True, url_path='submit')
    def submit_answers(self, request, pk):
        if request.method == "GET":
        # c = Course.objects.get(pk=pk)
            usertest = UserTest.objects.filter(user = request.user, test = self.get_object())

            return Response(data=UserTestSerializer(usertest, many=True, context={'request': request}).data,
                            status=status.HTTP_200_OK)

        elif request.method == "POST": 
            print(request.data)
            test = self.get_object()
            usertest  = UserTest.objects.create(user = request.user, test = test)
            if request.data["answers"] != []:
                arr_questions = []
                for answer in request.data["answers"]:
                    q, __ = Answer.objects.get_or_create(
                        questionid = answer["questionid"],
                        answer = answer["answer"]
                    )
                    q.save()
                    arr_questions.append(q)
            
                usertest.answers.set(arr_questions)
                usertest.save()
            return Response(status = status.HTTP_201_CREATED)

class UserTypeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer

    def get_permissions(self):
        if self.action in ['get_info', "retrive", "update", "partial_update"]:
            return [IsAuthenticated()]
        elif self.action in ["destroy", "list"]:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request):
        query = self.queryset.all()
        serializer = UserTypeSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        UserType = get_object_or_404(query, pk=pk)
        serializer = UserTypeSerializer(UserType, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        UserType = get_object_or_404(query, pk=pk)
        serializer = UserTypeSerializer(UserType, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        UserType = get_object_or_404(query, pk=pk)
        serializer = UserTypeSerializer(UserType, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        UserType = get_object_or_404(query, pk=pk)
        UserType.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['get'], detail=True, url_path='users')
    def get_usersbytype(self, request, pk):
        # c = Course.objects.get(pk=pk)
       

        users = self.get_object().user_usertype  
        if 'subject_id' in self.request.query_params:

            subject_id = self.request.query_params.get("subject_id").split(',')
            users = users.filter(Q(subject_id__in = subject_id))
            

        return Response(data=UserSerializer(users, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)
    
    

class VideoLessonViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = VideoLesson.objects.all()
    serializer_class = VideoLessonSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)


    def get_permissions(self):
        if self.action in ['get_info', "retrive", "update", "partial_update","destroy", "list"]:
            return [IsAuthenticated()]
        elif self.action in []:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request):
        query = self.queryset.all()
        serializer = VideoLessonSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        VideoLesson = get_object_or_404(query, pk=pk)
        serializer = VideoLessonSerializer(VideoLesson, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        VideoLesson = get_object_or_404(query, pk=pk)
        serializer = VideoLessonSerializer(VideoLesson, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        VideoLesson = get_object_or_404(query, pk=pk)
        serializer = VideoLessonSerializer(VideoLesson, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        VideoLesson = get_object_or_404(query, pk=pk)
        VideoLesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True, url_path='comments')
    def get_comments(self, request, pk):
        # c = Course.objects.get(pk=pk)
        comments = self.get_object().videolesson_comments

        return Response(data=CommentSerializer(comments, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)
    
    @action(methods=['post'], url_path='comments', detail=True)
    def post(self, request, pk):
        
        videolesson = self.get_object()
        user = request.user 

        comment  = Comment.objects.create(user = user, videolesson = videolesson)
      
        comment.content = request.data['content']

        comment.save()
        return Response(status = status.HTTP_201_CREATED)

    #     return Response(status=status.HTTP_201_CREATED)

class RatingViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.action in ['get_info', "retrive", "update", "partial_update"]:
            return [IsAuthenticated()]
        elif self.action in ["destroy", "list"]:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request):
        query = self.queryset.all()
        serializer = CourseRatingSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        CourseRating = get_object_or_404(query, pk=pk)
        serializer = CourseRatingSerializer(CourseRating, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        CourseRating = get_object_or_404(query, pk=pk)
        serializer = CourseRatingSerializer(CourseRating, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        CourseRating = get_object_or_404(query, pk=pk)
        serializer = CourseRatingSerializer(CourseRating, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        CourseRating = get_object_or_404(query, pk=pk)
        CourseRating.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LikeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


    def get_permissions(self):
        if self.action in ['get_info', "retrive", "list", "update", "partial_update"]:
            return [IsAuthenticated()]
        elif self.action in ["destroy"]:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request):
        query = self.queryset.all()
        serializer = LikeSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        Like = get_object_or_404(query, pk=pk)
        serializer = LikeSerializer(Like, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        Like = get_object_or_404(query, pk=pk)
        serializer = LikeSerializer(Like, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        Like = get_object_or_404(query, pk=pk)
        serializer = LikeSerializer(Like, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        Like = get_object_or_404(query, pk=pk)
        Like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GradeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_permissions(self):
        if self.action in ['get_info', "retrive", "update", "partial_update"]:
            return [IsAuthenticated()]
        elif self.action in ["destroy"]:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request):
        query = self.queryset.all()
        serializer = GradeSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        Grade = get_object_or_404(query, pk=pk)
        serializer = GradeSerializer(Grade, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        Grade = get_object_or_404(query, pk=pk)
        serializer = GradeSerializer(Grade, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        Grade = get_object_or_404(query, pk=pk)
        serializer = GradeSerializer(Grade, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        Grade = get_object_or_404(query, pk=pk)
        Grade.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['get'], detail=True, url_path='courses')
    def get_usersbytype(self, request, pk):
        # c = Course.objects.get(pk=pk)
        grades = self.get_object().grade_courses

        return Response(data=GradeSerializer(grades, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

class SubjectViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_permissions(self):
        if self.action in ['get_info', "retrive", "update", "partial_update"]:
            return [IsAuthenticated()]
        elif self.action in ["destroy"]:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request):
        query = self.queryset.all()
        serializer = SubjectSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        Subject = get_object_or_404(query, pk=pk)
        serializer = SubjectSerializer(Subject, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        Subject = get_object_or_404(query, pk=pk)
        serializer = SubjectSerializer(Subject, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        Subject = get_object_or_404(query, pk=pk)
        serializer = SubjectSerializer(Subject, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        Subject = get_object_or_404(query, pk=pk)
        Subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['get'], detail=True, url_path='courses')
    def get_usersbytype(self, request, pk):
        # c = Course.objects.get(pk=pk)
        subjects = self.get_object().subject_courses

        return Response(data=SubjectSerializer(subjects, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)



class TopicViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_permissions(self):
        if self.action in ['get_info', "retrive", "update", "partial_update"]:
            return [IsAuthenticated()]
        elif self.action in ["destroy"]:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request):
        query = self.queryset.all()
        serializer = TopicSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        user = get_object_or_404(query, pk=pk)
        serializer = TopicSerializer(user, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        user = get_object_or_404(query, pk=pk)
        serializer = TopicSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        user = get_object_or_404(query, pk=pk)
        serializer = TopicSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        user = get_object_or_404(query, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True, url_path='blogs')
    def get_comments(self, request, pk):
        # c = Course.objects.get(pk=pk)
        Topic = self.get_object().Topic_comments

        return Response(data=CommentSerializer(Topic, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    
    
    @action(methods=['post'], url_path='blogs', detail=True)
    def post(self, request, pk):
        
        Topic = self.get_object()
        user = request.user 

        comment  = Comment.objects.create(user = user, Topic = Topic)
        
        comment.content = request.data['content']

        comment.save()
        return Response(status = status.HTTP_201_CREATED)


class EnrolledViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Enrolled.objects.all()
    serializer_class = EnrolledSerializer

    def get_permissions(self):
        if self.action in ['get_info', "retrive", "update", "partial_update"]:
            return [IsAuthenticated()]
        elif self.action in ["destroy"]:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request):
        query = self.queryset.all()
        serializer = EnrolledSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        Enrolled = get_object_or_404(query, pk=pk)
        serializer = EnrolledSerializer(Enrolled, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        Enrolled = get_object_or_404(query, pk=pk)
        serializer = EnrolledSerializer(Enrolled, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        Enrolled = get_object_or_404(query, pk=pk)
        serializer = EnrolledSerializer(Enrolled, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        Enrolled = get_object_or_404(query, pk=pk)
        Enrolled.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChapterViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    def get_permissions(self):
        if self.action in ['get_info', "retrive", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        elif self.action in []:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request):
        query = self.queryset.all()
        serializer = ChapterSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = self.queryset.all()
        Chapter = get_object_or_404(query, pk=pk)
        serializer = ChapterSerializer(Chapter, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        query = self.queryset.all()
        Chapter = get_object_or_404(query, pk=pk)
        serializer = ChapterSerializer(Chapter, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        query = self.queryset.all()
        Chapter = get_object_or_404(query, pk=pk)
        serializer = ChapterSerializer(Chapter, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        query = self.queryset.all()
        Chapter = get_object_or_404(query, pk=pk)
        Chapter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True, url_path='lessons')
    def get_comments(self, request, pk):
        
        lessons = self.get_object().chapter_lesson

        return Response(data=LessonSerializer(lessons, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    
    
    @action(methods=['post'], url_path='lessons', detail=True)
    def post(self, request, pk):
        
        chapter = self.get_object()
        lesson  = Lesson.objects.create(chapter = chapter, name=request.data['name'])
        
        lesson.save()  
        return Response(status = status.HTTP_201_CREATED)