# Copyright 2012 Jeffrey R. Spies
# License: Apache License, Version 2.0
# Website: http://jspi.es/benchmark

from . import __VERSION__
from Benchmark import Benchmark

import time
import platform
import os
import sys


class BenchmarkProgram(object):

    def __init__(self, module="__main__", **kwargs):
        if isinstance(module, basestring):
            self.module = __import__(module)

        benchmarks = self.loadFromModule(self.module)

        totalRuns = 0
        objects = []
        for obj in benchmarks:
            obj = obj(**kwargs)
            obj.run()
            objects.append(obj)
            totalRuns += obj.getTotalRuns()

        title = kwargs.get('title', 'Benchmark Report')
        info = "Total runs: %d run in arbitrary order" % totalRuns + os.linesep
        info += "Python version: %s" % platform.python_version() + os.linesep
        info += "System: %s %s %s" % (platform.machine(),
                                      platform.system(),
                                      platform.release()) + os.linesep
        info += "Version: %s" % "benchmark v" + __VERSION__ + os.linesep
        info += "Date: %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        info += os.linesep

        sys.stdout.write(self.displayTable(objects, title, info, **kwargs))

    def formatHeading(self, head, level=1, **kwargs):
        format = kwargs.get('format', 'markdown')
        if format.lower() in ['markdown']:
            lvl = '#' if level == 1 else '##'
            return lvl + ' ' + head
        elif format.lower() in ['csv', 'comma']:
            return head
        elif format.lower() in ['plain']:
            return '\033[1m' + head + '\033[0m'
        else:  # rst
            lvl = '=' if level == 1 else '-'
            return head + os.linesep + (lvl * len(head))

    def displayTable(self, benchmarks, title, info, **kwargs):
        lines = ''
        lines += self.formatHeading(title, level=1, **kwargs)
        lines += os.linesep * 2

        for obj in benchmarks:
            if obj.label:
                title = obj.label
            else:
                title = obj.__class__.__name__
                title = title.replace('_', ' ')

            lines += self.formatHeading(title, level=2, **kwargs)
            lines += os.linesep * 2

            lines += obj.getTable(**kwargs)
            lines += os.linesep * 2

        lines += info

        return lines

    def loadFromModule(self, module):
        benchmarks = []
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, Benchmark):
                benchmarks.append(obj)
        return benchmarks

main = BenchmarkProgram
