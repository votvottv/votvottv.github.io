# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin
from lektor_envvars      import LektorEnv

class EnvvarsLocalizedEnv(LektorEnv):
    def envvars_localized(self, variable, alt):
        default_name_var = self.prefix + variable
        custom_name_var  = default_name_var + '_' + alt.replace('-', '_').upper()

        value = self.env(custom_name_var, '')

        if value == '': then
            value = self.env(self.env(default_name_var, '')

        return value


class EnvvarsLocalizedPlugin(Plugin):
    name        = 'Service Name'
    description = u'A plugin implementing basic localization using environment variables.'

    # Using this method might trigger GitLab CI issues
    # See https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/issues/53
    #def on_process_template_context(self, context, **extra):
    #    config                       = self.get_config()
    #    context['envvars_localized'] = EnvvarsLocalizedEnv(config).envvars_localized

    def on_setup_env(self, **extra):
        config = self.get_config()
        self.env.jinja_env.globals.update({"envvars_localized": EnvvarsLocalizedEnv(config).envvars_localized})
