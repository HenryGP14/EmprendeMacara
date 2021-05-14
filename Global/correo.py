from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

class Correo:
    
    def __init__(self, request):
        self.request = request
    
    def send(self, unUsuarioAdmin, destinatario, asunto, template, context):
        try:
            settings.EMAIL_HOST_USER = unUsuarioAdmin.correo
            settings.EMAIL_HOST_PASSWORD = unUsuarioAdmin.credenciales
            tplCorreo = get_template(template)
            content = tplCorreo.render(context)
            email = EmailMultiAlternatives(asunto, " ", settings.EMAIL_HOST_USER, [destinatario])
            email.attach_alternative(content, "text/html")
            email.send()
            return True
        except Exception as e:
            return False