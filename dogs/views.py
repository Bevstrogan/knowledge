from winreg import DeleteValue

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from dogs.forms import DogForm, ParentForm, DogModeratorForm
from dogs.models import Dog, Parent
from dogs.services import get_dogs_from_cache


class DogListView(ListView):
    model = Dog

    def get_queryset(self):
        return get_dogs_from_cache()


class DogDetailView(DetailView, LoginRequiredMixin):
    model = Dog

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     if self.request.user == self.object.owner:
    #         self.object.views_field += 1
    #         self.object.save()
    #         return self.object
    #     raise PermissionDenied


class DogCreateView(CreateView, LoginRequiredMixin):
    model = Dog
    form_class = DogForm
    success_url = reverse_lazy("dogs:dogs_list")

    def form_valid(self, form):
        dog = form.save()
        user = self.request.user
        dog.owner = user
        dog.save()
        return super().form_valid(form)


class DogUpdateView(UpdateView, LoginRequiredMixin):
    model = Dog
    form_class = DogForm
    success_url = reverse_lazy("dogs:dogs_list")

    def get_success_url(self):
        return reverse("dogs:dogs_detail", args=[self.kwargs.get("pk")])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        DogFormset = inlineformset_factory(Dog, Parent, ParentForm, extra=1)
        if self.request.method == "POST":
            context_data["formset"] = DogFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = DogFormset(instance=self.object)
        return context_data

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return DogForm
        if user.has_perm("dogs.can_edit_breed")and user.has_perm("dogs.cand_edit_description"):
            return DogModeratorForm
        raise PermissionDenied

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )


class DogDeleteView(DeleteView):
    model = Dog
    success_url = reverse_lazy("dogs:dogs_list")
