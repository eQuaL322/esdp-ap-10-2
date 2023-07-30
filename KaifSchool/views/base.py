from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

from KaifSchool.forms import LessonForm
from KaifSchool.models import Lesson, Theme
from accounts.forms import LoginForm
from json import dumps


class IndexView(TemplateView):
    template_name = "index.html"
    form = LoginForm

    def get(self, request, *args, **kwargs):
        all_lessons = Lesson.objects.all()
        data = []
        for lesson in all_lessons:
            if lesson.theme:
                title = lesson.theme.title
            else:
                title = 'No theme'
            data.append({
                "title": title,
                'id': lesson.pk,
                'start': lesson.lesson_date.isoformat(),
                'end': (lesson.lesson_date + lesson.duration).isoformat(),
            })
        data = dumps(data)
        form = self.form()
        lesson_form = LessonForm()
        all_lessons = Lesson.objects.all()
        user = get_user_model()
        themes = Theme.objects.all()
        teachers = user.objects.filter(role='Teacher')
        students = user.objects.filter(role='Student')
        context = {
            'data': data,
            'form': form,
            'lesson_form': lesson_form,
            'lessons': all_lessons,
            'themes': themes,
            'teachers': teachers,
            'students': students
        }
        return self.render_to_response(context)
