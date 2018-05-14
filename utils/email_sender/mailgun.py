import requests

import utils.email_sender.mailgun_constants as MailGunConstants


class MailGun(object):
    """This class allows the user to send emails using the MailGun API"""

    @staticmethod
    def send_email(email, subject, body):
        """send_email(str, str, str) -> return str

           This method uses the mailgun API to allow
           the user to send emails

           :param

              `email`: The receiptant email address
              `subject`: The subject of the email
              `body`: The email to be sent to the user

           :returns
              Returns a 'request [200]' if the message was sent
              else returns a 'request [400]' if the message failed
        """
        return requests.post(
            MailGunConstants.URL,
            auth=("api", MailGunConstants.API_KEY),
            data={"from": MailGunConstants.FROM,
                  "to": [email],
                  "subject": subject,
                  "text": body,
                  }
        )


