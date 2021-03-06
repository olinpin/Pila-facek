from django import template

register = template.Library()

@register.filter(name="has_group")
def has_group(user, group_name):
    if user.is_superuser:
        return user.is_superuser
    return user.groups.filter(name=group_name).exists()

@register.filter(name="group")
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()