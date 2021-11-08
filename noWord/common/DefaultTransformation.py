
from copy import deepcopy

def merge( input, params, context):

    targetResource = {}

    if isinstance( input, list):
        for resourceName in input:
            data = context.getResource(context.resources, resourceName)
            targetResource.update(deepcopy(data))

    return targetResource

def slice( input, params, context):

    inputRes = context.getResource(context.resources, input)

    outputList = inputRes[params['start']:params['end']]

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


def autonumber( input, params, context):

    inputRes = context.getResource(context.resources, input)

    outputRes = []
    index = 0

    for item in inputRes :
        index += 1
        newitem = deepcopy(item)
        newitem['number'] = index
        outputRes.append(newitem)

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
