from rest_framework import serializers
from .models import * 
from rest_framework.permissions import IsAdminUser


class UserSerializer(serializers.ModelSerializer):

    imageurl = serializers.SerializerMethodField(source='avatar')

    def get_imageurl(self, obj):
        request = self.context['request']
        if obj.avatar and not obj.avatar.name.startswith('/static'):
            path = '/static/%s' % obj.avatar.name

            return request.build_absolute_uri(path)

    class Meta: 
        model = User
        fields = "__all__"

class UserInfoSerializer(serializers.ModelSerializer):

    class Meta: 
        model = User
        fields = ["username", "id"]

class BlogSerializer(serializers.ModelSerializer):

    imageurl = serializers.SerializerMethodField(source = "image")

    def get_imageurl(self, obj):
        request = self.context['request']
        if obj.image and not obj.image.name.startswith('/static'):
            path = '/static/%s' % obj.image.name

            return request.build_absolute_uri(path)

    class Meta: 
        model = Blog
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Comment
        fields = "__all__"

class LikeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Like
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):

    imageurl = serializers.SerializerMethodField(source='image')

    def get_imageurl(self, obj):
        request = self.context['request']
        if obj.image and not obj.image.name.startswith('/static'):
            path = '/static/%s' % obj.image.name

            return request.build_absolute_uri(path)

    class Meta: 
        model = Course
        fields = "__all__"

class CourseCategorySerializer(serializers.ModelSerializer):

    
    
    class Meta: 
        model = CourseCategory
        fields = "__all__"

class LessonSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Lesson
        fields = "__all__"

class NotebookLessonSerializer(serializers.ModelSerializer):
    class Meta: 
        model = NotebookLesson
        fields = "__all__"



class QuestionSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Question
        fields = "__all__"

class CorrectAnswerSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Question
        fields = ("correct_answer")

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many = True, read_only = True)
    class Meta: 
        model = Test
        fields = "__all__"

class UserTypeSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = UserType
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = Subject
        fields = "__all__"


class GradeSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = Grade
        fields = "__all__"

class VideoLessonSerializer(serializers.ModelSerializer):
    videourl = serializers.SerializerMethodField(source='video')

    def get_videourl(self, obj):
        request = self.context['request']
        print(obj)
        if obj.video.name and not obj.video.name.startswith('/static'):
            path = '/static/%s' % obj.video.name

            return request.build_absolute_uri(path)

    class Meta: 
        model = VideoLesson
        fields = "__all__"



class RatingSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Rating
        fields = "__all__"

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = "__all__"


class TopicSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Topic
        fields = "__all__"




class EnrolledSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Enrolled
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Answer
        fields = "__all__"

class UserTestSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many = True, read_only = True)
    class Meta:
        model= UserTest
        fields = "__all__"