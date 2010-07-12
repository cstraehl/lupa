
import sys
import os
from distutils.core import setup, Extension

extra_setup_args = {}

# check if Cython is installed, and use it if available
try:
    from Cython.Distutils import build_ext
    import Cython.Compiler.Version
    print("building with Cython " + Cython.Compiler.Version.version)
    extra_setup_args['cmdclass'] = {'build_ext': build_ext}
    source_extension = ".pyx"
except ImportError:
    print("building without Cython")
    source_extension = ".c"

# support 'test' target if setuptools/distribute is available

if 'setuptools' in sys.modules:
    extra_setup_args['test_suite'] = 'lupa.tests.suite'

# check if LuaJIT is in a subdirectory and build statically against it

basedir = os.path.abspath(os.path.dirname(__file__))

def find_luajit_build():
    static_libs = []
    include_dirs = []

    os_path = os.path
    for filename in os.listdir(basedir):
        if filename.lower().startswith('luajit'):
            filepath = os_path.join(basedir, filename, 'src')
            if os_path.isdir(filepath):
                libfile = os_path.join(filepath, 'libluajit.a')
                if os_path.isfile(libfile):
                    static_libs = [libfile]
                    include_dirs = [filepath]
                    print("found LuaJIT build in %s" % filepath)
                    print("building statically")
    return dict(extra_objects=static_libs, include_dirs=include_dirs)

ext_modules = [
    Extension(
        'lupa._lupa',
        sources = ['lupa/_lupa'+source_extension],
        **find_luajit_build()
        )
    ]

long_description = '\n\n'.join(
    open(os.path.join(basedir, text_file)).read()
    for text_file in ['README.txt', 'INSTALL.txt'])
    

setup(
    name = "lupa",
    version = '0.1',
    author="Stefan Behnel",
    author_email="stefan_ml (at) behnel.de",
    url="http://pypi.python.org/pypi/lupa",
#    download_url="",

    description="Simple wrapper around LuaJIT",

    long_description=long_description,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Other Scripting Engines',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
    ],

#    package_dir = {'': 'src'},
    packages = ['lupa'],
#    package_data = {},
    ext_modules = ext_modules,
    **extra_setup_args
)