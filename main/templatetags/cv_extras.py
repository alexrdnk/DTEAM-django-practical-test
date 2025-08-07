from django import template

register = template.Library()


@register.filter
def split(value, arg):
    """
    Split a string by the given delimiter.
    Usage: {{ value|split:", " }}
    """
    return value.split(arg)


@register.filter
def get_skills_preview(value, max_skills=3):
    """
    Get a preview of skills, showing only the first few.
    Usage: {{ cv.skills|get_skills_preview:3 }}
    """
    skills = value.split(', ')
    if len(skills) <= max_skills:
        return skills
    return skills[:max_skills] 