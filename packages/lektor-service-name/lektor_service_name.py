# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin
from os import environ

# FIXME: use the same config as the envvars plugin
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
