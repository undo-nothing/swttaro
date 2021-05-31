import os
import ssl
import smtplib
from email import encoders
from email.mime.base import MIMEBase


class EmailBackend(object):
    """
    A wrapper that manages the SMTP network connection.
    """

    def __init__(self, host=None, port=None, username=None, password=None,
                 use_tls=None, fail_silently=False, use_ssl=None, timeout=None,
                 **kwargs):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.use_ssl = use_ssl
        self.timeout = timeout
        self.fail_silently = fail_silently

    @property
    def connection_class(self):
        return smtplib.SMTP_SSL if self.use_ssl else smtplib.SMTP

    def get_connection(self, *args, **kwargs):
        self.connection = self.connection_class(*args, **kwargs)

    def open(self):
        if self.connection:
            return False

        connection_params = {}
        if self.timeout is not None:
            connection_params['timeout'] = self.timeout

        self.get_connection(self.host, self.port, **connection_params)
        if self.use_tls:
            self.connection.starttls()

        self.connection.login(self.username, self.password)
        return True

    def close(self):
        """Closes the connection to the email server."""
        if self.connection is None:
            return
        try:
            try:
                self.connection.quit()
            except (ssl.SSLError, smtplib.SMTPServerDisconnected):
                self.connection.close()
            except smtplib.SMTPException:
                if self.fail_silently:
                    return
                raise
        finally:
            self.connection = None

    def send_messages(self, email_messages):
        """
        Sends one or more EmailMessage objects and returns the number of email
        messages sent.
        """
        if not email_messages:
            return

            new_conn_created = self.open()
            if not self.connection or new_conn_created is None:
                return
            num_sent = 0
            for message in email_messages:
                sent = self._send(message)
                if sent:
                    num_sent += 1
            if new_conn_created:
                self.close()
        return num_sent

    def _send(self, email_message):
        if not email_message.recipients():
            return False
        from_email = email_message.from_email
        recipients = [addr for addr in email_message.recipients()]
        message = email_message.message()
        try:
            self.connection.sendmail(from_email, recipients, message.as_bytes(linesep='\r\n'))
        except smtplib.SMTPException:
            if not self.fail_silently:
                raise
            return False
        return True


def get_attachments(file_list=None):
    attachments = []
    file_list = file_list if file_list else []
    for filepath in file_list:
        with open(filepath, 'rb') as f:
            filename = os.path.split(filepath)[1]
            mime = MIMEBase('text', 'txt', filename=filepath)
            mime.add_header('Content-Disposition', 'filepath', filename=filename)
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            attachments.append(mime)

    return attachments


def send_one_mail(subject, body, to, context=None, to_cc=None, to_bcc=None, attachments=None):
    '''
    attachments: must be value file path list
    '''
    from_email = 'test'
    if attachments:
        attachments = get_attachments(attachments)
    email_message = EmailBackend(subject, body, from_email,
                                 to=to, cc=to_cc, bcc=to_bcc,
                                 attachments=attachments)
    email_message.send()


def send_one_mail_to_self():
    """
    test email setting correct
    :return:
    """
    subject = 'Test Email'
    body = 'Test Email Body'
    to = 'test'
    print((to, subject, body))
    send_one_mail(subject, body, to)
