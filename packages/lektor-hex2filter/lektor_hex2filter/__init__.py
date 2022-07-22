# -*- coding: utf-8 -*-
import math

from lektor.pluginsystem import Plugin

from .generate_filter import main


class Hex2FilterPlugin(Plugin):
    name = 'hex2filter'
    description = u'convert a hexadecimal color code to a CSS filter'

    cache = {}

    def on_process_template_context(self, context, **extra):
        cache = Hex2FilterPlugin.cache
        def generate_filter(color: str) -> str:
            if color in cache:
                return cache[color]

            result = main(color)['filter']
            cache[color] = result

            return result

        context['generate_filter'] = generate_filter
