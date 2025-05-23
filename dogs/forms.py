from django.core.exceptions import ValidationError
from django.utils import timezone

from django.forms import ModelForm, BooleanField

from dogs.models import Dog, Parent


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class DogForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Dog
        exclude = ("views_field", "owner")


class DogModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Dog
        fields = ("description", "breed")


class ParentForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Parent
        fields = "__all__"

    def clean_year_born(self):
        year_born = self.cleaned_data["year_born"]
        current_year = timezone.now().year
        time_delta = current_year - year_born
        if time_delta >= 100:
            raise ValidationError("Собаки столько не живут")
        else:
            return year_born
