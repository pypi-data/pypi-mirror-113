import argparse
import importlib
import logging
import json
import pkg_resources
import sys

from .log import setup_logging

logger = logging.getLogger(__name__)


def load_module(module_name):
    import fload.stream as base_module

    module_class = None
    if hasattr(base_module, module_name):
        module_class = getattr(base_module, module_name)

    if not module_class:
        module_class = load_external_module(module_name)

    if not module_class:
        module_class = load_from_python_module(module_name)

    if not module_class:
        return None

    module_instance = module_class()
    return module_instance


def load_external_module(module_name):
    searched_entrypoints = []
    for entrypoint in pkg_resources.iter_entry_points('fload_modules'):
        searched_entrypoints.append(entrypoint)
        module = entrypoint.load()
        if hasattr(module, module_name):
            module_class = getattr(module, module_name)
            logger.debug('module loaded from %s, %s', entrypoint, module)
            return module_class
    logger.debug('no module found in entrypoints %s', searched_entrypoints)


def load_from_python_module(module_name):
    try:
        m, c = module_name.split(':', 1)
        module_loaded = importlib.import_module(m)
        class_loaded = getattr(module_loaded, c)
        logger.debug('module loaded from %s, %s', module_loaded, c)
        return class_loaded
    except (ModuleNotFoundError, AttributeError, ValueError) as ex:
        logger.warn('load module error, %s', ex)
        pass


def _pop_module_name(argv):
    i = 0
    for arg in argv[1:]:
        if not arg.startswith('-'):
            del argv[i]
            return arg
        i += 1


def main():
    from fload import __version__ as version
    argv = sys.argv

    usage = '%(prog)s command\r\n'
    parser = argparse.ArgumentParser('fload', usage=usage)
    parser.add_argument('-V', '--version', action='version', default=False,
                    version='%(prog)s {version}'.format(version=version))
    # parser.add_argument('module')
    module_name = _pop_module_name(argv)
    # ops = parser.parse_args()
    

    if module_name is None:
        ops = parser.parse_args()
        if not module_name and ops.version:
            print('fload %s' % version)
            sys.exit(0)

        print('Please specify command.')
        parser.print_help()
        sys.exit(1)

    setup_logging()

    mod = load_module(module_name)
    if mod is None:
        parser.error("module %s not found." % module_name)

    if hasattr(mod, 'add_arguments'):
        getattr(mod, 'add_arguments')(parser)

    parser.usage = f'fload {module_name}'
    ops = parser.parse_args()
    
    if hasattr(mod, 'init'):
        getattr(mod, 'init')(ops)
   
    
    for line in sys.stdin:
        item = json.loads(line)
        try:
            ret = mod.process(item)
            
            if ret:
                print(json.dumps(ret))
                sys.stdout.flush()
                
        except Exception as ex:
            logger.error('Error when processing item %s', item, exc_info=ex)
            sys.exit(1)


if __name__ == '__main__':
    main()

