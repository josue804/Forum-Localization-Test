from __future__ import unicode_literals

from django.db import models
from misago.users.models.user import User, UserManager

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from misago.categories.models import Category, RoleCategoryACL, CategoryRole
from misago.acl.models import Role
from django.utils.text import slugify

@receiver(post_save, sender=Category)
def my_handler(sender, **kwargs):
    category = kwargs['instance']
    if not category.parent.parent:
        role = Role.objects.create(name=category.name + ' Member')
        admin_role = Role.objects.get(name='Moderator')
        member_category_role = CategoryRole.objects.get(name="Start and reply threads")
        admin_category_role = CategoryRole.objects.get(name="Start and reply threads, make polls")

        RoleCategoryACL.objects.create(role=role, category=category, category_role=member_category_role)
        RoleCategoryACL.objects.create(role=admin_role, category=category, category_role=admin_category_role)


        child_category = category.children.create(name="General", slug=slugify(category.name + "-General"))

        RoleCategoryACL.objects.create(role=role, category=child_category, category_role=member_category_role)
        RoleCategoryACL.objects.create(role=admin_role, category=child_category, category_role=admin_category_role)

## Need to handle category deletion triggering permissions deletions

# Create your models here.
class User(User):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    objects = UserManager()

#Category.objects.exclude(id__in=[1,2]).delete()
