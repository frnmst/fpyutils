#
# notify.py
#
# Copyright (C) 2017-2020 frnmst (Franco Masotti) <franco.masotti@live.com>
#
# This file is part of fpyutils.
#
# fpyutils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# fpyutils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fpyutils.  If not, see <http://www.gnu.org/licenses/>.
#
"""Functions on notifications."""

import smtplib
import ssl
from email.utils import formatdate
from email.mime.text import MIMEText
import requests
from .path import add_trailing_slash


def send_email(message: str, smtp_server: str, port: int, sender: str,
               user: str, password: str, receiver: str, subject: str):
    r"""Send an email.

    :parameter message: the body of the message.
    :parameter smtp_server: the address of the sending server.
    :parameter port: the port of the sending server.
    :parameter sender: the email of the sender.
    :parameter user: the username of the sender.
    :parameter password: the password of the sender.
    :parameter receiver: the email of the receiver.
    :parameter subject: the subject field of the email.
    :type message: str
    :type smtp_server: str
    :type port: int
    :type sender: str
    :type user: str
    :type password: str
    :type receiver: str
    :type subject: str
    :raises: a built-in exception.
    """
    # https://stackoverflow.com/questions/36832632/sending-mail-via-smtplib-loses-time
    #
    # Copyright (C) 2016 tfv @ Stack Overflow (https://stackoverflow.com/a/36834904)
    # Copyright (C) 2017 recolic @ Stack Overflow (https://stackoverflow.com/a/36834904)
    # Copyright (C) 2020 Franco Masotti <franco.masotti@live.com>
    #
    # This script is licensed under a
    # Creative Commons Attribution-ShareAlike 4.0 International License.
    #
    # You should have received a copy of the license along with this
    # work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg['Date'] = formatdate(localtime=True)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
            smtp_server, port, context=context) as conn:
        conn.login(user, password)
        conn.sendmail(sender, receiver, msg.as_string())


def send_gotify_message(url: str,
                        token: str,
                        message: str = 'message',
                        title: str = 'title',
                        priority: int = 5):
    r"""Send a notification to a gotify server.

    :parameter url: the URL of the Gotify server
    :parameter token: the APP token
    :parameter message: the message title.
        Defaults to ``message``.
    :parameter title: the text of the message
        Defaults to ``title``.
    :parameter priority: the message priority.
        Defaults to ``5``.
    :type url: str
    :type token: str
    :type message: str
    :type title: str
    :type priority: int
    :raises: a requests or a built-in exception.
    """
    full_url = add_trailing_slash(url) + 'message?token=' + token

    payload = {
        'title': title,
        'message': message,
        'priority': priority,
    }

    return requests.post(full_url, json=payload)


if __name__ == '__main__':
    pass
