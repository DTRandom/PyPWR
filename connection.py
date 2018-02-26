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
from http import client
import json
from user import User

class PWRTelegramApi:

    def __init__(self, host):
        self._host = host
        self._api = client.HTTPSConnection(host)
        try:
            api.request("HEAD", "/")
        except Exception:
            raise ConnectionError('Could not connect to Host')

    def phoneLogin(self, phone):
        request = "/phonelogin?phone={phone}".format(
            phone=phone
        )
        self._api.request(request)
        result = self._api.getresponse()
        response = json.load(result.read().decode('utf-8'))
        if response["ok"]:
            self._tempcode = response["result"]
            self.completePhoneLogin()
        else:
            raise SyntaxError("Can't login with that number, is it correct?")

    def completePhoneLogin(self):
        request = "/user{user}/completephonelogin?code={code}".format(
            user=self._tempcode, code=input("Insert the code you" +
                                            "recieved from Telegram: ")
        )
        self._api.request(request)
        result = self._api.getresponse()
        response = json.load(result.read().decode('utf-8'))
        if response["ok"]:
            self._token = response["result"]
            return response["result"]
        elif response["error_code"] == "401":
            self.complete2FALogin()
        else:
            print("Invalid Telegram Code")
            self.completePhoneLogin()

    def complete2FALogin(self):
        request = "/user{user}/complete2FALogin?password={password}".format(
            user=self._tempcode, password=input("Insert your password")
        )
        self._api.request(request)
        result = self._api.getresponse()
        response = json.load(result.read().decode('utf-8'))
        if response["ok"]:
            self._token = response["result"]
            return response["result"]
        else:
            print("Invalid password")
            self.complete2FALogin()

    def getMe(self):
        request = "/user{user}/getMe".format(user=self._token)
        self._api.request(request)
        result = self._api.getresponse()
        response = json.load(result.read().decode('utf-8'))
        if response["ok"]:
            if 'username' in response:
                username = response["username"]
            else:
                username = None
                        first_name = response[]
            return User(user_id=response["id"], username=response["username"])
