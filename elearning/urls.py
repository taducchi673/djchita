from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
# router.register(prefix='categories', viewset=views.CategoryViewSet, basename='category')
# User
router.register(prefix='users', viewset=views.UserViewSet, basename='Users')
router.register(prefix='usertypes', viewset=views.UserTypeViewSet, basename='Usertypes')

# Course
router.register(prefix='grades', viewset=views.GradeViewSet, basename='grades')
router.register(prefix='subjects', viewset=views.SubjectViewSet, basename='subjects')
router.register(prefix='courses', viewset=views.CourseViewSet, basename='image_courses')
router.register(prefix='course-categories', viewset=views.CourseCategoryViewSet, basename='course-categories')
router.register(prefix='ratings', viewset=views.RatingViewSet, basename='course-ratings')

router.register(prefix='blogs', viewset=views.BlogViewSet, basename='image_category')
router.register(prefix='topics', viewset=views.TopicViewSet, basename='topics')


router.register(prefix='tests', viewset=views.TestViewSet, basename='Tests')
router.register(prefix='questions', viewset=views.QuestionViewSet, basename='Questions')
router.register(prefix='lessons', viewset=views.LessonViewSet, basename='lessons')
router.register(prefix='video-lessons', viewset=views.VideoLessonViewSet, basename='video-lessons')
router.register(prefix='notebook-lessons', viewset=views.NotebookLessonViewSet, basename='video-lessons')


router.register(prefix='comments', viewset=views.CommentViewSet, basename='comments')
router.register(prefix='likes', viewset=views.LikeViewSet, basename='likes')
router.register(prefix='chapters', viewset=views.ChapterViewSet, basename='chapter')
# router.register(prefix='usertests', viewset=views.UserTestViewSet, basename='usertest')









urlpatterns = [
    path('', include(router.urls))
    
]