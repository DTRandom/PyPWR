"""
MIT License

Copyright (c) 2018 Francesco Zimbolo a.k.a. DTRandom

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import config
import connection
import validators


class Userbot:

    def __init__(self, phone=None, host='api.pwrtelegram.xyz'):
        if not phone:
            phone = input("Insert your phone number: ")
        phone = phone.replace('+', '00')
        self._phone = phone
        if 'http' not in host:
            self._host = 'https://' + host
            if not validators.url(self._host):
                raise SyntaxError('Invalid Host')

    def log_in(self):
        self._token = connection.PWRTelegramApi(self._host
                                                ).phoneLogin(self._phone)
        print("LogIn: OK")

    def getMe(self):
        return connection.PWRTelegramApi.getMe()
