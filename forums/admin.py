# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ombucore import admin
from ombucore.admin.sites import AdminCentralBaseView
from ombucore.admin.form_base import ModelFormBase
from ombucore.admin.forms import ModelMultipleChoiceWidget, ModelMultipleChoiceField
from ombucore.admin.views import AddView
from ombucore.menus.admin import MenuAdmin
from ombucore.pages import admin as pages_admin
from forums import models
import django_filters
from misago.users.forms.admin import NewUserForm, UserBaseForm
from misago.categories.forms import CategoryFormBase
from misago.categories.models import Category
from misago.users.djangoadmin import UserAdminModel
from django.http import HttpResponseRedirect
from django.contrib import messages
from django import forms
from mptt.forms import TreeNodeChoiceField, TreeNodeMultipleChoiceField
from misago.acl.models import Role


### Category Admin
class CategoryForm(CategoryFormBase):

    parent = TreeNodeChoiceField(
                label="Parent category",
                queryset=Category.objects.all(),
                initial=Category.objects.get(name="Root"),
                empty_label=None,
            )

    class Meta:
        fields = CategoryFormBase.Meta.fields + ['parent',]
        fieldsets = (
            ('Basic', {'fields': ('parent', 'name', 'description', 'css_class',
                                'is_closed', 'require_threads_approval',
                                'require_replies_approval', 'require_edits_approval',
                                'prune_started_after', 'prune_replied_after',
                                'archive_pruned_in',
            )}),
        )

# class CategoryAddView(AddView):
#     form_class = CategoryForm
#     success_message = '%(username)s was created successfully'
#
#     def form_valid(self, form):
#         if form.is_valid():
#             new_user = models.Category.objects.create_user(
#                 form.cleaned_data['username'],
#                 form.cleaned_data['email'],
#                 form.cleaned_data['new_password'],
#                 title=form.cleaned_data['title'],
#                 rank=form.cleaned_data.get('rank'),
#                 joined_from_ip=self.request.user_ip,
#                 set_default_avatar=True
#             )
#             new_user.first_name = form.cleaned_data['first_name']
#             new_user.last_name = form.cleaned_data['last_name']
#             new_user.save()
#
#             self.submitted_successfully = True
#
#             success_message = self.get_success_message(form.cleaned_data)
#             if success_message:
#                 messages.success(self.request, success_message)
#
#             form_class = self.get_form_class()
#             fkwargs = self.get_form_kwargs()
#             fkwargs.pop('data')
#             fkwargs.pop('files')
#             new_form = form_class(**fkwargs)
#             return self.render_to_response(self.get_context_data(form=form))

class CategoryFilterSet(admin.views.FilterSet):
    search = django_filters.CharFilter(
                    name='username',
                    lookup_expr='icontains',
                    help_text='',
                )

    class Meta:
        fields = ['search',]


class CategoryAdmin(admin.ModelAdmin):
    form_class = CategoryForm
    filterset_class = CategoryFilterSet
    list_display = [
        ('name', 'Name'),
    ]

    class Meta:
        verbose_name = "ERO"



admin.site.register(models.Category, CategoryAdmin)


### User Admin
class UserForm(NewUserForm):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'username', 'rank', 'title', 'roles', 'email', 'new_password',
        )
        fieldsets = (
            ('Basic', {'fields': ('first_name', 'last_name', 'username', 'rank', 'title', 'roles', 'email', 'new_password',)}),
        )

        widgets = {
            'roles': forms.widgets.CheckboxSelectMultiple()
        }

class UserAddView(AddView):
    form_class = UserForm
    success_message = '%(username)s was created successfully'

    def form_valid(self, form):
        if form.is_valid():
            new_user = models.User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['new_password'],
                title=form.cleaned_data['title'],
                rank=form.cleaned_data.get('rank'),
                joined_from_ip=self.request.user_ip,
                set_default_avatar=True
            )
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()

            self.submitted_successfully = True

            success_message = self.get_success_message(form.cleaned_data)
            if success_message:
                messages.success(self.request, success_message)

            form_class = self.get_form_class()
            fkwargs = self.get_form_kwargs()
            fkwargs.pop('data')
            fkwargs.pop('files')
            new_form = form_class(**fkwargs)
            return self.render_to_response(self.get_context_data(form=form))

class UserFilterSet(admin.views.FilterSet):
    search = django_filters.CharFilter(
                    name='username',
                    lookup_expr='icontains',
                    help_text='',
                )

    class Meta:
        fields = ['search',]


class UserAdmin(admin.ModelAdmin):
    form_config = {
        'fields': ( 'first_name', 'last_name', 'username', 'email',
                    'rank', 'roles', 'is_staff', 'is_superuser',
                    'is_avatar_locked', 'avatar_lock_user_message', 'avatar_lock_staff_message',
                    'is_signature_locked', 'signature_lock_user_message', 'signature_lock_staff_message',
                    'subscribe_to_started_threads', 'subscribe_to_replied_threads', 'is_active_staff_message', 'is_active',
        ),
        'fieldsets': (
            ('Basic', {'fields': ('first_name', 'last_name', 'username', 'email',)}),
            ('Permissions', {'fields': ('rank', 'roles', 'is_staff', 'is_superuser',)}),
            ('Locks', {'fields': ('is_avatar_locked', 'avatar_lock_user_message', 'avatar_lock_staff_message',
                                    'is_signature_locked', 'signature_lock_user_message', 'signature_lock_staff_message',
            )}),
            ('Status', {'fields': ('subscribe_to_started_threads', 'subscribe_to_replied_threads', 'is_active_staff_message', 'is_active',)}),
        ),
        'widgets' : {
            'roles': forms.widgets.CheckboxSelectMultiple()
        }
    }

    filterset_class = UserFilterSet
    list_display = [
        ('full_name', 'Name'),
        ('username', 'Username'),
        ('email', 'Email'),
        ('rank', 'Rank'),
    ]
    add_view = UserAddView

    def full_name(self, user):
        return user.first_name + ' ' + user.last_name

admin.site.register(models.User, UserAdmin)
