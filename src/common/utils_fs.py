#!/usr/bin/env python
import os
import argparse
import json
import yaml




def parserCommandLine(additionalArgs=[]):
  parser = argparse.ArgumentParser("noWord pdf generator")
  parser.add_argument(dest="source", help="Source folder")
  parser.add_argument(dest="dest", help="Destination folder")

  for arg in additionalArgs:
    parser.add_argument(**arg)

  return parser.parse_args()

def isContentDir(path) :
    basename = os.path.basename(path)
    return os.path.isdir(path) \
        and not basename.startswith("__") \
        and not basename.startswith(".")

def loadJson(filename):
  filename = os.path.normpath(filename)
  try:
    with open(filename) as data_file:
      data = json.load(data_file)
      return data
  except Exception as e:
    print("Could not read json file: " + str(e))
    exit(1)

def loadYAML(filename):
  filename = os.path.normpath(filename)
  try:
    with open(filename) as data_file:
      data = yaml.load(data_file)
      return data
  except Exception as e:
    print("Could not read yaml file: " + str(e))
    exit(1)

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
