try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
import collections

class versions():
    def __init__(self):
        try:
            f = open("currentversion","r")
            response =  urlopen("https://raw.githubusercontent.com/Auquan/data_set_id/master/versions.txt")
            script = response.read().decode('utf8').split()
            para = f.read().split()
            f.close()
            list= collections.defaultdict(lambda : '0')
            for i in range(len(para)):
                list[para[i]]=para[i]
            for i in range(len(script)):
                if(list[script[i]]!= script[i]):
                    list[script[i]] = script[i]
                    f = open("currentversion","a+")
                    f.write(script[i] + "\n")
                    new_response = urlopen("https://raw.githubusercontent.com/Auquan/data_set_id/master/" + script[i] + ".py")
                    code = new_response.read().decode('utf8')
                    exec(code)
        except FileNotFoundError:
            response =  urlopen("https://raw.githubusercontent.com/Auquan/data_set_id/master/versions.txt")
            script = response.read().decode('utf8').split()
            for i in range(len(script)):
                f = open("currentversion","a+")
                f.write(script[i] + "\n")
                new_response = urlopen("https://raw.githubusercontent.com/Auquan/data_set_id/master/" + script[i] + ".py")
                code = new_response.read().decode('utf8')
                exec(code)
