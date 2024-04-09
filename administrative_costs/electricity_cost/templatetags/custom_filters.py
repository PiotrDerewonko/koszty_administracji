# custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_data(data_dict, counter_name):
    return data_dict.get(f'data_{counter_name}')

@register.filter
def get_image(data_dict, counter_name):
    return data_dict.get(f'image_{counter_name}')
