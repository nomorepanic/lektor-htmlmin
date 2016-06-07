# -*- coding: utf-8 -*-
import os
import codecs
import chardet

import htmlmin
from lektor.pluginsystem import Plugin

class HTMLMinPlugin(Plugin):
    name = u'Lektor HTMLmin'
    description = u'HTML minifier for Lektor. Based on htmlmin.'

    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)
        self.options = {
			'remove_empty_space': True,
			'remove_all_empty_space': True,
			'reduce_empty_attributes': True,
			'reduce_boolean_attributes': False,
			'remove_optional_attribute_quotes': False,
			'keep_pre': False,
            'pre_attr':'pre'
		}

    def find_html_files(self, destination):
        """
        Finds all html files in the given destination.
        """
        all_files = []
        for root, dirs, files in os.walk(destination):
            for f in files:
                if f.split('.')[-1] == 'html':
                    fullpath = os.path.join(root, f)
                    all_files.append(fullpath)
        return all_files


    def minify_file(self, target):
        """
        Minifies the target html file.

        Handles the original encoding
        """

        decode = True
        encoding_ = ['utf-8', 'latin-1']
        enc=chardet.detect(target)

        if enc['encoding'] == "ascii":
            decode = False
            encoding_ = ['latin-1', 'utf-8']

        f = codecs.open(target, 'r+', encoding_[0])

        if decode:
            result = htmlmin.minify(f.read().decode(encoding_[1]), **self.options)
        else:
            result = htmlmin.minify(f.read(), **self.options)

        f.seek(0)
        f.write(result)
        f.truncate()
        f.close()


    def on_after_build_all(self, builder, **extra):
        """
        after-build-all lektor event
        """
        destination = builder.destination_path
        files = self.find_html_files(destination)
        for htmlfile in files:
            self.minify_file(htmlfile)
