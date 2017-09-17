from pprint import pprint
from pathlib import Path
import shutil
import json

class JsonParser():

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
