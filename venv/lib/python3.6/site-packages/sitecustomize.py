# This file is created by Homebrew and is executed on each python startup.
# Don't print from here, or else python command line scripts may fail!
# <https://docs.brew.sh/Homebrew-and-Python.html>
import re
import os
import sys

if sys.version_info[0] != 3:
    # This can only happen if the user has set the PYTHONPATH for 3.x and run Python 2.x or vice versa.
    # Every Python looks at the PYTHONPATH variable and we can't fix it here in sitecustomize.py,
    # because the PYTHONPATH is evaluated after the sitecustomize.py. Many modules (e.g. PyQt4) are
    # built only for a specific version of Python and will fail with cryptic error messages.
    # In the end this means: Don't set the PYTHONPATH permanently if you use different Python versions.
    exit('Your PYTHONPATH points to a site-packages dir for Python 3.x but you are running Python ' +
         str(sys.version_info[0]) + '.x!\n     PYTHONPATH is currently: "' + str(os.environ['PYTHONPATH']) + '"\n' +
         '     You should `unset PYTHONPATH` to fix this.')

# Only do this for a brewed python:
if os.path.realpath(sys.executable).startswith('/usr/local/Cellar/python3'):
    # Shuffle /Library site-packages to the end of sys.path
    library_site = '/Library/Python/3.6/site-packages'
    library_packages = [p for p in sys.path if p.startswith(library_site)]
    sys.path = [p for p in sys.path if not p.startswith(library_site)]
    # .pth files have already been processed so don't use addsitedir
    sys.path.extend(library_packages)

    # the Cellar site-packages is a symlink to the HOMEBREW_PREFIX
    # site_packages; prefer the shorter paths
    long_prefix = re.compile(r'/usr/local/Cellar/python3/[0-9._abrc]+/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages')
    sys.path = [long_prefix.sub('/usr/local/lib/python3.6/site-packages', p) for p in sys.path]

    # Set the sys.executable to use the opt_prefix
    sys.executable = '/usr/local/opt/python3/bin/python3.6'
