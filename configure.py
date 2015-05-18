from tools import ninja_syntax as ninja




BUILD_FILENAME = 'build.ninja'


"""
Helper class that by default does the right thing to build files for windows 
mingw platform, but can be subclassed to build Maud-lib on other platforms

"""
class BuildActions():
    
    def __init__(self, object_ext='o', lib_ext='lib'):
        pass
    
    


def main():
    
    ninja_writer = ninja.Writer(open(BUILD_FILENAME, 'w'))
    n = ninja_writer

    n.comment('Empty build')
    
    n.rule('cc', 'gcc $cflags -c $in -o $out')
    n.build('./build/helloworld_bin.o', 'cc', './src/apps/helloworld/helloworld_bin.cc')
    
    n.rule('exe', 'gcc $cflags -o $out $in ')
    n.build('./build/helloworld_bin.exe', 'exe', './build/helloworld_bin.o')
    n.close()
    
if __name__ == '__main__':
    main()
    