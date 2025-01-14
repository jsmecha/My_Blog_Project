from django import template

register = template.Library()

@register.filter
def range_filter(value):
    max_length = 300
    filtered_value = value
    if len(value) > max_length:
        filtered_value = f"{value[:300]}...."
    
    return filtered_value

