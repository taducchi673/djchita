from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser


# Create your models here.


class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserType(models.Model):
    usertype =  models.CharField(max_length = 100, null = True, unique = True)
    
    def __str__(self):
        return self.usertype


class Subject(ModelBase):
    subject_name = models.CharField(max_length = 150)

class Grade(ModelBase):
    grade = models.CharField(max_length = 100)

class User(AbstractUser):
    avatar = models.ImageField(null=True, upload_to='users/%Y/%m')
    usertype = models.ForeignKey(UserType, on_delete = models.CASCADE, null = True, related_name = "user_usertype")
    discription = RichTextField(null = True, blank= True)    
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE, null = True, blank = True)


class CourseCategory(ModelBase):
    course_category = models.CharField(max_length = 100)



class Course(ModelBase):
    name = models.CharField(max_length= 100)
    subject = models.ForeignKey(Subject, null = True, on_delete = models.CASCADE, related_name = "subject_courses")
    grade = models.ForeignKey(Grade, null = True, on_delete = models.CASCADE, related_name = "grade_courses")
    image = models.ImageField(upload_to = "courses/%Y/%m", null = True)
    teacher = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    description = RichTextField(null = True)

class Chapter(ModelBase): 
    name = models.CharField(max_length = 100, unique = True, null = True)
    course = models.ForeignKey(Course, on_delete = models.CASCADE, null = True, related_name = "course_chapter")
    
class Lesson(ModelBase):
    name = models.CharField(max_length = 100, unique = True, null = True)
    chapter = models.ForeignKey(Chapter, on_delete = models.CASCADE, null = True, related_name = "chapter_lesson")
    class Meta: 
        unique_together = (("chapter", "name")) 


class NotebookLesson(ModelBase):
    name = models.CharField(max_length = 100, unique = True, null = True)
    lesson = models.ForeignKey(Lesson, null = True, on_delete = models.CASCADE, related_name = "lesson_notebooklesson")
    content = RichTextField(null= True)

class VideoLesson(ModelBase):
    name = models.CharField(max_length = 100, unique = True, null = True)
    lesson = models.ForeignKey(Lesson, null = True, on_delete = models.CASCADE, related_name = "lesson_videolesson")
    description = RichTextField(null = True)
    video = models.FileField(upload_to ="video_uploaded/%Y/%m", null = True)

class Question(ModelBase):
    question = RichTextField(null = True)
    answer1 = models.CharField(max_length = 1000, null = True)
    answer2 = models.CharField(max_length = 1000, null = True)
    answer3 = models.CharField(max_length = 1000, null = True)
    answer4 = models.CharField(max_length = 1000, null = True)
    correct_answer = models.CharField(max_length = 1000, null = True)

    class Meta: 
        unique_together = ("question", "answer1", "answer2", "answer3", "answer4", "correct_answer")

class Test(ModelBase):
    name = models.CharField(max_length = 100, unique = True, null = True)
    lesson = models.ForeignKey(Lesson, null = True, on_delete = models.CASCADE, related_name= "lesson_test")
    questions = models.ManyToManyField(Question, null = True)
    time_limit = models.IntegerField(null = True)

    class Meta:
        unique_together = [("name", "lesson")]

class Enrolled(ModelBase):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    enrolled = models.BooleanField(default = True)
    

    class Meta: 
        unique_together = ("user", "course")



class Topic(ModelBase):
    topic_name = models.CharField(max_length = 100)


class Blog(ModelBase):
    name = models.CharField(max_length = 100, unique = True, null = True)
    content = RichTextField(null = True)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE, null = True, blank = True, related_name = "blogs_topic")
    author = models.ForeignKey(User,on_delete = models.CASCADE, null = True, blank = True, related_name = "blog_author" )
    image = models.ImageField(upload_to = "blogs/%Y/%m", null = True)


class Rating(ModelBase):
    blog = models.ForeignKey(Blog, blank = True, null=True, on_delete = models.CASCADE, related_name='blog_ratings')
    videolesson = models.ForeignKey(VideoLesson, blank = True, null=True, on_delete = models.CASCADE, related_name='videolesson_ratings')
    notebooklesson = models.ForeignKey(NotebookLesson, blank = True, null=True, on_delete = models.CASCADE, related_name='notebooklesson_ratings')
    question = models.ForeignKey(Question, blank = True, null=True, on_delete = models.CASCADE, related_name='question_ratings')
    test = models.ForeignKey(Test, blank = True, null=True, on_delete = models.CASCADE, related_name='test_ratings')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='user_ratings')
    rating = models.FloatField(default = 0)

    
class Comment(ModelBase):
    content = models.TextField()
    blog = models.ForeignKey(Blog, blank = True, null=True, on_delete = models.CASCADE, related_name='blog_comments')
    videolesson = models.ForeignKey(VideoLesson, blank = True, null=True, on_delete = models.CASCADE, related_name='videolesson_comments')
    notebooklesson = models.ForeignKey(NotebookLesson, blank = True, null=True, on_delete = models.CASCADE, related_name='notebooklesson_comments')
    question = models.ForeignKey(Question, blank = True, null=True, on_delete = models.CASCADE, related_name='question_comments')
    test = models.ForeignKey(Test, blank = True, null=True, on_delete = models.CASCADE, related_name='test_comments')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='user_comments')
    course = models.ForeignKey(Course, blank = True, null=True, on_delete = models.CASCADE, related_name='course_comments')
    comment = models.ForeignKey('self', blank = True, null=True, on_delete = models.CASCADE, related_name='comment_comments')

class Like(ModelBase):
    liked = models.BooleanField(max_length = 100, unique = True, blank = True, null=True)
    blog = models.ForeignKey(Blog, blank = True, null=True, on_delete = models.CASCADE, related_name='blog_likes')
    videolesson = models.ForeignKey(VideoLesson, blank = True, null=True, on_delete = models.CASCADE , related_name='videolesson_likes')
    notebooklesson = models.ForeignKey(NotebookLesson, blank = True, null=True, on_delete = models.CASCADE , related_name='notebooklesson_likes')
    question = models.ForeignKey(Question, blank = True, null=True, on_delete = models.CASCADE , related_name='blog_likes')
    test = models.ForeignKey(Test, blank = True, null=True, on_delete = models.CASCADE , related_name='blog_likes')
    user = models.ForeignKey(User, on_delete = models.CASCADE , related_name='blog_likes')
    class Meta: 
        unique_together = (("user", "blog"), ("user", "test"))

class Answer(ModelBase):
    questionid = models.CharField(max_length = 100)
    answer = models.CharField(max_length = 100)

class UserTest(ModelBase):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null = True)
    test = models.ForeignKey(Test, on_delete = models.CASCADE, null = True)
    # result = models.IntegerField(null = True)
    answers = models.ManyToManyField(Answer, null = True)
    class Meta: 
        unique_together = (("user", "test"))

