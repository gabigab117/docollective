from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField

from docollective.settings import TEST_MODE, ENV


class ExChangerSignupForm(UserCreationForm):
    if not TEST_MODE and not ENV == "DEV":
        captcha = ReCaptchaField()

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "first_name", "last_name", "type", "upper_size", "lower_size", "foot_size",
                  "favorite_color"]
