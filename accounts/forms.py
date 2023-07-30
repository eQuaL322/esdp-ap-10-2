from django import forms
from django.contrib.auth import get_user_model

from KaifSchool.models import LessonCount


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        required=True,
        strip=False,
    )
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        required=True,
        strip=False,
    )

    class Meta:
        model = get_user_model()
        fields = (
            'first_name', 'last_name', 'email', 'role', 'timezone', 'phone', 'password', 'password_confirm')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].widget.attrs.update({"placeholder": "+XXXXXXXXXXX"})
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
        self.fields["role"].widget.attrs.update({"class": "form-select form-control"})
        self.fields["timezone"].widget.attrs.update({"class": "form-select form-control"})

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not str(phone).startswith('+77'):
            raise forms.ValidationError(
                'Набраный вами номер не соотвествует коду страны (Казахстан), пример номера +77052356678')
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают!")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        user.username = self.cleaned_data.get("email")
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.CharField(
        required=True,
        label="",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "style": "border: 1px solid #e6e6eb; border-left: 0;",
                   "placeholder": "Email address"}
        ),
    )
    password = forms.CharField(
        required=True,
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "style": "border: 1px solid #e6e6eb; border-left: 0;",
                   "placeholder": "Password"}
        ),
    )


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'first_name', 'last_name', 'email', 'avatar', 'timezone', 'phone', 'bio_text', 'role'
        )
        widgets = {
            'avatar': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.label = ""

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get("email")
        if commit:
            user.save()
        return user


class UserChangePasswordForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        required=True,
        strip=False,
    )
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        required=True,
        strip=False,
    )

    class Meta:
        model = get_user_model()
        fields = ('password', 'password_confirm')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.label = ""

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают!")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user


class LessonCountForm(forms.ModelForm):
    class Meta:
        model = LessonCount
        fields = ('balance',)
