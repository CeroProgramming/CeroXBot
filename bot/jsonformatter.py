from pprint import pprint
from pathlib import Path
import shutil
import json

class JsonFormatter():

    def __init__(self):
        pass

    def importer(filename):
        checkfile = Path("config/" + filename)
        if not checkfile.is_file():
            checkexamplefile = Path("config/example_" + filename)
            if not checkexamplefile.is_file():
                return "ErrorNoFileFound"
            shutil.copy('config/example_' + filename, "config/" + filename)

        with open("config/" + filename) as jsonfile:
            data = json.load(jsonfile)
        return data

    def exporter(data, filename):
        with open("config/" + filename, "w") as jsonfile:
            json.dump(data, jsonfile)
        return

    def addgame(data, name):
        gamedict = dict()
        gamedict = {"name": name, "altnames": [name], "members": []}
        data["games"].__setitem__(name, gamedict)
        return data

    def removegame(data, name):
        data["games"].__delitem__(name)
        return data

    def addaltname(data, game, name):
        data["games"][game]["altnames"].append(name)
        return data

    def removealtname(data, game, name):
        data["games"][game]["altnames"].remove(name)
        return data

    def addmember(data, game, memberid):
        data["games"][game]["members"].append(memberid)
        return data

    def addautomember(data, altname, memberid):
        for game in list(data["games"].keys()):
            try:
                data["games"][game]["altnames"].index(altname)
                data["games"][game]["members"].append(memberid)
                return data
            except:
                pass

    def removemember(data, game, memberid):
        data["games"][game]["members"].remove(memberid)
        return data

    def listgames(data):
        return ", ".join(list(data["games"].keys()))


    def listaltnames(data, game):
        return ", ".join(data["games"][game]["altnames"])

    def listmembers(data, game):
        return data["games"][game]["members"]

    def existnotmember(data, altname, memberid):
        for game in list(data["games"].keys()):
            try:
                data["games"][game]["altnames"].index(altname)
                try:
                    data["games"][game]["members"].index(memberid)
                    return False
                except ValueError:
                    return True
            except:
                pass
        return False



if __name__ == "__main__":
    js = JsonFormatter()
    pass
