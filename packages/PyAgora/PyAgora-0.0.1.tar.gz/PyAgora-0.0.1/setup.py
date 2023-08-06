"""
PyAgora v0.0.1: Python Bindings for Agora SDK.

Copyright (c) 2021 Fan Junshuang

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY
OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import platform
import sys
import glob

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

__version__ = "0.0.1"

# distutils will try to locate and link dynamically against agora sdk.
#
# If you would rather statically link in the agora sdk library run:
#
# % python setup.py build --static-link
#
# Specify the environment variable AGORASDK_PATH with the build tree
# of agora sdk.

STATIC_LINKING = False

if "--static-link" in sys.argv:
    STATIC_LINKING = True
    sys.argv.remove("--static-link")

agorasdk_path = './agora'
for arg in sys.argv:
    if arg.startswith('--sdkpath'):
        agorasdk_path = arg[10:]
        sys.argv.remove(arg)

mac_sysroot_path = os.environ.get("SYSROOT_PATH", None)

pyagora_module_sources = ['src/_pyagoramodule.cpp',
                          "src/_agoraobject.cpp",
                          "src/_circlebuffer.cpp",
                          "src/_viewsmanager.cpp",
                          ]
include_dirs = []
external_libraries = []
extra_compile_args = []
extra_link_args = []
scripts = []
defines = []
data_files = []
data_files += [('example', glob.glob('./example/*py'))]
data_files += [('data', glob.glob('./data/*'))]

if sys.platform == 'darwin':
    defines += [('MACOSX', '1')]
    if mac_sysroot_path:
        extra_compile_args += ["-isysroot", mac_sysroot_path]
        extra_link_args += ["-isysroot", mac_sysroot_path]
    extra_link_args += ['-F', os.path.join(agorasdk_path, 'libs')]
    extra_link_args += ['-framework', 'AgoraRtcKit']
    include_dirs = [os.path.join(agorasdk_path, 'libs/AgoraRtcKit.framework/Versions/A/Headers')]
    extra_compile_args += ['-std=c++11']
elif sys.platform == 'win32':
    bits = platform.architecture()[0]
    if '64' in bits:
        defines.append(('MS_WIN64', '1'))
        extra_link_args = [
            os.path.join(agorasdk_path, 'libs/x86_64/agora_rtc_sdk.lib')
        ]
        data_files += [('', glob.glob(os.path.join(agorasdk_path, 'libs/x86_64/*')))]
    else:
        extra_link_args = [
            os.path.join(agorasdk_path, 'libs/x86/agora_rtc_sdk.lib')
        ]
        data_files += [('', glob.glob(os.path.join(agorasdk_path, 'libs/x86/*')))]
    include_dirs = [os.path.join(agorasdk_path, 'libs/include/')]

data_files += [('', glob.glob(os.path.join(agorasdk_path, 'libs/include/*.h')))]
data_files += [('', glob.glob('src/*.h'))]
'''
    # platform specific configuration
    if sys.platform == 'darwin':
        extra_link_args += ['-framework', 'CoreAudio',
                            '-framework', 'AudioToolbox',
                            '-framework', 'AudioUnit',
                            '-framework', 'Carbon']
    elif sys.platform == 'cygwin':
        external_libraries += ['winmm']
        extra_link_args += ['-lwinmm']
    elif sys.platform == 'win32':
        # i.e., Win32 Python with mingw32
        # run: python setup.py build -cmingw32
        external_libraries += ['winmm']
        extra_link_args += ['-lwinmm']
    elif sys.platform == 'linux2':
        extra_link_args += ['-lrt', '-lm', '-lpthread']
        # GNU/Linux has several audio systems (backends) available; be
        # sure to specify the desired ones here.  Start with ALSA and
        # JACK, since that's common today.
        extra_link_args += ['-lasound', '-ljack']
'''

setup(name='PyAgora',
      version=__version__,
      author="Fan",
      url="",
      description='AgoraSdk Python Bindings',
      long_description=__doc__.lstrip(),
      scripts=scripts,
      py_modules=['pyagora'],
      package_dir={'': 'src'},
      data_files=data_files,
      ext_modules=[
          Extension('_pyagorasdk',
                    sources=pyagora_module_sources,
                    include_dirs=include_dirs,
                    define_macros=defines,
                    libraries=external_libraries,
                    extra_compile_args=extra_compile_args,
                    extra_link_args=extra_link_args)
      ])
