import os
import pathlib
import shutil
import sys

from setuptools import Command, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

GITHUB_URL = "https://github.com/dheerajreal/random-strings/"
VERSION = '0.1.1'


class PublishCommand(Command):
    """Support setup.py publish."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Print things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing older builds")
            shutil.rmtree(os.path.join(here, "dist"))
        except FileNotFoundError:
            print("No older builds exist, Do nothing")

        self.status("Building Source and Wheel")
        os.system("{0} setup.py sdist bdist_wheel".format(sys.executable))

        self.status("Uploading to PyPi using Twine")
        os.system("twine upload dist/*")

        sys.exit()


setup(
    name='random-strings',
    version=VERSION,
    license='MIT',
    description='strings that are ✨ random ✨',
    url=GITHUB_URL,
    keywords=['random', 'strings', 'utilities', 'security'],
    py_modules=["random_strings"],
    python_requires='>=3.6, <4',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_file="LICENSE.txt",

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only'
    ],

    project_urls={
        'Bug Reports': GITHUB_URL + 'issues/',
        'Source': GITHUB_URL,
    },
    # setup.py publish
    cmdclass={
        "publish": PublishCommand,
    },
)
