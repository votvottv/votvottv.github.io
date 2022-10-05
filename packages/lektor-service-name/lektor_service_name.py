# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin

# This approach respects the envvars plugin configuration, but fails to build in the GitLab CI
# See https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/merge_requests/48#note_2840161
#
#from lektor_envvars      import LektorEnv
#
#class ServiceNameEnv(LektorEnv):
#    def service_name(self, alt):
#        default_name_var = self.prefix + 'SERVICE_NAME'
#        custom_name_var  = default_name_var + '_' + alt.replace('-', '_').upper()
#
#        return self.env(custom_name_var, self.env(default_name_var, ''))
#
#
#class ServiceNamePlugin(Plugin):
#    name = 'Service Name'
#    description = u'A plugin that gets a localized site service name from environment variables.'
#
#    def on_process_template_context(self, context, **extra):
#        config                  = self.get_config()
#        context['service_name'] = ServiceNameEnv(config).service_name

# This approach does not respect the envvars plugins configuration, but
# successfully builds in the GitLab CI.
from os import environ

# Hardcoded default prefix
DEFAULT_PREFIX = "LEKTOR_"

def service_name(alt):
    default_name_var = DEFAULT_PREFIX + 'SERVICE_NAME'
    custom_name_var  = default_name_var + '_' + alt.replace('-', '_').upper()

    if custom_name_var in environ:
        return environ[custom_name_var]

    if default_name_var in environ:
        return environ[default_name_var]

    return ''


class ServiceNamePlugin(Plugin):
    name = 'Service Name'
    description = u'A plugin that gets a localized site service name from environment variables.'

    def on_process_template_context(self, context, **extra):
        context['service_name'] = service_name
