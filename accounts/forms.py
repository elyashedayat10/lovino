from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("phone_number",)

    # def clean(self):
    #     cleand_data = super(UserCreationForm, self).clean()
    #     password = cleand_data["password"]
    #     password_confirm = cleand_data["password_confirm"]
    #     if (password and password_confirm) and (password_confirm != password_confirm):
    #         raise ValidationError("unmatched password")
    #     return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you can change password using <a href="../password/">this form</a>.'
    )

    class Meta:
        model = User
        fields = (
            "phone_number",
            "password",
        )
