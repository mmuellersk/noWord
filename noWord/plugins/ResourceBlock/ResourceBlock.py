#!/usr/bin/env python
import os
import sys
import glob
sys.path.insert(0, '...')


from reportlab.lib import colors
from reportlab.lib.units import cm

import noWord.common.utils_rp as cmn_utils_rp
import noWord.common.utils_di as cmn_utils_di

from noWord.common.PluginInterface import PluginInterface
import noWord.common.utils_fs as cmn_utils_fs


class ResourceBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'resource'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):
        file_types = ('*.yaml','*.json','*.plist','*.xml');
        # filename or content element
        if 'filename' in block:
            filename = context.processTextCmds(block['filename']).strip()
            data = cmn_utils_fs.deserialize(os.path.join(block['_path'], filename))
        elif 'folder' in block:
            folder = context.processTextCmds(block['folder']).strip()
            
            if (os.path.isdir(folder) == False):
                folder = os.path.join( block['_path'], folder)
            recursive = self.getElemValue(block, 'recursive', False)
            filekey = self.getElemValue(block, 'filekey', '')

            files = []
            if not filekey:
                for type in file_types:
                    files.extend(glob.glob(os.path.join(folder, type),recursive=recursive))
            else:
                files = glob.glob(os.path.join(folder, filekey),recursive=recursive)
            
            data=[]
            for file in files:
                data.append( cmn_utils_fs.deserialize(file))
   
        elif 'fileselector' in block:
            fileselector = os.path.join( block['_path'], block['fileselector'])
            files = []
            files.extend(glob.glob(fileselector,recursive=True))
            data=[]
            for file in files:
                data.append( cmn_utils_fs.deserialize(file))
        elif 'content' in block:
            data = block['content']

        else:
            return []

        if 'sort' in block:
            sortKey=block['sort']
            if isinstance(sortKey,str):
                data = sorted(data, key=lambda k: k[sortKey])
            elif isinstance(sortKey,list):
                if len(sortKey)==1:
                    data = sorted(data, key=lambda k: k[sortKey[0]])
                if len(sortKey)==2:
                    data = sorted(data, key=lambda k: (k[sortKey[0]], k[sortKey[1]]))
                if len(sortKey)==3:
                    data = sorted(data, key=lambda k: (k[sortKey[0]], k[sortKey[1]], k[sortKey[2]]))
                else:
                    print('Sort with more than 3 fields not supported')


        if 'select' in block:
            selectCmd = context.processTextCmds(block['select']).strip()
            data = cmn_utils_di.selectSubset(data, selectCmd)

        # autonumbering
        autonumber = self.getElemValue(block, 'autonumber', False)
        if autonumber:
            for x, entry in enumerate(data):
                data[x]['number']=str(x+1)


        # alias element
        alias = context.processTextCmds(block['alias']).strip()

        # level element, default 1
        setGlobal = self.getElemValue(block, 'global', False)

        if alias in context.resources:
            context.resources[alias].update(data)
        else:
            context.resources[alias] = data

        if setGlobal:
            context.docInfo.update(data)

        # return empty list
        return []
