#!/usr/bin/env python

import os
import sys
import importlib

import common.utils_fs as cmn_utils_fs

from importlib.util import spec_from_file_location, module_from_spec


class PluginManager :
    def __init__(self) :
        self.pluginFolders = []
        self.pluginCategories = {}

    def addPluginFolder( self, folder) :
        self.pluginFolders.append(folder)

    def loadPlugins( self ) :
        for plugin in self.searchPlugins() :
            self.insertPlugin(plugin.Module())

    def insertPlugin( self, object) :
        cat = object.Category()
        name = object.Name()
        if cat in self.pluginCategories :
            self.pluginCategories[cat][name] = object
        else :
            plugins = {}
            plugins[name] = object
            self.pluginCategories[cat] = plugins

    def searchPlugins( self ) :
        for folder in self.pluginFolders :
            for item in sorted(os.listdir(folder)) :
                itemPath = os.path.join(folder, item)
                if cmn_utils_fs.isContentDir(itemPath) :
                    sys.path.append(itemPath)
                    yield self.load_module(itemPath)


    def findPlugin( self, name, category='default') :
        if category in self.pluginCategories :
            if name in self.pluginCategories[category] :
                return self.pluginCategories[category][name]

        return None

    def load_module(self,path, name=""):
        try :
            # take the module name by default
            name = name if name != "" else path.split(os.sep)[-1]
            spec = spec_from_file_location(name, os.path.join(path, "__init__.py"))
            plugin_module = module_from_spec(spec)
            spec.loader.exec_module(plugin_module)
            return plugin_module
        except Exception as e:
            print("failed to load module", path, "-->", e)
