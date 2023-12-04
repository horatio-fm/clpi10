"""
Generates 'my_package'.version.__file__ which is NOT in the GIT repo.
This is specific for every worktree.
"""
import importlib
import os
import re
import subprocess
import getpass
import sys
from pathlib import Path

project_path = os.path.dirname(os.path.dirname(__file__))
project_name = os.path.basename(project_path)

module_name = re.sub(r'\d+$', '', project_name)
module_path_dir = os.path.join(project_path, module_name)
module_path_file = os.path.join(project_path, module_name, module_name + ".py")

if not os.path.exists(module_path_dir):
    os.makedirs(module_path_dir)
    Path(os.path.join(module_path_dir, "__init__.py")).touch()
    # proc = subprocess.Popen(f'git add {os.path.join(module_path_dir, "__init__.py")}', stdout=subprocess.PIPE, shell=True)
if not os.path.exists(module_path_file):
    # Path(module_path_file).touch()
    with open(module_path_file, "w") as fp:
        fp.write(f"""
import argparse
import os


from {module_name}.version import version
__version__ = version


def main():

    parser = argparse.ArgumentParser(description='Description of {module_name}')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    args = parser.parse_args()


if __name__ == '__main__':
    main()

""")
    # proc = subprocess.Popen(f'git add {module_path_file}', stdout=subprocess.PIPE, shell=True)



my_package = importlib.import_module(module_name)

version_file = os.path.join(os.path.dirname(my_package.__file__), "version.py")
# if not os.path.exists(my_package.version.__file__):
if not os.path.exists(version_file):
    Path(version_file).touch()

my_package.version = importlib.import_module(module_name + ".version")

username = getpass.getuser()

git = "git"

proc = subprocess.Popen('{0} diff --exit-code'.format(git), stdout=subprocess.PIPE, shell=True)
info = proc.communicate()[0].decode("utf-8").rstrip()

if proc.returncode != 0:
    print("There are local changes in the working directory!!")
    print("There are local changes in the working directory!!")
    print("There are local changes in the working directory!!")
    print("There are local changes in the working directory!!")
    print("There are local changes in the working directory!!")
    print("DDD!!")
    sys.exit(1)

proc = subprocess.Popen('{0} rev-list --count HEAD'.format(git), stdout=subprocess.PIPE, shell=True)
count = proc.communicate()[0].decode("utf-8").rstrip()

if count == '1':
    proc = subprocess.Popen('{0} tag v0.0.0'.format(git), stdout=subprocess.PIPE, shell=True)

proc = subprocess.Popen('{0} describe --tags'.format(git), stdout=subprocess.PIPE, shell=True)
version = proc.communicate()[0].decode("utf-8").rstrip()

proc = subprocess.Popen('{0} rev-parse --short HEAD'.format(git), stdout=subprocess.PIPE,
                        shell=True)
hashkey = proc.communicate()[0].decode("utf-8").rstrip()

proc = subprocess.Popen('{0} rev-parse --git-dir'.format(git), stdout=subprocess.PIPE, shell=True)
git_dir = proc.communicate()[0].decode("utf-8").rstrip()

if len(version.split("-")) > 1:
    version = "-".join(version.split("-")[:-1] + [hashkey])
else:
    version = "-".join([version, hashkey])

proc = subprocess.Popen('{0} rev-parse --abbrev-ref HEAD'.format(git), stdout=subprocess.PIPE,
                        shell=True)
current_branch = proc.communicate()[0].decode("utf-8").rstrip()

proc = subprocess.Popen('{0} show -s --format=%ci HEAD'.format(git), stdout=subprocess.PIPE,
                        shell=True)
time_of_commit = proc.communicate()[0].decode("utf-8").rstrip()
time_of_commit = time_of_commit.replace(" ", "_")
time_of_commit = time_of_commit.replace(":", "-")


from .install_hooks import hook_text_list
with open(my_package.version.__file__, "w") as fp:
    fp.write(f'''"""
Warning: This file is automatically generated by the following GIT hooks:{hook_text_list}
It is NOT in the repository. It is specific for every worktree.
"""

''')
    fp.write("version = '")
    fp.write("__".join([version, time_of_commit, current_branch]))
    fp.write("'")


def create_bin_folder():

    global module_path_dir
    bin_path_dir = os.path.join(module_path_dir, "bin")
    if not os.path.exists(bin_path_dir):
        os.makedirs(bin_path_dir)
        bin_path_module = os.path.join(bin_path_dir, f"{module_name}_main.py")
        with open(bin_path_module, "w") as fp:
            fp.write(f"""
from {module_name}.{module_name} import main as exe_start


def main():

    exe_start()


if __name__ == '__main__':
    main()

""")
        # proc = subprocess.Popen(f'git add {bin_path_module}', stdout=subprocess.PIPE, shell=True)


create_bin_folder()

