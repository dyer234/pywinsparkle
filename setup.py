from setuptools import setup, Distribution
#from pypandoc import convert_file

class BinaryDistribution(Distribution):
    def has_ext_modules(foo):
        return True


#: Converts the Markdown README in the RST format that PyPi expects.
#long_description = convert_file('README.md', 'rst')


setup(name='pywinsparkle',
      description='A python wrapper for the winsparkle project',
      long_description='A python wrapper for the winsparkle project',
      version='1.5.0',
      url='https://github.com/dyer234/pywinsparkle',
      author='Daniel Dyer',
      author_email='dyer234@gmail.com',
      license='MIT',
      keywords="sparkle winsparkle windows update",
      test_suite='nose.collector',
      tests_require=['nose'],
      packages=["pywinsparkle"],
      package_data= { "pywinsparkle" : ["libs/x64/WinSparkle.dll", "libs/x86/WinSparkle.dll"] },
      classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 5 - Production/Stable',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Topic :: Software Development',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
      ],
      include_package_data=True,
      distclass=BinaryDistribution,
)
