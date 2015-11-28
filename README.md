# Google spreadsheet to Django.

This library uses a Google SpreadSheet to generates django applications.

## Why using a Google spreadsheet to configure a database?

- The Google spreadsheet works as a function analysis document that can be presented to the database stakeholders. By using the spreadsheet document to generate code the devolper makes sure that is code is according to what was agreed with the stakeholders.
- One other advantage is that the Google spreadsheet document can be edited in colaboration with several users at the same time. Also all the changes are tracked in the document history log.

## How to use

1. [Create a Django project](https://docs.djangoproject.com/en/1.8/intro/tutorial01/)
2. Download and install the library googlespreadsheet2django using the command: python setup.py install
3. Make a copy of the [Google SpreadSheet document](https://docs.google.com/spreadsheets/d/1HWhdkKIHUK-tOEJWEp6gVh3evyV1YipgqV7QeTsUtYI/edit?usp=sharing) and edit the tables and fields of your database.
4. Share the document to everyone with the link (this is necessary for the script to download the file).
5. Open the terminal and move from your current directory to the created django project directory.
6. Use the command: gsheet2django "<id of the Google spreasheet document>" to generate the code of your django applications.

#### The generated code result

For the template Google spreadsheet it will generates the next files:

```sh
├── details  
│   ├── abstractmodels  
│   │   ├── Country.py  
│   │   ├── __init__.py  
│   │   └── Person.py  
│   ├── admins  
│   │   ├── CountryAdmin.py  
│   │   ├── __init__.py  
│   │   └── PersonAdmin.py  
│   ├── __init__.py  
│   ├── models.py  
│   └── admin.py  
└── static  
    └── js  
        └── models  
            ├── country.js  
            └── person.js  
```

- The abstractmodels and admins folders describes the Models and their visualisation in the admin interface. The files on these folders should not be touched, never!! because they will be replaced everytime you generate a new code.
- In the files models.py and admin.py you will see comments like this one:
```python
##### auto:start:Person #####
... some code ...
	##### auto:end:Person #####
```
These comments indicate which parts of the code would be replaced when ever you generate a new code based on the spreadsheet. Every code outside these comments would be kept, which means that you can use these files to add extra rules or fields to your application.
- The static -> js files implement the hide and show rules of the fields vs values.

<br>
<br>
<br>
<br>
<br>
<br>
------------------------------------------------------------------------------

## The Google spreadsheet format

#### Applications tab

![Applications tab](docs/imgs/applications_tab.png?raw=true "Screen")

In the "Applications" tab we will see a column the title "Applications" as in the image bellow. Here we should add in each row the django applications we would like to generate. 

![Applications tab](docs/imgs/applications_list.png?raw=true "Screen")

The names should respect the django syntax for applications names, and each application should be added in a new row bellow the column "Applications".

#### Add a new table

To add a new table we should select the option "Database application -> Add new table" in the Google spreadsheet main menu, as in the image bellow.

![New table](docs/imgs/new_table.png?raw=true "Screen")

After you select the option a popup window will ask you for the name of the new table.

![Table name popup](docs/imgs/tablename_popup.png?raw=true "Screen")

After the Ok, a new tab will be generated with the format "Table_#name you gave for the table#".  
On the top of the tab spreadsheet we will configure for which application the tab bellongs to in the field <Select an application>. If we click on this field, a dropdown box will be shown with the available applications configured in the tab "Applications".

![Table header](docs/imgs/table_header.png?raw=true "Screen")

The fields <Table singular label> and <Table plurar label> are the names of the tables that will be used in the Django admin interface.

The field <Data access> allow us to configure which type of access we will have to this table. Check the available options in the image bellow.

![Table data access](docs/imgs/table_data_access.png?raw=true "Screen")