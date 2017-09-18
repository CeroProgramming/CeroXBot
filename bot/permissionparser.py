from pprint import pprint
from pathlib import Path
import shutil
import json

class PermissionParser():

    def __init__(self):
        pass

    def uservalidate(data, user):

        default_group = "Default"

        for group in list(data["permissions"].keys()):
            if user.id in data["permissions"][group]["UserList"].split(" "):
                return group

        for group in list(data["permissions"].keys()):
            for role in user.roles:
                if role.id in data["permissions"][group]["GrantToRoles"].split(" "):
                    return group

        return default_group


if __name__ == "__main__":
    pp = PermissionParser()
    pass
