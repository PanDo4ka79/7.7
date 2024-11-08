from django import template

register = template.Library()

CENSOR_WORDS = ['запрещенное', 'слово']

@register.filter(name='censor')
def censor(value):
    text = value
    for word in CENSOR_WORDS:
        text = text.replace(word, '*' * len(word))
    return text

