from setuptools import setup
import os
import shutil
import locale
locale.getpreferredencoding = lambda: 'UTF-8'

setup(name="fattybugs",
      version="1.0",
      description="A basic module for working with a primitive bug database",
      long_description="A primitive module and CLI scripts for tracking bugs in a minimalist sqlite database",
      author="Colin Hilchey",
      author_email="colin.hilchey@gmail.com",
      license="MIT",
      package_dir={"":"lib"},
      scripts=["scripts/list_bugs.py","scripts/add_bug.py","scripts/fix_bug.py"],
      install_requires=['python-dateutil',
                        ],
      include_package_data=True,
      zip_safe=False)

