#!/usr/bin/env python

import sys
import os
import argparse
import glob

import config
import builder


def list_version(arguments):
    component = arguments.component
    component_package_dir = os.path.join(config.get_config()['package_dir'], component)  
    if (os.path.isdir(component_package_dir)):
        for dirname in glob.glob(os.path.join(component_package_dir, component + "_*")):
            print "{}".format(os.path.split(dirname)[1])

def package(arguments):
    component = arguments.component
    builder.package_component(arguments.component)

def switch_version(arguments):
    component = arguments.component
    component_package_dir = os.path.join(config.get_config()['package_dir'], component)  
    deploy_dir = config.get_config()['deploy_dir']

    if (not os.path.exists(deploy_dir)):
        os.makedirs(deploy_dir)
    
    os.symlink(os.path.join(component_package_dir, arguments.target_version),
        os.path.join(deploy_dir, component))

def build(arguments):
    component = arguments.component
    builder.build_component(arguments.component)

def noop(*__):
    pass

def run(arguments):
    runner = {
        'list': list_version,
        'build': build,
        'package': package,
        'switch': switch_version
    } 
    runner.get(arguments.action, noop)(arguments)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('action')
    parser.add_argument('component')
    parser.add_argument('-c', '--config', dest='config_file')
    parser.add_argument('--to', dest='target_version')

    arguments = parser.parse_args()
    if arguments.config_file is not None:
        config.read_config_file(arguments.config_file)
    else:
        config.read_config_file()
    
    run(arguments);
    
