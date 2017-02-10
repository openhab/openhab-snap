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
        self._modify_setenv()
        self._fix_instance_path()

    def _modify_oh2_dir(self):
        logger.warning('Patching ' + self.installdir + '/runtime/bin/oh2_dir_layout')
        self._replaceAll(self.installdir+"/runtime/bin/oh2_dir_layout", "${OPENHAB_HOME}/conf", "${SNAP_DATA}/conf")
        self._replaceAll(self.installdir+"/runtime/bin/oh2_dir_layout", "${OPENHAB_HOME}/userdata", "${SNAP_DATA}/userdata")

    def _modify_setenv(self):
        logger.warning('Patching ' + self.installdir + '/runtime/bin/setenv')
        self._replaceAll(self.installdir+"/runtime/bin/setenv","-Dopenhab.logdir=${OPENHAB_LOGDIR}","-Dopenhab.logdir=${OPENHAB_LOGDIR}\n  -Duser.home=${SNAP_DATA}")

    def _fix_instance_path(self):
        logger.warning('Patching ' + self.installdir + '/runtime/bin/client')
        self._replaceAll(self.installdir+"/runtime/bin/client", "${KARAF_HOME}/instances", "${SNAP_DATA}/karaf/instances")
        logger.warning('Patching ' + self.installdir + '/runtime/bin/instance')
        self._replaceAll(self.installdir+"/runtime/bin/instance", "${KARAF_HOME}/instances", "${SNAP_DATA}/karaf/instances")
        logger.warning('Patching ' + self.installdir + '/runtime/bin/karaf')
        self._replaceAll(self.installdir+"/runtime/bin/karaf", "${KARAF_HOME}/instances", "${SNAP_DATA}/karaf/instances")
        logger.warning('Patching ' + self.installdir + '/runtime/bin/shell')
        self._replaceAll(self.installdir+"/runtime/bin/shell", "${KARAF_HOME}/instances", "${SNAP_DATA}/karaf/instances")

    def _replaceAll(self,filePath,searchExp,replaceExp):
        for line in fileinput.input(filePath, inplace=1):
             if searchExp in line:
                 line = line.replace(searchExp,replaceExp)
             sys.stdout.write(line)
