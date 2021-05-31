#!/usr/bin/env python
import re
import datetime


# Process date, save each field as string
def splitDate(aDocInfo):
    if aDocInfo is not None:
        if "date" in aDocInfo:
            dt = datetime.datetime.strptime(aDocInfo["date"], "%d.%m.%Y")
            aDocInfo.update({
                "year": dt.year,
                "month": "{0:02d}".format(dt.month),
                "day": "{0:02d}".format(dt.day)})
        else:
            dt = datetime.datetime.now()
            aDocInfo.update({
                "year": dt.year,
                "month": "{0:02d}".format(dt.month),
                "day": "{0:02d}".format(dt.day)})

    return aDocInfo


def flattenDicts(dictList, keys=[]):
    if len(dictList) == 0:
        return []
    if len(keys) == 0:
        keys = dictList[0].keys()
    return [[d[k] if (k in d) else ' ' for k in keys] for d in dictList]

def selectSubset( resource, query):
    tableRegex = re.compile("^([^\[\]]+)\[(\d+)\]$")
    path = query.split("/")

    for child in path:
        result = tableRegex.findall(child)
        if len(result) > 0:
            (key, index) = result[0]
            resource = resource[key][int(index)]
        else:
            try:
                resource = resource[child]
            except:
                return None
    return resource
