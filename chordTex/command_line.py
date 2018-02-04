from chordTex.chordImporter.ultimate_guitar import UltimateGuitarParser
from chordTex.latex.leadsheets_writer import LeadsheetsWriter
from argparse import ArgumentParser

def chord_import():
	print('hallo')

	argparser = ArgumentParser()
	argparser.add_argument('url')
	argparser.add_argument('filename')
	args = argparser.parse_args()

	with UltimateGuitarParser(LeadsheetsWriter) as parser:
		parser(args.url, args.filename)