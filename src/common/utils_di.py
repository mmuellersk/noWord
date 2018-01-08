#!/usr/bin/env python

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

    return aDocInfo


def flattenDicts(dictList, keys=[]):
    if len(dictList) == 0:
        return []
    if len(keys) == 0:
        keys = dictList[0].keys()
    return [[d[k] for k in keys] for d in dictList]
