import smtplib
import traceback
from email.message import EmailMessage


def send_feedback_email(subject, message, user=None):
    print("mail fonk: ")
    print(message)

    mail_list = ["ibrahimsevkibayrakdar@gmail.com", "info@craniocatch.com",
                 "batuhanaltog88@gmail.com", "ahmetresul159@gmail.com"]

    try:
        mail_server = "mail.craniocatch.com"
        mail_username = 'teknik@craniocatch.com'
        mail_password = ".=4-CzHB6yvtM20="

        msg = EmailMessage()
        msg.set_content(message)
        msg["Subject"] = subject
        msg["From"] = mail_username
        msg["To"] = ", ".join(mail_list)
        server = smtplib.SMTP(mail_server, 587)
        server.login(mail_username, mail_password)
        server.send_message(msg)
        server.quit()
        print("Information mail sent.")
        return True
    except Exception as exc:
        traceback.print_exc()
        print(f"Informatin mail could not be sent. Message: {exc}")
        return False
