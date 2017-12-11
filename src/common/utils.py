

import argparse




def generatorParser(additionalArgs=[]):
  parser = argparse.ArgumentParser("Generate a PDF document")
  parser.add_argument(dest="source", help="Source folder")
  parser.add_argument(dest="dest", help="Destination folder")

  for arg in additionalArgs:
    parser.add_argument(**arg)

  return parser.parse_args()

def deserialize(path):
  try:
    ext = path.split(".")[-1]
  except:
    pass

  data = {}

  opened = False
  if os.path.isfile(path):
    opened = True
    if ext == "json":
      import json
      f = open(path, "rt")
      data = json.load(f)
    elif ext == "yaml":
      import yaml
      f = open(path, "rt")
      data = yaml.load(f)
    elif ext == "plist":
      import plistlib
      f = open(path, "rb")
      data = plistlib.load(f)
    else:
      opened = False
    if opened:
      f.close()
  if not opened:
    print("Could not deserialize file " + path)

  return data
