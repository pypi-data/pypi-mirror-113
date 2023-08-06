import argparse
import json
import sys
import types

class FloadModule:
    def init(self, ops):
        pass

    def add_arguments(self, parser:argparse.ArgumentParser):
        pass

    def emit(self, item):
        sys.stdout.write(json.dumps(item) + '\n')

    def start_run(self):
        """
        start run the module, emit new items or process item.
        """
        pass

    def on_close(self):
        pass


class Pipeline(FloadModule):
    def process(self, item):
        pass

    def start_run(self):
        for line in sys.stdin:
            item = json.loads(line)
            ret = self.process(item)
            if ret:
               self.emit(ret)
        self.on_close()


def run_start(mod):
    ret = mod.start()
    if not isinstance(ret, types.GeneratorType):
        ret = [ret]
    
    for item in ret:
        yield item


class Source(FloadModule):
    def start(self):
        pass

    def start_run(self):
        for item in run_start(self):
            self.emit(item)

        self.on_close()
