from django.urls import path, re_path
from django.views.i18n import JavaScriptCatalog


from KaifSchool.views.exercise import *
from KaifSchool.views.lesson import *
from KaifSchool.views.task import *
from KaifSchool.views.theme import *

from KaifSchool.views.base import *

urlpatterns = [
    path("", IndexView.as_view(), name='index'),
    path('jso18n', JavaScriptCatalog.as_view(), name='js'),
    path('lesson/<int:pk>/', LessonDetailView.as_view(), name='lesson'),
    path('lesson/create/<int:pk>', LessonCreate.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/update/', LessonUpdate.as_view(), name='lesson_update'),
    path('lesson/update/theme/', LessonUpdateTheme.as_view(), name='lesson_update_theme'),
    path('lesson/<int:pk>/update/status/', LessonUpdateStatus.as_view(), name='lesson_update_status'),
    path('lesson/<int:pk>/delete/', LessonDelete.as_view(), name='lesson_delete'),
    path('lesson/<int:id>/data/', get_meeting_data, name='lesson_data'),
    path('lesson/list/education/', LessonsEducationView.as_view(), name='education'),
    path('theme/list/catalog/', ThemeCatalog.as_view(), name='theme_list_catalog'),
    path('theme/list/personal/', ThemePersonal.as_view(), name='theme_list_personal'),
    path('theme/<int:pk>/', ThemeDetail.as_view(), name='theme_detail'),
    path('theme/create/', ThemeCreate.as_view(), name='theme_create'),
    path('theme/<int:pk>/update/', ThemeUpdate.as_view(), name='theme_update'),
    path('theme/<int:pk>/delete/', ThemeDelete.as_view(), name='theme_delete'),
    path('theme/<int:pk>/create/', ExerciseCreate.as_view(), name='exercise_create'),
    path('theme/<int:pk>/exercise/update/', ExerciseUpdate.as_view(), name='exercise_update'),
    path('theme/<int:theme_pk>/exercise/<int:pk>/delete/', ExerciseDelete.as_view(), name='exercise_delete'),
    path('ex/<int:exercise_id>/tasks/', TaskList.as_view(), name='task_list'),
    path('ex/<int:exercise_id>/task/create/', TaskCreate.as_view(), name='task_create'),
    path('ex/<int:exercise_id>/task/<int:pk>/update/', TaskUpdate.as_view(), name='task_update'),
    path('ex/<int:exercise_id>/task/<int:task_id>/delete/', delete_task, name='task_delete'),
    path('ex/<int:exercise_id>/task/<int:pk>/answer/delete', delete_answer, name='delete_answer'),
]
