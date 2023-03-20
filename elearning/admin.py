from django.contrib import admin
from .models import * 


# Register your models here.
# admin.registe
admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(CourseCategory)
admin.site.register(Lesson)
admin.site.register(NotebookLesson)
admin.site.register(Question)
admin.site.register(Test)
admin.site.register(UserType)
admin.site.register(VideoLesson)
admin.site.register(Topic)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Enrolled)
admin.site.register(Chapter)
admin.site.register(Answer)
admin.site.register(UserTest)


