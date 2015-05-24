from tools import ninja_syntax as ninja

import os
from tools import convert_config



BUILD_FILENAME = 'build.ninja'



def builddir(*path):
    return os.path.join('$builddir', *path)
    
def buildconfig(*path):
    return os.path.join('$builddir', 'config', *path)
    
def tooldir(*path):
    return os.path.join('tools', *path)
    
def srcdir(*path):
    return os.path.join('src', *path)
    
def application(*path):
    return os.path.join('src', 'app', *path)
    
def collect_configs(path):
    result = []
    for root, dirs, files in os.walk(path):
        matches = [os.path.join(root, name) for name in files if name.endswith('.cfg')]
        if len(matches) > 0:        
            result.append(*matches)
    return result


"""
Helper class that by default does the right thing to build files for windows 
mingw platform, but can be subclassed to build Maud-lib on other platforms

#"""
class BuildActions():
    
    def __init__(self, ninja, prefix, obj_ext='.o', lib_ext='.a', prog_ext='.exe'):
        self.ninja = ninja
        self.prefix = prefix
        self.obj_ext = obj_ext
        self.lib_ext = lib_ext
        self.prog_ext = prog_ext
        
        
    def object(self, rule, input_file):
        obj_name, ext = os.path.splitext(input_file)
        return self.ninja.build(builddir(obj_name+self.obj_ext),
                                self.prefix + rule,
                                input_file,
                                implicit = buildconfig('configured'))[0]
    

def main():
    
    ninja_writer = ninja.Writer(open(BUILD_FILENAME, 'w'))
    n = ninja_writer

    try:
        configs = collect_configs(path='src')
        
        for config in configs:
            print(config)
            
    finally:
        n.close()
    
#    n.comment('Empty build')
#    n.variable('cflags', '-Wall')
#    n.rule('cc', 'gcc $cflags -c $in -o $out')
#    n.build('./build/helloworld_bin.o', 'cc', './src/apps/helloworld/helloworld_bin.cc')
#    
#    n.rule('exe', 'gcc $cflags -o $out $in ')
#    n.build('./build/helloworld_bin.exe', 'exe', './build/helloworld_bin.o')
#    n.close()

    
    
if __name__ == '__main__':
    main()
    