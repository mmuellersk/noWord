#!/usr/bin/env python
import os
import sys
import argparse
import json
import yaml
import plistlib
import xmltodict

noWordDir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "../..")

sys.path.insert(0, noWordDir)

import noWord as meta


def parserCommandLine(additionalArgs=[]):
    parser = argparse.ArgumentParser(description="noWord pdf generator")

    parser.add_argument('-v', '--version', action='version',
                        version=meta.__version__)

    parser.add_argument(dest="source", help="Source folder")
    parser.add_argument(dest="dest", help="Destination folder")

    for arg in additionalArgs:
        parser.add_argument(**arg)

    return parser.parse_args()


def isContentDir(path):
    basename = os.path.basename(path)
    return os.path.isdir(path) \
        and not basename.startswith("__") \
        and not basename.startswith(".")


def loadJson(filename):
    filename = os.path.normpath(filename)
    try:
        with open(filename, encoding='utf-8') as data_file:
            data = json.load(data_file)
            return data
    except Exception as e:
        print("Could not read json file: " + str(e))
        raise


def loadYAML(filename):
    filename = os.path.normpath(filename)
    try:
        with open(filename, encoding='utf-8') as data_file:
            data = yaml.load(data_file, Loader=yaml.FullLoader)
            return data
    except Exception as e:
        print("Could not read yaml file: " + str(e))
        raise


def loadPList(filename):
    filename = os.path.normpath(filename)
    try:
        with open(filename, 'rb') as data_file:
            data = plistlib.load(data_file)
            return data
    except Exception as e:
        print("Could not read plist file: " + str(e))
        raise

def loadXML(filename):
    filename = os.path.normpath(filename)
    try:
        with open(filename, 'rb') as data_file:
            data = xmltodict.parse(data_file)
            return data
    except Exception as e:
        print("Could not read xml file: " + str(e))
        raise


def deserialize(path):
    try:
        ext = path.split(".")[-1]
    except:
        pass

    data = {}

    if os.path.isfile(path):
        if ext == "json":
            data = loadJson(path)
        elif (ext == "yaml") or (ext == "yml") :
            data = loadYAML(path)
        elif ext == "plist":
            data = loadPList(path)
        elif ext == "xml":
            data = loadXML(path)
        else:
            print("Could not deserialize file " + path)

    return data

def saveJson(filename,data):
    filename = os.path.normpath(filename)
    
    with open( filename, 'w') as outfile:
        json.dump(data, outfile)
