from setuptools import setup

setup(name='sbol3',
      version='1.0b5',
      description='Python implementation of SBOL 3 standard',
      python_requires='>=3.7',
      url='https://github.com/SynBioDex/pySBOL3',
      author='Tom Mitchell',
      author_email='tcmitchell@users.noreply.github.com',
      license='MIT License',
      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 4 - Beta',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',

      ],
      # What does your project relate to?
      keywords='synthetic biology',
      packages=['sbol3'],
      package_data={'sbol3': ['rdf/sbol3-shapes.ttl']},
      install_requires=[
            'rdflib==5',
            'rdflib-jsonld',
            'python-dateutil',
            'pyshacl==0.14',
            'requests',
      ],
      test_suite='test',
      tests_require=[
            'pycodestyle>=2.6.0'
      ])
