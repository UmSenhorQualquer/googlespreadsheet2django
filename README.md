# Google spreadsheet to django.

The library uses a Google spreadsheet to generates django applications.

## Why using a Google spreadsheet to configure a database?

- The Google spreadsheet works as a functional and technical analysis document that can be presented to the database stakeholders. By using the spreadsheet document to generate code the developer makes sure that his code is according to what was agreed with the stakeholders.
- One other advantage is that the Google spreadsheet document can be edited in colaboration with several users at the same time. Also all the changes are tracked in the document history log.

## How to use

1. Create a [django project](https://docs.djangoproject.com/en/1.8/intro/tutorial01/) and [configure](http://django-suit.readthedocs.org/en/develop/) the [django-suit](http://djangosuit.com/) application.
2. Download and install the library googlespreadsheet2django using the command: python setup.py install
3. Make a copy of this [Google spreadsheet document](https://docs.google.com/spreadsheets/d/1HWhdkKIHUK-tOEJWEp6gVh3evyV1YipgqV7QeTsUtYI/edit?usp=sharing) and edit the tables and fields of your database.
4. Configure the document to be shared with everyone with the link (this is necessary for the code generator script to download the file).
5. Open the terminal and go to the created django project directory.
6. Use the command: gsheet2django "\<id of the Google spreasheet document\>" to generate the code of your django applications.
7. Add the new applications to the settings.py file.

#### The generated code result

For the Google spreadsheet template, the gsheet2django will generate the next files:

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

- The abstractmodels and admins folders describes the Models, and their visualisation in the admin interface. The files on these folders should not be touched, never!! because they will be replaced everytime you generate a the code.
- In the files models.py and admin.py you will see comments like these ones:
```python
##### auto:start:Person #####
... some code ...
    ##### auto:end:Person #####
```
These comments indicate which parts of the code would be replaced when ever you generate a new code based on the spreadsheet. All the code outside these comments will be kept, which means that you can use these files to add extra rules or fields to your application.
- The static -> js files implement the hide and show rules of the fields.

<br>
<br>
<br>
<br>
<br>
<br>

## The Google spreadsheet format

#### Applications tab

![Applications tab](docs/imgs/applications_tab.png?raw=true "Screen")

In the "Applications" tab we will see a column the title "Applications" as in the image below. Here we should add in each row the django applications which we would like to generate.

![Applications tab](docs/imgs/applications_list.png?raw=true "Screen")


#### Add a new table

To add a new table we should select the option "Database application -> Add new table" in the Google spreadsheet main menu, as in the image bellow.

![New table](docs/imgs/new_table.png?raw=true "Screen")

After we select the option a popup window will ask you for the name of the new table.

![Table name popup](docs/imgs/tablename_popup.png?raw=true "Screen")

After the OK, a new tab will be generated with the format "Table_\<name you gave for the table\>".  
On the top of the tab spreadsheet we will configure which application the table bellongs to in the field \<Select an application\>.
If we click on this field, a dropdown box will be shown with the applications configured in the tab "Applications".

![Table header](docs/imgs/table_header.png?raw=true "Screen")

The fields \<Table singular label\> and \<Table plural label\> are the names of the table that will be used in the django admin interface.

The field \<Data access\> allow us to configure which type of access we would like to have on this table.
Check the available options in the image bellow.

![Table data access](docs/imgs/table_data_access.png?raw=true "Screen")

#### Add fields to the table

By default the table is added with a primary key set.

![Default fields](docs/imgs/default_fields.png?raw=true "Screen")

To add new fields you should use the option "Database application -> Add new field" in the Google spreadsheet main menu, as in the image bellow.

![New field](docs/imgs/new_field.png?raw=true "Screen")

A new row will appear in the spreadsheet, where you should configure your fields properties.

The details of fields configurations columns are explained in the table below.


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
| Field format                                  |  | The field will show "Auto generated" value or a dropdown list depending on the type of the table field.            |
| Possible answers                              | Empty or a dropdown list. | If the table field is a "Dropdown list" or a "Radio buttons list" a dropdown with the values from the spreadsheet "Answers" tab will be shown. |
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


#### Choices tab

The choices tab is used to configure the values of the Dropdown lists and Radio buttons lists fields.

![Answers tab](docs/imgs/answers-tab.png?raw=true "Screen")

The value in the "Answer identifier" column should be unique to each set of values, and should respect a python variable format.

![Answers spreadsheet](docs/imgs/answers-spreadsheet.png?raw=true "Screen")
