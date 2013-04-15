from setuptools import setup, find_packages

version = '1.0'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='collective.portlet.mailman',
      version=version,
      description="Portlet for subscribing to mailman list",
      long_description=long_description,
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Python",
        ],
      keywords='',
      author='Paul J Stevens',
      author_email='paul@nfg.nl',
      url='',
      license='gpl',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      namespace_packages=['collective', 'collective.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'plone.api',
          'plone.directives.form',
      ],
      extras_require={'test': ['plone.app.testing']},
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
