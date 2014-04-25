import requests, yaml, os, zipfile

from os.path import expanduser

# site = "tengs.herokuapp.com"
site = "http://0.0.0.0:3000"
home = expanduser("~")
file_path = "{0}/.tengs".format(home)
tengs_path = "{0}/tengs".format(home)

def generate_url(url, api_key=None):
    if api_key == None:
        api_key = credentials()["api_key"]
    return "{0}/api/{1}?api_key={2}".format(site, url, api_key)

def credentials():
    stream = file(file_path, 'r')
    return yaml.load(stream)

def login(args):
    path = "users/{0}/check_auth.json".format(args.github_name)
    res = requests.get(generate_url(path, api_key=args.api_key))
    if res.status_code == 200:
        data = {
            "github_name": args.github_name,
            "api_key": args.api_key
        }
        with open(file_path, 'w+') as outfile:
            outfile.write(yaml.dump(data, default_flow_style=False))
        print "login has been successful!"
        print "{0} has written".format(file_path)
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
            r = requests.get(exercise["tarball"] + "?api_key=" + credentials()["api_key"])
            with open(tarball_path, "wb") as code:
                code.write(r.content)
            zfile = zipfile.ZipFile(tarball_path)
            zfile.extractall(exercise_path)
