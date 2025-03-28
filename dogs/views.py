from winreg import DeleteValue

from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from dogs.forms import DogForm, ParentForm
from dogs.models import Dog, Parent


class DogListView(ListView):
    model = Dog


class DogDetailView(DetailView):
    model = Dog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_field += 1
        self.object.save()
        return self.object


class DogCreateView(CreateView):
    model = Dog
    form_class = DogForm
    success_url = reverse_lazy("dogs:dogs_list")


class DogUpdateView(UpdateView):
    model = Dog
    form_class = DogForm
    success_url = reverse_lazy("dogs:dogs_list")

    def get_success_url(self):
        return reverse("dogs:dogs_detail", args=[self.kwargs.get("pk")])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        DogFormset = inlineformset_factory(Dog, Parent, ParentForm, extra=1)
        if self.request.method == "POST":
            context_data["formset"] = DogFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = DogFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class DogDeleteView(DeleteView):
    model = Dog
    success_url = reverse_lazy("dogs:dogs_list")
