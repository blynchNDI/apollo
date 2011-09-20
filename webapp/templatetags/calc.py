from django import template

register = template.Library()

@register.filter(name='percentage')  
def percentage(fraction, population):
    try:
        return "%.1f%%" % ((float(fraction) / float(population)) * 100)
    except ValueError:
        return '0%'
    except ZeroDivisionError:
        return "0%"

