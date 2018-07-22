from glob import glob
from os import path, mkdir
from shutil import copyfile
from pkg_resources import parse_version
from setuptools import setup, find_packages
from setuptools.command.install import install

ROOT_DIR = path.dirname(__file__)


class InstallWithDirectorySetup(install):

    def run(self):
        # run the normal setuptools installation
        install.run(self)

        # create a working data directory for the application in the user's directory
        root_dir = path.join(path.expanduser("~"), ".dinner_time")
        config_fn = path.join("conf", "cfg.json")
        if not path.exists(root_dir):
            mkdir(root_dir)
            copyfile(config_fn, root_dir)


# Read requirements
fn = path.join(ROOT_DIR, 'requirements.txt')
with open(fn, 'r') as fh:
    requirements = [str(x).strip() for x in fh.readlines()]

# Read from and write to the version file
fn = path.join(ROOT_DIR, "dinner_time", "_version.py")
with open(fn, 'r+') as fh:
    version_found = False
    while not version_found:
        vpos = fh.tell()
        line = fh.readline()
        if line == '':
            # reached EOF without finding the version
            # End of file
            raise ValueError("Could not find __version__ in %s." % fn)
        elif line.startswith('__version__'):
            exec(line)
            version_found = True

# Get list of data files
data_files = ['README.md'] + glob('conf/*')

setup(
    name="dinner-time",
    version=__version__,
    description="Tagging-based, localized meal data store.",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering"
    ],
    url="https://github.com/aagnone3/dinner-time",
    author="Anthony Agnone",
    author_email="anthonyagnone@gmail.com",
    packages=find_packages(exclude=['*.test', 'test']),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'get_recipes = dinner_time.tools.get_recipes:main'
        ]
    },
    cmdclass={
        "install": InstallWithDirectorySetup
    },
    zip_safe=False,
    data_files=[('share/aagnone/dinner_time', data_files)]
)
