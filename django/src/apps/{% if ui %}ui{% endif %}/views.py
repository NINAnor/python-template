from typing import Self

from django.db.models import Model
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    TemplateView,
    UpdateView,
)
from django_filters.views import FilterMixin
from django_tables2 import SingleTableView

from .utils import get_deleted_objects


class FilterableSingleTableView(FilterMixin, SingleTableView):
    """
    Override get context data to avoid calling the view pagination
    """

    def get_context_data(
        self: Self,
        object_list: list[Model] = None,
        **kwargs,
    ) -> Context:
        # Create the filterset
        filterset_class = self.get_filterset_class()
        kwargs = {
            "data": self.request.GET or None,
            "request": self.request,
            "queryset": self.get_queryset(),
        }
        self.filterset = filterset_class(**kwargs)

        # Assign the result to object list
        if (
            not self.filterset.is_bound
            or self.filterset.is_valid()
            or not self.get_strict()
        ):
            self.object_list = self.filterset.qs
        else:
            self.object_list = self.filterset.queryset.none()

        queryset = object_list if object_list is not None else self.object_list
        context = {
            "paginator": None,
            "page_obj": None,
            "is_paginated": False,
            "object_list": queryset,
            "filter": self.filterset,
        }
        context.update(kwargs)

        # Using the filtered queryset populate the table
        table = self.get_table(**self.get_table_kwargs())
        context[self.get_context_table_name(table)] = table
        return context


class UINavigationMixin:
    active_dropdown = None
    active_route = None
    create_path = None
    delete_path = None

    def get_create_path(self: Self) -> str:
        if self.create_path:
            return reverse_lazy(self.create_path)
        return None

    def get_delete_path(self: Self) -> str:
        if self.create_path:
            return reverse_lazy(self.delete_path)
        return None

    def get_context_data(self: Self, **kwargs) -> Context:
        ctx = super().get_context_data(**kwargs)
        ctx["sidenav_active_dropdown"] = self.active_dropdown
        ctx["sidenav_active_route"] = self.active_route
        ctx["create_path"] = self.get_create_path()
        ctx["delete_path"] = self.get_delete_path()
        return ctx


class UITitleMixin:
    active_dropdown = None
    active_route = None

    def get_context_data(self: Self, **kwargs) -> Context:
        ctx = super().get_context_data(**kwargs)
        if self.model:
            ctx["title"] = self.model._meta.verbose_name_plural.title()
        elif self.queryset:
            ctx["title"] = self.queryset.model._meta.verbose_name_plural.title()
        else:
            ctx["title"] = ""
        return ctx


class UITemplateView(UINavigationMixin, TemplateView):
    pass


class UICreateView(UITitleMixin, UINavigationMixin, CreateView):
    template_name = "ui/create.html"


class UIDetailView(UITitleMixin, UINavigationMixin, DetailView):
    template_name = "ui/detail.html"


class UIListView(
    UITitleMixin,
    UINavigationMixin,
    FilterableSingleTableView,
):
    paginate_by = 30
    ordering = ("-id",)
    template_name = "ui/list.html"


class UIUpdateView(UITitleMixin, UINavigationMixin, UpdateView):
    template_name = "ui/update.html"
    readonly = False

    def get_context_data(self: Self, *args, **kwargs) -> Context:
        ctx = super().get_context_data(*args, **kwargs)
        ctx["readonly"] = self.readonly
        return ctx


class UIFormView(UITitleMixin, UINavigationMixin, FormView):
    template_name = "ui/form.html"

    def get_context_data(self: Self, **kwargs) -> Context:
        ctx = super().get_context_data(**kwargs)
        ctx["form_action"] = ""
        ctx["form_method"] = "post"
        return ctx


class UIActionView(DetailView):
    def get_redirect_url(self: Self) -> HttpResponse:
        if self.redirect_url:
            return self.redirect_url

        raise NotImplementedError("you must implement get_redirect_url")

    def get_success_url(self: Self, *args, **kwargs) -> str:
        if self.success_url:
            return self.success_url

        raise NotImplementedError("you must implement get_success_url")

    def do_action(self: Self, *args, **kwargs) -> HttpResponse:
        return HttpResponseRedirect(self.get_success_url(*args, **kwargs))

    def post(self: Self, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        return self.do_action(*args, **kwargs)

    def get(self: Self, *args, **kwargs) -> HttpResponse:
        return HttpResponseRedirect(self.get_redirect_url(*args, **kwargs))


class UIActionConfirmView(FormView):
    def get_redirect_url(self: Self) -> str:
        if self.redirect_url:
            return self.redirect_url

        raise NotImplementedError("you must implement get_redirect_url")

    def get_context_data(self: Self, **kwargs) -> Context:
        kwargs.setdefault("view", self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs

    def get_success_url(self: Self, *args, **kwargs) -> str:
        if self.success_url:
            return self.success_url

        raise NotImplementedError("you must implement get_success_url")

    def do_action(self: Self, *args, **kwargs) -> HttpResponse:
        return HttpResponseRedirect(self.get_success_url(*args, **kwargs))

    def post(self: Self, *args, **kwargs) -> HttpResponse:
        return self.do_action(*args, **kwargs)


class UIDeleteView(UITitleMixin, UINavigationMixin, DeleteView):
    template_name = "ui/delete.html"

    def get_context_data(self: Self, **kwargs) -> Context:
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context["deletable_objects"] = deletable_objects
        context["model_count"] = dict(model_count).items()
        context["protected"] = protected
        return context
