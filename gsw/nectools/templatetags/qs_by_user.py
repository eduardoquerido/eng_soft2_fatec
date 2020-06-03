from django import template

register = template.Library()


class ByUserNode(template.Node):
    def __init__(self, qs, user, var_name):
        self.qs = template.Variable(qs)
        self.user = template.Variable(user)
        self.var_name = var_name

    def render(self, context):
        qs = self.qs.resolve(context)
        user = self.user.resolve(context)
        context[self.var_name] = qs.by_user(user)
        return ''


@register.tag
def by_user(parser, token):
    bits = token.split_contents()
    if len(bits) < 4:
        raise template.TemplateSyntaxError(
            "'%s' takes at least three arguments"
            " (qs, user, var_name)" % bits[0]
        )
    qs = bits[1]
    user = bits[2]
    _as = bits[3]  # noqa
    var_name = bits[4]
    return ByUserNode(qs, user, var_name)
