# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
import os
import fileinput
import sys
import snapcraft
import logging

from snapcraft.plugins import dump

logger = logging.getLogger(__name__)

class JavaRuntimePlugin(snapcraft.BasePlugin):

    @classmethod
    def schema(cls):
        schema = super().schema()

        schema['properties']['zulu-armhf'] = {
            'type': 'string'
        }
        schema['properties']['zulu-armel'] = {
            'type': 'string'
        }
        schema['properties']['zulu-arm64'] = {
            'type': 'string'
        }
        schema['properties']['zulu-amd64'] = {
            'type': 'string'
        }
        schema['properties']['zulu-x86'] = {
            'type': 'string'
        }

        # Inform Snapcraft of the properties associated with pulling. If these
        # change in the YAML Snapcraft will consider the build step dirty.
        schema['pull-properties'].append('zulu-armhf')
        schema['pull-properties'].append('zulu-armel')
        schema['pull-properties'].append('zulu-arm64')
        schema['pull-properties'].append('zulu-amd64')
        schema['pull-properties'].append('zulu-x86')

        return schema

    def __init__(self, name, options, project):
        super().__init__(name, options, project)
        # we want to be clever and filter schema based on architecture, so snapcraft
        # handles rest for us, if we have zulu package defined for current architecture
        # use it, and clean stage-packages and build-packages, otherwise clean source
        logger.info('Deciding which java runtime to use: {!r}'.format(self.project.deb_arch))
        if getattr(self.options, 'source', None):
        if 'amd64' == self.project.deb_arch and self.options.zulu_amd64:
             self.build_packages = []
             self.stage_packages = []
             setattr(options, 'source', self.options.zulu_amd64)
             self.sourcedir = self.options.zulu_amd64
        elif 'armhf' == self.project.deb_arch and self.options.zulu_armhf:
             self.build_packages = []
             self.stage_packages = []
             setattr(options, 'source', self.options.zulu_armhf)
             self.sourcedir = self.options.zulu_armhf
        elif 'arm64' == self.project.deb_arch and self.options.zulu_arm64:
             self.build_packages = []
             self.stage_packages = []
             setattr(options, 'source', self.options.zulu_arm64)
             self.sourcedir = self.options.zulu_arm64
        elif 'i386' == self.project.deb_arch and self.options.zulu_x86:
             self.build_packages = []
             self.stage_packages = []
             setattr(options, 'source', self.options.zulu_x86)
             self.sourcedir = self.options.zulu_x86
        else:
             self.sourcedir = None
