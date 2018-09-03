#!/usr/bin/env python
import os
import sys
import getpass
import reportlab.lib.enums
import copy
import sys
import datetime
import pprint

noWordDir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "../..")

sys.path.insert(0, '..')
sys.path.insert(0, noWordDir)
sys.path.insert(0, './noWord')


from noWord.common.PluginManager import PluginManager
from noWord.common.NWProcContext import NWProcContext
from noWord.common.NWDocument import NWDocument

import noWord.common.utils_fs as cmn_utils_fs
import noWord.common.utils_di as cmn_utils_di
import noWord.common.utils_rp as cmn_utils_rp

import noWord as meta

import noWord.common.DefaultDecoration as NoWordDecoration


class NWGenerator:
    def __init__(self, aSourcePath, aOutputPath, extPluginFolders=[], dumpContent=False):

        self.dumpContentFlag = dumpContent

        self.pluginMng = PluginManager()

        self.pluginMng.addPluginFolder(
            os.path.join(os.path.dirname(__file__),
                         '../plugins/'))

        for extPluginFolder in extPluginFolders:
            self.pluginMng.addPluginFolder(extPluginFolder)

        self.pluginMng.loadPlugins()

        # Load general prefs
        docInfos = cmn_utils_fs.deserialize(
            os.path.join(aSourcePath,
                         "doc_info.yaml"))

        self.context = NWProcContext(docInfos,
                                     aSourcePath,
                                     aOutputPath,
                                     self.prepareBlocks,
                                     self.processBlocks)

        self.context.addResource(
            'noWordInfo', {'name': meta.__name__, 'version': meta.__version__})

        self.context.addResource(
            'buildInfo', {
                'timestamp': datetime.datetime.now().isoformat(),
                'builder': getpass.getuser()})

        self.overrideValues(
            'styles', self.context.styleSheet, self.context.docInfo)

        self.doc = NWDocument(self.context.docInfo, self.context.styleSheet)
        self.context.doc = self.doc

        if 'decorations' in self.context.docInfo:
            decorations = self.context.docInfo['decorations']
            for decoration in decorations:
                if hasattr(NoWordDecoration, decoration):
                    self.addDecoration(getattr(NoWordDecoration, decoration))

    def overrideValues(self, strkey, dicTraget, dicSource):
        if strkey in dicSource:
            dicTraget.update(dicSource[strkey])

    def setStyleSheet(self, obj):
        self.context.styleSheet = obj
        self.overrideValues(
            'styles', self.context.styleSheet, self.context.docInfo)
        self.doc.setStyleSheet(obj)

    def addDecoration(self, funcObj):
        self.doc.addDecoration(funcObj)

    def prepareBlocks(self, blocks, context, path):
        for block in blocks:
            block['_path'] = path
            plugin = self.pluginMng.findPlugin(block['type'])
            if plugin is not None:
                plugin.prepare(block, context)
            else:
                print('Plugin not found: %s' % block['type'])

    def processBlocks(self, blocks, context, path):
        content = []
        for block in blocks:
            block['_path'] = path
            plugin = self.pluginMng.findPlugin(block['type'])
            if plugin is not None:
                content.extend(plugin.process(block, context))
            else:
                print('Plugin not found: %s' % block['type'])

        return content

    def process(self):
        # load block list
        blocks = []
        for block in self.processFolder(self.context.sourcePath):
            blocks.append(block)

        # init plugins: init only used plugins
        pluginset = set()
        for block in blocks:
            if 'content' in block:
                for blockContent in block['content']:
                    if 'type' in blockContent:
                        plugin = self.pluginMng.findPlugin(
                            blockContent['type'])
                        if plugin is not None:
                            pluginset.add(plugin)
                            continue

            plugin = self.pluginMng.findPlugin(block['type'])
            if plugin is not None:
                pluginset.add(plugin)
        for plugin in pluginset:
            plugin.init(self.context)

        # prepare blocks
        for block in blocks:
            plugin = self.pluginMng.findPlugin(block['type'])
            if plugin is not None:
                plugin.prepare(block, self.context)
            else:
                print('Plugin not found: %s' % block['type'])

        # process blocks
        content = []
        content.append(cmn_utils_rp.TriggerFlowable(self.context.buildBegins))

        for block in blocks:
            plugin = self.pluginMng.findPlugin(block['type'])
            if plugin is not None:
                content.extend(plugin.process(block, self.context))
            else:
                print('Plugin not found: %s' % block['type'])

        content.extend(self.context.process())

        if not os.path.isdir(self.context.outputPath):
            os.makedirs(self.context.outputPath)

        outputfile = os.path.join(
            self.context.outputPath,
            self.context.docInfo["outputFileTemplate"])

        if self.dumpContentFlag:
            self.dumpContent(content)

        self.doc.build(outputfile, self.context, content)

        return self.context.pageCounter.pageCount

    def processFolder(self, path):
        for item in sorted(os.listdir(path)):
            itemPath = os.path.join(path, item)

            if os.path.isdir(itemPath) and not item.startswith("."):
                for subitem in self.processFolder(itemPath):
                    yield subitem
            elif item.endswith(".yaml"):
                parts = cmn_utils_fs.loadYAML(itemPath)

                if type(parts) is not list:
                    continue

                for part in parts:
                    if "type" not in part:
                        continue

                    # add file path for assets loading
                    part['_path'] = path

                    yield part

    def dumpContent(self, content):

        dumpoutputfile = os.path.join(
            self.context.outputPath,
            self.context.docInfo["outputFileTemplate"] + '.txt')

        with open(dumpoutputfile, 'w', encoding='utf-8') as f:
            prettyPrinter = pprint.PrettyPrinter(indent=4, stream=f)
            prettyPrinter.pprint(content)
