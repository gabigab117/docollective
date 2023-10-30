from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, forms
from captcha.fields import ReCaptchaField


class ExChangerSignupForm(UserCreationForm):
    captcha = ReCaptchaField()

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "first_name", "last_name", "type", "size", "favorite_color"]
