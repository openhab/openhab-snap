# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
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

        if 'source' in schema['required']:
            del schema['required']

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
        # handles rest for us.
        # If we have zulu package defined for target architecture use it, and clean stage-packages, build-packages
        # If we have no zulu package defined, use openjdk-8-jre instead
        self.zulu = True
        self.build_packages = []
        self.stage_packages = []
        if 'amd64' == self.project.deb_arch and self.options.zulu_amd64:
             self.sourcedir = self.options.zulu_amd64
        elif 'armhf' == self.project.deb_arch and self.options.zulu_armhf:
             self.sourcedir = self.options.zulu_armhf
        elif 'arm64' == self.project.deb_arch and self.options.zulu_arm64:
             self.sourcedir = self.options.zulu_arm64
        elif 'i386' == self.project.deb_arch and self.options.zulu_x86:
             self.sourcedir = self.options.zulu_x86
        else:
             self.stage_packages.append('openjdk-8-jre')
             self.build_packages.append('openjdk-8-jre-headless')
             self.zulu = False
             logger.info('We do not have zulu release for {!r}, defaulting to openjdk runtime'.format(self.project.deb_arch))

        if self.zulu:
             setattr(options, 'source', self.sourcedir)
             logger.info('Using zulu java runtime for {!r}: {!r}'.format(self.project.deb_arch, self.sourcedir))

    def build(self):
        super().build()
        if self.zulu:
            snapcraft.file_utils.link_or_copy_tree(
                self.builddir, self.installdir,
                copy_function=lambda src, dst: dump._link_or_copy(src, dst, self.installdir))

    def enable_cross_compilation(self):
        if not self.zulu:
            pass

    def env(self, root):
        # set env based on java runtime we are using
        if self.zulu:
            return ['JAVA_HOME=%s/jre' % root,
                    'PATH=%s/jre/bin:$PATH' % root]
        else:
            return ['JAVA_HOME=%s/usr/lib/jvm/java-8-openjdk-%s' % (root, self.project.deb_arch),
                    'PATH=%s/usr/lib/jvm/java-8-openjdk-%s/bin:$PATH' % (root, self.project.deb_arch)]

    def snap_fileset(self):
        # Cut out jdk/zulu-jdk bits which are not needed, we want just jre
        if self.zulu:
            return (['-bin',
                     '-demo',
                     '-include',
                     '-lib',
                     '-man',
                     '-sample',
                     '-src.zip',
                     '-jre/lib/aarch32/client/libjvm.diz',
                     '-openhab-control',
                     '-connect-interfaces',
                     ])
        else:
            return (['-lib',
                     '-var',
                     '-usr/include',
                     '-usr/lib/gcc',
                     '-usr/lib/ssl',
                     '-usr/lib/X11',
                     '-usr/lib/*-linux-gnu/',
                     '-usr/sbin',
                     '-usr/shared',
                     ])
