from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "password",
        )

    def save(self, commit=True):
        user: CustomUser = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user
