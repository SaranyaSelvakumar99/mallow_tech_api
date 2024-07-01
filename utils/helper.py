from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from mallowtech_store import settings
def send_custom_mail(message, recepiants, subject,template):
    
    """
    Sending Custom mail fucntion which is callable
    """
    
    try:
        email_html_message = render_to_string(template, message)
        email = EmailMultiAlternatives(subject, email_html_message, settings.DEFAULT_FROM_EMAIL, [recepiants])
        email.attach_alternative(email_html_message, "text/html")
        email.send()
    except Exception as e:
        pass
    
def sum_of_denomination(request_data):
    denominations = {
        500: request_data.get('count_500', 0),
        100: request_data.get('count_100', 0),
        50: request_data.get('count_50', 0),
        20: request_data.get('count_20', 0),
        10: request_data.get('count_10', 0),
        5: request_data.get('count_5', 0),
        2: request_data.get('count_2', 0),
        1: request_data.get('count_1', 0),
        }
    
    return denominations