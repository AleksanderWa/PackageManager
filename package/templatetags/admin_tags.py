from django import template

register = template.Library()


@register.simple_tag
def row_css(cl, index):
    if not hasattr(cl.model_admin, "set_row_style"):
        return ""
    return cl.model_admin.set_row_style(cl.result_list[index], index)
