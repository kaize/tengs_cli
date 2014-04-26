import requests, os, zipfile
from tengs_cli import *

def login(args):
    path = "users/{0}/check_auth.json".format(args.github_name)
    res = requests.get(generate_url(path, api_key=args.api_key))
    if res.status_code == 200:
        data = {
            "github_name": args.github_name,
            "api_key": args.api_key
        }
        write_config(data)
        print "login has been successful!"
        print "{0} has been written".format(file_path)
    else:
        print "invalid credentials"

def fetch(args):
    path = "exercises/unchecked.json"
    res = requests.get(generate_url(path))
    data = res.json()
    for exercise in data["exercises"]:
        exercise_path = "{0}/{1}/{2}".format(tengs_path, exercise["teng_slug"], exercise["name"])
        tarball_path = "{0}/exercise.zip".format(exercise_path)
        if not os.path.isdir(exercise_path):
            os.makedirs(exercise_path)
        r = requests.get(exercise["tarball"] + "?api_key=" + value_for("api_key"))
        with open(tarball_path, "wb") as code:
            code.write(r.content)
        zfile = zipfile.ZipFile(tarball_path)
        zfile.extractall(exercise_path)
