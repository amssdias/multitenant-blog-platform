from django import template

register = template.Library()

@register.filter(name="add_class_if_error")
def add_class_if_error(field, css_class):
    """Adds a CSS class if the field has errors."""
    if field.errors:
        return field.as_widget(attrs={"class": field.field.widget.attrs.get("class", "") + " " + css_class})
    return field.as_widget()
