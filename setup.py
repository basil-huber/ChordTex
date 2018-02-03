from setuptools import setup

setup(name='chordTex',
      version='0.1',
      description='Program and Library to generate PDF of chords and tabs',
      author='Basil',
      author_email='basil.huber@gmail.com',
      license='Free',
      packages=['chordTex', 'chordTex.chordImporter', 'chordTex.latex'],
      entry_points = {'console_scripts': ['chord_import=chordTex.command_line:chord_import']},
      zip_safe=False)