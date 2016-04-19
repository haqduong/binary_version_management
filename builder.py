import os
import shutil
import glob
import config
import time
from subprocess import call

def build_component(component_name):
    source_dir = config.get_config()['source_dir']
    build_dir = config.get_config()['build_dir']
    
    component_src = os.path.join(source_dir, component_name)
    component_build_dir = os.path.join(build_dir, component_name)

    if (not os.path.exists(component_build_dir)):
        os.makedirs(component_build_dir)

    qmake_file = os.path.join(component_src, "{0}.pro".format(component_name))
    current_dir = os.getcwd()
    os.chdir(component_build_dir)
    # /usr/bin/qmake-qt4 -r -spec /usr/share/qt4/mkspecs/linux-g++ $DEBUG_FLAGS -o Makefile $SOURCE_DIR/VEWS/Server/Server.pro
    call(['/usr/bin/qmake-qt4', '-r',
        '-spec', '/usr/share/qt4/mkspecs/linux-g++',
        '-o', 'Makefile',
        qmake_file]) 
    call(['make', '-j4'])

def package_common_lib():
    program_lib_dirs = os.path.join(config.get_config()['source_dir'],
                           'libs')
    thirdparty_lib_dirs = os.path.join(config.get_config()['source_dir'],
                           'Thirdparty', 'lib', 'x64')
    output_lib_dirs = os.path.join(config.get_config()['package_dir'], 'libs')
    if not os.path.exists(output_lib_dirs):
        os.makedirs(output_lib_dirs)
    for filename in glob.glob(os.path.join(program_lib_dirs, "*")):
        shutil.copy2(filename, output_lib_dirs)
    for filename in glob.glob(os.path.join(thirdparty_lib_dirs, "*")):
        shutil.copy2(filename, output_lib_dirs)

def package_component(component_name):
    package_common_lib()
    binary_dir = os.path.join(config.get_config()['package_dir'], 'temp')
    output_lib_dirs = os.path.join(config.get_config()['package_dir'], 'libs')
    package_dir = config.get_config()['package_dir']
    component_package_dir = os.path.join(config.get_config()['package_dir'], component_name)  
    if not os.path.exists(component_package_dir):
        os.makedirs(component_package_dir)

    if os.path.exists(binary_dir):
        shutil.rmtree(binary_dir)
    os.makedirs(binary_dir)

    build_dir = os.path.join(config.get_config()['build_dir'], component_name)
    if not os.path.exists(build_dir):
        print "Build dir does not exists"
        return

    shutil.copytree(os.path.join(build_dir, 'MainApp'), os.path.join(binary_dir, 'MainApp'))
    shutil.copytree(os.path.join(build_dir, 'plugins'), os.path.join(binary_dir, 'plugins'))
    os.symlink(output_lib_dirs, os.path.join(binary_dir, 'libs'))
    
    os.chdir(package_dir)
    call(['tar', 'cjf', os.path.join(component_package_dir, 
        "{0}_{1}.tar.gz".format(component_name, time.strftime('%y%m%d.%H%M'))),
        '-h', 'temp'])
    
    shutil.rmtree('temp')
 
