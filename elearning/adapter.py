from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings



class DefaultAccountAdapterCustom(DefaultAccountAdapter):
    def send_email(self, template_prefix, email, context):
        context['activate_url'] = settings.URL_FRONT + "verify-email/?key" + context['key']
        msg = self.render_mail(template_prefix, email, context)
        msg.send()
        
