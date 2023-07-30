from django.urls import path

from accounts.views import *

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", ProfileCreateView.as_view(), name="profile-create"),
    path("settings/profile/<int:pk>/", UserDetailView.as_view(), name="profile-detail"),
    path("settings/profile/<int:pk>/update/", UserChangeView.as_view(), name="profile-update"),
    path("settings/profile/<int:pk>/update-password/", UserChangePasswordView.as_view(), name="update-password"),
    path(
        "settings/profile/<int:pk>/delete/", DeleteAccountView.as_view(), name="profile_delete"
    ),
    path("settings/profile/<int:pk>/lesson_count/", LessonCountView.as_view(), name="lesson_count"),
    path(
        "settings/profile/<int:pk>/lesson_count_filtered/", get_lessons_count_by_date_range,
        name="lesson_count_filtered"
    ),
    path("users/students/", StudentsListView.as_view(), name="students_list"),
    path("users/theachers/", TeachersListView.as_view(), name="teachers_list"),
    path("users/staff/", StaffListView.as_view(), name="staff_list"),
]
