try:
    from setuptools import setup
except ImportError:
    # can't have the entry_points option here.
    from distutils.core import setup

setup(name='presentation2html',
      version='1.0.0',
      author="Ahmed T. Youssef",
      author_email="xmonader@gmail.com",
      description='convert google presentations to reveal.js website',
      long_description='convert google presentations to reveal.js website',
      packages=['presentation2html'],
      scripts=['scripts/slides2html'],
      url="https://github.com/threefoldtech/presentation2html",
      license='BSD 3-Clause License',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
      ],
      )