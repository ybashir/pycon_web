from django.template import Library
from django.template.loader import get_template

register = Library()


@register.simple_tag(takes_context=True)
def render_field(context, field, template="generic/form_field.html"):
    """
    Renders fields for a form with an optional template choice.
    """
    context["field"] = field
    return get_template(template).render(context)


@register.simple_tag
def list_iterator(form):
    return list(form)
