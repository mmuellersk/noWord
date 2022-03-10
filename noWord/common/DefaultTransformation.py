
from copy import deepcopy

def availableTransformations():

    transformations =  [
        'merge',
        'slice',
        'distinct',
        'selectFirst',
        'autonumber',
        'sort',
        'distinctFirstToken',
        'replace'
    ]

    return transformations

def merge( input, params, context):

    targetResource = {}

    if isinstance( input, list):
        for resourceName in input:
            data = context.getResource(context.resources, resourceName)
            targetResource.update(deepcopy(data))

    return targetResource

def slice( input, params, context):

    inputRes = context.getResource(context.resources, input)

    outputList = deepcopy(inputRes[params['start']:params['end']])

    return outputList


def distinct( input, params, context):

    inputRes = context.getResource(context.resources, input)

    outputRes = []
    outputResList = []

    for item in inputRes :
        if params['key'] in item :
            token = item[params['key']]
            if not token in outputResList :
                outputResList.append(token)
                entry = {}
                entry[params['key']] = token
                outputRes.append(entry)

    return outputRes


def selectFirst( input, params, context):

    inputRes = context.getResource(context.resources, input)

    outputRes = {}

    for item in inputRes :
        if params['key'] in item :
            if item[params['key']] == params['value']:
                outputRes = item
                break

    return outputRes

def autonumber( input, params, context):

    inputRes = context.getResource(context.resources, input)

    outputRes = []
    index = 0

    if inputRes is not None:

        for item in inputRes :
            index += 1
            newitem = deepcopy(item)
            newitem['number'] = index
            outputRes.append(newitem)

    return outputRes

def sort( input, params, context):

    inputRes = context.getResource(context.resources, input)

    outputRes = []
    sortKey = params['key']
    reverseFlag = params['reverse'] if 'reverse' in params else False

    if inputRes is None:
        return outputRes

    if isinstance(sortKey,str):
        outputRes = sorted(inputRes, key=lambda k: k[sortKey], reverse=reverseFlag)
    elif isinstance(sortKey,list):
        if len(sortKey)==1:
            outputRes = sorted(inputRes, key=lambda k: k[sortKey[0]], reverse=reverseFlag)
        if len(sortKey)==2:
            outputRes = sorted(inputRes, key=lambda k: (k[sortKey[0]], k[sortKey[1]]), reverse=reverseFlag)
        if len(sortKey)==3:
            outputRes = sorted(inputRes, key=lambda k: (k[sortKey[0]], k[sortKey[1]], k[sortKey[2]]), reverse=reverseFlag)
        else:
            print('Sort with more than 3 fields not supported')

    return outputRes

def distinctFirstToken( input, params, context):

    inputRes = context.getResource(context.resources, input)

    outputRes = []
    outputResList = []

    for item in inputRes :
        if params['key'] in item :
            tokens = item[params['key']].split(params['seperator'])
            if len(tokens) > 0 :
                token = tokens[0]
                if not token in outputResList :
                    outputResList.append(token)
                    entry = {}
                    entry[params['key']] = token
                    outputRes.append(entry)

    return outputRes

def replace( input, params, context):

    inputRes = context.getResource(context.resources, input)

    outputRes = []

    key = params["key"]
    old = params["old"]
    new = params["new"]

    if inputRes is not None:

        for item in inputRes :
            newitem = deepcopy(item)
            newitem[key] = item[key].replace(old, new)
            outputRes.append(newitem)

    return outputRes
