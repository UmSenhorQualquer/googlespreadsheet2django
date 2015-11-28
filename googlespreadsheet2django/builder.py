# -*- coding: utf-8 -*-
import argparse, os, requests, xlrd
from googlespreadsheet2django.models.models_loader import ModelsLoader
from googlespreadsheet2django.answers.answers_loader import AnswersLoader

def export_code(documentID, path):
	INPUTFILE 	= os.path.join(path, documentID+'.xlsx' )

	r = requests.get('https://docs.google.com/spreadsheet/ccc?key=%s&output=xlsx' % documentID)
	outfile = open(INPUTFILE, 'wb'); outfile.write(r.content); outfile.close()

	workbook = xlrd.open_workbook( INPUTFILE )
	answers = AnswersLoader(workbook)
	models = ModelsLoader(workbook, answers)

	models.saveModel(path)
	models.updateModel(path)
	models.saveAdmin(path)
	models.updateAdmin(path)
	models.saveJs(path)

	os.remove(INPUTFILE)

	return models.applications


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("googlespreadsheetid")
	parser.add_argument("--export-path", default='.')
	args = parser.parse_args()

	export_code(args.googlespreadsheetid, args.export_path)
	

if __name__ == "__main__": main()