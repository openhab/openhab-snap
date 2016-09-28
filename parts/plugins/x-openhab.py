# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
import os
import fileinput
import sys
import snapcraft
import logging

from snapcraft.plugins import dump

logger = logging.getLogger(__name__)

class OpenHabPlugin(snapcraft.plugins.dump.DumpPlugin):

    def build(self):
        super().build()
        self._modify_oh2_dir()
        self._modify_karaf()

    def _modify_oh2_dir(self):
        logger.warning('Patching ' + self.installdir + '/runtime/karaf/bin/oh2_dir_layout')
        self._replaceAll(self.installdir+"/runtime/karaf/bin/oh2_dir_layout", "${OPENHAB_HOME}/conf", "${SNAP_COMMON}/conf")
        self._replaceAll(self.installdir+"/runtime/karaf/bin/oh2_dir_layout", "${OPENHAB_HOME}/userdata", "${SNAP_COMMON}/userdata")
        self._replaceAll(self.installdir+"/runtime/karaf/bin/oh2_dir_layout", "${OPENHAB_RUNTIME}/karaf/etc", "${SNAP_COMMON}/karaf/etc")

    def _modify_karaf(self):
        logger.warning('Patching ' + self.installdir + '/runtime/karaf/bin/karaf')
        self._replaceAll(self.installdir+"/runtime/karaf/bin/karaf", "${KARAF_HOME}/instances", "${SNAP_COMMON}/karaf/instances")

    def _replaceAll(self,filePath,searchExp,replaceExp):
        for line in fileinput.input(filePath, inplace=1):
             if searchExp in line:
                 line = line.replace(searchExp,replaceExp)
             sys.stdout.write(line)
