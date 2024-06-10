from email import message

from django.core.mail import send_mail
from django.core.mail import EmailMessage


def send_activation_code(email, code):
    message = f'Перейдите по данной ссылке для активации аккаунта: \n\n http://127.0.0.1:8000/api/v1/account/activate/{code}'

    email_message = EmailMessage(
        'Nedvizhimost',
        message,
        'iptest228228@gmail.com',
        [email],
    )

    email_message.attach_file('C:/Users/user/Desktop/project_x/emailimages/logo.png')

    email_message.send()


def send_forgot_password_code(email, code):
    send_mail(
        'Nedvizhimost',
        f'Вот ваш код для востоновления пароля, никому не показывайте его: {code}',
        'iptest228228@gmail.com',
        [email]
    )


