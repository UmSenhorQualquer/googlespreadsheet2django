# Google spreadsheet to Django.

This library uses a Google SpreadSheet to generates django applications.

## Why using a Google SpreadSheet to configure a database?

- The google spreadsheet works as an function analysis document that can be presented to the database stakeholders. By using the spreadsheet document to generate code, the devolper makes sure that is code is acording to what was requested by the stakeholders.
- One other advantage is that the google spreadsheet document can be edited in colaboration with several users at the same time.
- Also all the changes are tracked in the document history log.

## How to use:

* [Create a Django project](https://docs.djangoproject.com/en/1.8/intro/)tutorial01/)
* Download and unstall the library googlespreadsheet2django using the command: python setup.py install
* Make a copy of the [Google SpreadSheet document](https://docs.google.com/spreadsheets/d/1HWhdkKIHUK-tOEJWEp6gVh3evyV1YipgqV7QeTsUtYI/edit?usp=sharing) and edit the tables and fields of your database.
* Share the document to everyone with the link (this is necessary for the script to download the file).
* Open the terminal and move from your current directory to the created django project directory.
* Use the command: gsheet2django "<id of the google spreasheet document>" to generate the code of your django applications.