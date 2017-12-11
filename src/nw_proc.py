import sys
import os
import datetime
import re


import common.utils as NWUtils


from common.generator import NWGenerator


def main():
  args = NWUtils.generatorParser()

  # Load general prefs
  docInfos = NWUtils.deserialize(os.path.join(args.source, "doc_info.yaml"))
  # Process date, save each field as string
  if "date" in docInfos:
    dt = datetime.datetime.strptime(docInfos["date"], "%d.%m.%Y")
    docInfos.update({"year": dt.year, "month": "{0:02d}".format(dt.month), "day": "{0:02d}".format(dt.day)})

  generator = NWGenerator()

  generator.build()

  nbPages = generator.render()
  print(str(nbPages) + " pages rendered")


if __name__ == "__main__": main()
