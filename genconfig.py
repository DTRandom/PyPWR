"""
MIT License

Copyright (c) 2017 Application-And-Bots-Developing

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
import validators
from http import client
import json
import re
pn = re.compile('[^\d]')


def gen_configredis():
    rhost = input("insert redis host") or "127.0.0.1"
    rport = input("insert redis port") or 6379
    assert int(rport), "The redis port must be an integer"
    rdb = input("insert the redis database") or 1
    rpassword = input("insert redis password") or None
    import redis
    try:
        r = redis.StrictRedis(host=rhost,
                              port=rport,
                              db=rdb,
                              password=rpassword)
    except redis.ConnectionError:
        print('Redis connection error')
        return gen_configredis()

    return {"host":rhost,"port":rport,
            "db":rdb,"password":rpassword}


def gen_configmariadb():
    mariahost = input("insert mariadb host") or '127.0.0.1'
    mariaport = input("insert mariadb port") or 3306
    assert int(mariaport), "The mariadb port must be an integer"
    mariauser = input("insert mariadb user") or "root"
    mariapassword = input("insert mariadb password") or "root"
    mariadb = input("insert mariadb database") or 'telegrambot'
    try:
        import MySQLdb
        cnx = MySQLdb.connect(user=mariauser,
                              password=mariapassword,
                              host=mariahost,
                              port=mariaport)
        cursor = cnx.cursor()
        cursor.execute("SELECT VERSION()")
    except Exception:
        print("error connection mariadb")
        return gen_configmariadb()
    create = input("create table mariadb?")
    control = True
    while control:
        if create.upper() == "YES":
            control = False
            print('create the db')
            try:
                with open('./data/sql/createtable.sql', 'r') as sqlfile:
                    cursor.execute(sqlfile.read().format(db=mariadb))
            except Exception:
                print("error create database")
        elif create.upper() == "NO":
            control = False
            print('dont create the db')
        else:
            create = input("insert yes or no")
    cursor.close()
    cnx.commit()
    cnx.close()
    return {"host":mariahost,"port":mariaport,
            "db":mariadb,"user":mariauser,"password":mariapassword}


def gen_configpwrt():
    a = input("use pwrt? [YES or NO]") or None
    control = True
    while control:
        if a is None or a.upper() == "NO":
            return {"host":None,"token":None}
        elif a.upper() == "YES":
            control = False
        else:
            a = input("use pwrt? [YES or NO]") or None
    hostapi = hostapipwrt()
    token = tokenpwrt(hostapi)
    return {"host":hostapi,"token":token}


def hostapipwrt():
    hostapi = input("insert host api pwrtelegram:")
    if "http" not in hostapi:
        hostapip = "https://" + hostapi
    else:
        hostapip = hostapi.replace("http://", '').replace("https://", '')
    if validators.url(hostapip):
        try:
            api = client.HTTPSConnection(hostapi)
            api.request("HEAD", "/")
            return hostapi
        except Exception:
            print("connessione non riuscita")
            return hostapipwrt()
    else:
        print("inserire un host valido")
        return hostapipwrt()


def tokenpwrt(hostapi, host=None):
    if not host:
        host = input("create new account (yes or no):")
    if host.upper() == "YES":
        codeprov = numberpwrt(hostapi)
        return codeloginpwrt(codeprov, hostapi)
    elif host.upper() == "NO":
        return tokentestpwrt(hostapi=hostapi)
    else:
        print("insert yes or no")
        return tokenpwrt(hostapi)


def numberpwrt(hostapi):
    api = client.HTTPSConnection(hostapi)
    number = input("insert number:").replace('+', '00')

    if not pn.search(number):
        request = "/phonelogin?phone={phone}".format(
            phone=number
        )
        api.request("GET", request)
        result = api.getresponse()
        response = json.loads(result.read().decode("utf-8"))
        if response["ok"]:
            return response["result"]
        else:
            return numberpwrt(hostapi)


def codeloginpwrt(codeprov, hostapi):
    api = client.HTTPSConnection(hostapi)
    code = input("insert code from telegram:")
    if not pn.search(code):
        request = "/user{codeprov}/completephonelogin?code={code}".format(
            codeprov=codeprov,
            code=code)
        api.request("GET", request)
        result = api.getresponse()
        response = json.loads(result.read().decode("utf-8"))
        if response["ok"]:
            return response["result"]
        elif "2FA" in str(response["description"]).upper():
            print(response["description"])
            return factory2passwdpert(codeprov, hostapi)
    return codeloginpwrt(codeprov, hostapi)


def factory2passwdpert(codeprov, hostapi):
    api = client.HTTPSConnection(hostapi)
    password = input("insert password from telegram:")
    request = "/user{codeprov}//complete2FALogin?password={password}".format(
        codeprov=codeprov,
        password=password
    )
    api.request("GET", request)
    result = api.getresponse()
    response = json.loads(result.read().decode("utf-8"))
    if response["ok"]:
        return response["result"]
    else:
        return factory2passwdpert(codeprov, hostapi)


def tokentestpwrt(hostapi, token=None):
    api = client.HTTPSConnection(hostapi)
    if not token:
        token = input("insert token pwrtelegram:")
    try:
        request = "/user{USER_TOKEN}/getChat?chat_id={idchat}".format(
            USER_TOKEN=token,
            idchat=token.split(':')[0])
        api.request("GET", request)
        result = api.getresponse()
        response = json.loads(result.read().decode("utf-8"))

        if response["ok"]:
            return token
        else:
            print("insert valid token")
            return tokentestpwrt(hostapi)
    except Exception:
        print("insert valid token")
        return tokentestpwrt(api)


def gen_config():
    with open("LICENSE", "r") as License:
        conf = {"license":License.read().replace('\n',' ')}
    with open("./data/config/config.json.sample",'r') as config:
        stock = json.load(config)
    redis = gen_configredis()
    redis.update({"value": stock["redis"]["value"]})
    conf.update({"redis":redis})
    conf.update({"mariadb":gen_configmariadb()})
    token = input("insert token Telegram")
    assert token, "You must insert a bot token"
    conf.update({"bot":{"token":token}})
    conf.update({"pwrt":gen_configpwrt()})
    admin = []
    a = input("insert id admin single or split by ,")
    control01 = True
    while control01:
        if str(a).upper() == "N":
            control01 = False
        else:
            a = str(a).replace(' ', '').split(',')
            for b in a:
                try:
                    admin.append(int(b))
                except Exception:
                    print("id admin not int")
            a = input("insert id admin single or split by ,")
    conf.update({"admin":admin})
    create = input("insert language pref")
    control = True
    while control:
        if create == None:
            create = input("insert language pref")
        else:
            control = False
            conf.update({"langpref":create})

    create = input("insert sysntax pref (HTML or MARKDOWN)")
    control = True
    while control:
        if create.upper() =="HTML":
            control = False
            conf.update({"syntaxpref": create.upper()})
        elif create.upper() == "MARKDOWN":
            control = False
            conf.update({"syntaxpref":create.upper()})
        else:
            create = input("insert sysntax pref (HTML or MARKDOWN)")

    create = input("use whitelist group?")
    control = True
    while control:
        if create.upper() == "YES":
            control = False
            cwhitelist = True
            control01 = True
            whitelistv = []
            a = input("insert id group single or split by ,")
            while control01:
                if str(a).upper() == "N":
                    control01 = False
                else:
                    a = str(a).replace(' ', '').split(',')
                    for b in a:
                        try:
                            whitelistv.append(int(b))
                        except Exception:
                            print("id group not int")
                    a = input("insert id group single or split by ,")
        elif create.upper() == "NO":
            control = False
            cwhitelist = False
            whitelistv = [0, 0]
        else:
            create = input("insert yes or no")
    control01 = True
    whitelistdeep = []
    a = input("insert deeeplink whitelist single or split by , or n for stop")
    while control01:
        if str(a).upper() == "N":
            control01 = False
        else:
            a = str(a).replace(' ', '').split(',')
            for b in a:
                whitelistdeep.append(b)

            a = input("insert deeeplink whitelist single or split by , or n for stop")
    conf.update({"whitelist":{"bool":cwhitelist,"list":whitelistv,
                              "deeplinklist":whitelistdeep}})
    create = input("use inline?")
    control = True
    while control:
        if create.upper() == "YES":
            control = False
            inlinev = True
        elif create.upper() == "NO":
            control = False
            inlinev = False
        else:
            create = input("insert yes or no")
    conf.update({"inline":{"bool":inlinev}})
    create = input("use antiflood?")
    control = True
    while control:
        if create.upper() == "YES":
            control = False
            antifloodv = True
            timeantifloodv = {"advert": {"msg": 5, "seconds": 2},
                              "warn": {"msg": 20, "seconds": 8},
                              "ban24h": {"warn": 5, "seconds": 3600}}
            # TODO timeantifloodv set user
        elif create.upper() == "NO":
            control = False
            antifloodv = False
            timeantifloodv = {"advert": {"msg": 5, "seconds": 2},
                              "warn": {"msg": 20, "seconds": 8},
                              "ban24h": {"warn": 5, "seconds": 3600}}
        else:
            create = input("insert yes or no")
    conf.update({"antiflood":{"bool":antifloodv,"value":timeantifloodv}})
    create = input("use checkgroup?")
    control = True
    while control:
        if create.upper() == "YES":
            control = False
            checkgroupbv = True
            timecheck = input("insert time check in seconds [43200]:") or 43200
            control01 = True
            while control01:
                try:
                    timecheck = int(timecheck)
                    control01 = False
                except Exception:
                    print("time  not int")
                    timecheck = input(
                        "insert time check in seconds[43200]:"
                    ) or 43200
            checkgroup = input("insert group id")
            control01 = True
            while control01:
                try:
                    checkgroup = int(checkgroup)
                    control01 = False
                except Exception:
                    print("group id   not int")
                    timecheck = input("insert group id")
        elif create.upper() == "NO":
            control = False
            checkgroupbv = False
            timecheck = 864000
            checkgroup = "id"
        else:
            create = input("insert yes or no")
    conf.update({"checkgroup":{"bool":checkgroupbv,"time":timecheck,
                 "idgroup":checkgroup}})

    control = True
    test = input("use crontab [Yes or No") or "NO"
    while control:
        if test.upper() == "NO":
            conf.update({"crontab":{"bool":False}})
            control = False
        elif test.upper() == "YES":
            conf.update({"crontab":{"bool":True}})
            control = False
        else:
            test = input("use crontab [Yes or No") or "NO"

    control = True
    test = input("INSERT id group for support") or None
    while control:
        try:
            conf.update({"chatsupport":{"chat":int(test)}})
            control = False
        except Exception:
            print("idgroup is not int")
            test = input("INSERT id group") or None

    levellogging = input("INSERT level logging for terminal") or 20
    while control:
        try:
            levellogging = int(levellogging)
            control = False
        except Exception:
            print("levellogging is not int")
            levellogging = input("INSERT level logging") or 20

    control = True
    test = input("use chatlog [Yes or No") or "NO"
    while control:
        if test.upper() == "NO":
            conf.update({"log": {"chat": {"bool":False,
                                          "chatlog":"idchat",
                                          "level":30},
                                 "term":{"level":levellogging,
                                         "format":stock["log"]
                                         ["term"]["format"]}}})
            control = False
        elif test.upper() == "YES":
            control = False
            levellogginc = input("INSERT level logging chat") or 30
            control1 = True
            while control1:
                try:
                    levellogginc = int(levellogginc)
                    control1 = False
                except Exception:
                    print("levellogging is not int")
                    levellogginc = input("INSERT level logging chat ") or 30
            chatlogging = input("INSERT chat id ") or None
            control1 = True
            while control1:
                try:
                    chatlogging = int(chatlogging)
                    control1 = False
                except Exception:
                    print("levellogging is not int")
                    chatlogging = input("INSERT chat id ") or None
            conf.update({"log": {"chat": {"bool": True,
                                          "chatlog": chatlogging,
                                          "level": levellogginc},
                                 "term": {"level": levellogging,
                                          "format": stock["log"]
                                          ["term"]["format"]}}})

        else:
            test = input("use chatlog [Yes or No") or "NO"

    return conf





def genconfig(file=None):
    if file is None:
        file = './data/config/config.json'
    conf = gen_config()
    with open(file, 'w')as j:
        json.dump(conf, j, indent=2, ensure_ascii=False)
    return True

if __name__ == "__main__":
    print(genconfig("example.json"))
