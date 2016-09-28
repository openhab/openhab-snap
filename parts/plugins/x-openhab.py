# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
import os
import stat
import fileinput
import sys
import snapcraft
import logging

from tempfile import mkstemp
from shutil import move
from os import remove, close

from snapcraft.plugins import dump

logger = logging.getLogger(__name__)

class OpenHabPlugin(snapcraft.plugins.dump.DumpPlugin):

    def build(self):
        super().build()
        self._modify_oh2_dir()
        self._modify_karaf()

    def _modify_oh2_dir(self):
        logger.warning('Patching ' + self.installdir + '/runtime/karaf/bin/oh2_dir_layout')
        self._replaceAll(self.installdir+"/runtime/karaf/bin/oh2_dir_layout", "${OPENHAB_HOME}/conf", "${SNAP_USER_COMMON}/conf")
        self._replaceAll(self.installdir+"/runtime/karaf/bin/oh2_dir_layout", "${OPENHAB_HOME}/userdata", "${SNAP_USER_COMMON}/userdata")
        self._replaceAll(self.installdir+"/runtime/karaf/bin/oh2_dir_layout", "${OPENHAB_RUNTIME}/karaf/etc", "${SNAP_USER_COMMON}/karaf/etc")

    def _modify_karaf(self):
        logger.warning('Patching ' + self.installdir + '/runtime/karaf/bin/karaf')
        self._replaceAll(self.installdir+"/runtime/karaf/bin/karaf", "${KARAF_HOME}/instances", "${SNAP_USER_COMMON}/karaf/instances")

    def _replaceAll(self,filePath,searchExp,replaceExp):
        fh, abs_path = mkstemp()
        with open(abs_path,'w') as new_file:
            with open(filePath) as old_file:
#            for line in fileinput.input(f, inplace=1):
#                if searchExp in line:
#                    line = line.replace(searchExp,replaceExp)
                for line in old_file:
                    new_file.write(line.replace(searchExp, replaceExp))
        close(fh)
        #Remove original file
        remove(filePath)
        #Move new file
        move(abs_path, filePath)
        st = os.stat(filePath)
        os.chmod(filePath, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IRGRP | stat.S_IROTH | stat.S_IXOTH)
