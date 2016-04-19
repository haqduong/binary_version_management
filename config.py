import os
import yaml


__default_config = { "source_dir" : os.path.expanduser('~/src'),
    "build_dir" : os.path.expanduser('~/build'),
    "package_dir" : os.path.expanduser('~/package'),
    "deploy_dir" : os.path.expanduser('~/deploy') }

__config = dict()

def get_config():
    return __config

def default_config_file():
    return os.path.expanduser('~/.config/bvm.yml')    

def write_default_config(config_file=default_config_file()):
    global __default_config
    print 'Creating default configuration file...'
    with open(config_file, "w") as f:
        f.write(yaml.dump(__default_config))
    print 'Done'

def read_config_file(config_file=default_config_file()):
    global __config
    print "Configuration file: {}".format(config_file)
    print 'Reading configuration file...'
    if (os.path.exists(config_file)):
        stream = file(config_file, 'r')
        __config = yaml.load(stream)
        print 'Done'
        return __config
    else:
        write_default_config(config_file) 
        __config = __default_config
        print 'Done'
        return __config
