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

After the Ok, a new tab will be generated with the format "Table_\<name you gave for the table\>".  
On the top of the tab spreadsheet we will configure for which application the tab bellongs to in the field \<Select an application\>. If we click on this field, a dropdown box will be shown with the available applications configured in the tab "Applications".

![Table header](docs/imgs/table_header.png?raw=true "Screen")

The fields \<Table singular label\> and \<Table plural label\> are the names of the tables that will be used in the Django admin interface.

The field \<Data access\> allow us to configure which type of access we will have to this table. Check the available options in the image bellow.

![Table data access](docs/imgs/table_data_access.png?raw=true "Screen")

#### Add fields to the table

By default the table is added with the primary key set.

![Default fields](docs/imgs/default_fields.png?raw=true "Screen")

To add new fields you should use the option "Database application -> Add new field" in the Google spreadsheet main menu, as in the image bellow.

![New field](docs/imgs/new_field.png?raw=true "Screen")

A new row will appear in the spreadsheet, where you should configure your field properties.

The field configurations columns details are explained in the table bellow.


| Column                                        | Value                                     | Description                           |
| --------------------------------------------- | ----------------------------------------- | ------------------------------------- |
| Field label                                   | Free text                                 |                                       |
| Database field name                           | SQL column format                         |                                       |
| Tab                                           | Free text                                 | Tells in which tab the field should be shown. ![Tabs](docs/imgs/django-suit-tabs.png?raw=true "Screen")     |
| Group                                         | Free text                                 | Tells in which group the field should be shown. ![Group](docs/imgs/django-suit-group.png?raw=true "Screen") |
| Type of field                                 | It is possible to select the next options:|                                       |
|                                               | Created by user                           | It generates a read-only field which will store the user that created each a table record. |
|                                               | Creation date and time                    | It generates a read-only field which will store the date and time when the table record was created. |
|                                               | Date                                      | ![Date field](docs/imgs/django-suit-date.png?raw=true "Screen") |
|                                               | Date time                                 | ![Date time field](docs/imgs/django-suit-datetime.png?raw=true "Screen") |
|                                               | Decimal number                            | ![Decimal field](docs/imgs/django-suit-decimal.png?raw=true "Screen") |
|                                               | Decimal numbers range                     |                                       |
|                                               | Dropdown list                             | ![Dropdown field](docs/imgs/django-suit-dropdown.png?raw=true "Screen") |
|                                               | Email                                     | Like the text field, but validates if the input value respect the email format. |
|                                               | File                                      | ![File field](docs/imgs/django-suit-file.png?raw=true "Screen") |
|                                               | Foreign key                               | Like a dropdown list but the values are from a table. |
|                                               | Function                                  |                                       |
|                                               | Integer                                   | Like a small text field, but it validates if the value is an integer. |
|                                               | Integers range                            | Like the Integer field, but it validates a lower and upper bounds. |
|                                               | Multiple choice                           | ![Multiple choice field](docs/imgs/django-suit-multiplechoice.png?raw=true "Screen") |
|                                               | Number of identification                  | Read-only field, it works as primary key. |
|                                               | Radio buttons list                        |                                       |
|                                               | Slug                                      |                                       |
|                                               | Small text                                | ![Text field](docs/imgs/django-suit-text.png?raw=true "Screen") |
|                                               | Text                                      | Textarea field. |
|                                               | Update date and time                      | Read-only field. Stores the date time of a record last update. |
|                                               | Updated by user                           | Read-only field. Stores the user which made the last update. |
|                                               | Boolean                                   | ![Boolean field](docs/imgs/django-suit-boolean.png?raw=true "Screen") |
| Field format                                  | The field will have "Auto generated" value or a dropdown list depending on the "Type of field" column value. |             |
| Possible answers                              | The field will be empty or a dropdown with the values from the "Answers" tab of the spreadsheet, depending on the "Type of field" column value.|        |
| Mandatory                                     | Yes/No                                    |                                       |
| Depends on another field's answer             | Dropdown listing the fields of the table. |                          |
| Show the field when these values are selected | Values separed by ";"                     |                                       |
| Help label                                    | Free text                                 |                                       |
| Visible                                       | Yes/No                                    |                                       |
| Show in the list by order                     | Integer                                   | The name will be constructed by the order of the values of this column. |
| Show filter                                   | Yes/No                                    |                                       |
| Use as search field                           | Yes/No                                    |                                       |
| Use on name                                   | Integer                                   |                                       |
| Unique                                        | Yes/No                                    |                                       |
| Default value                                 | Free value                                |                                       |