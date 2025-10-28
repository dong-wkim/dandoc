<div align="center">
  <a href="https://github.com/dong-wkim/dandoc">
    <img src="img/logo.png" alt="Logo" width="300" height="300">
  </a>

  <h3 align="center">Dandoc</h3>

  <p align="center">
    "Dandoc" is my (Dan`s) version of the popular file conversion method Pandoc. <br />
    <br />
    This repository converts simple plaintext (.txt) outline syntax to relational database table creation through network graph theory.
    <br />
    <br />
    <a href="https://github.com/dong-wkim/dandoc"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/dong-wkim/dandoc">View Demo</a>
    &middot;
    <a href="https://github.com/dong-wkim/dandoc/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/dong-wkim/dandoc/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>
<!-- network graph for conversions here -->

Through five forward and five backward conversion scripts, this python script allows conversion between txt, yml, json, sql, db, and csv files that are automatically updated for easy relational database creation and data entry through either flat spreadsheets or (upcoming) data forms. Example usage will be a systematic review and meta-analysis.  

## data

```python
formats = [
    `.txt`, 
    `.yaml`, 
    `json`,
    `sql`,
    `csv`,
    `db` 
]
```

## src

- [X] 1. `txt_yml.py`
- [X] 2. `yml_json.py`
- [X] 3. `json_sql.py`
- [ ] 4. `sql_db.py`
- [ ] 5. `db_csv.py`
- [ ] 10. `csv_db.py`
- [ ] 9. `db_sql.py`
- [ ] 8. `sql_json.py`
- [ ] 7. `json_yml.py`
- [ ] 6. `yml_txt.py`

### docs

`dandoc` formats = `txt`, `yml`, `json`
`pandoc` formats = `pdf`, `md`, `docx`

### data

`dandoc` formats = `sql`, `db`, `csv`
`pandoc` formats = `xlsx`

## conversion table

| no. | input | output |     src      | description |
| :-- | :---: | :----: | :----------: | :---  |
| 1   |  txt  |  yml  | `txt_yml.py`  |  |
| 2   |  yml |  json  | `yml_json.py` |  |
| 3   |  json |  sql   | `json_sql.py`  |  |
| 4   |  sql  |   db   |  `sql_db.py`   | Creation of database and tables in postgreSQL |
| 5   |   db  |  csv   |  `db_csv.py`   | Export of csv files from postgreSQL |
| 6   | yml  |  txt   | `yml_txt.py`  |  |
| 7   | json  |  yml  | `json_yml.py` |  |
| 8   |  sql  |  json  | `sql_json.py`  |  |
| 9   |  db   |  sql   | `db_sql.py`    |  |
| 10  |  csv  |   db   | `csv_db.py`    |  |


<!-- Comments/notes:

Better to use psql or python for converting between JSON and CSV files?

<<<<<<< HEAD
Full paths to scripts:
"E:\20-29 projects\.github\repositories\dandoc\src\txt_yml.py"
"E:\20-29 projects\.github\repositories\dandoc\src\yml_json.py"
"E:\20-29 projects\.github\repositories\dandoc\src\json_sql.py"
"E:\20-29 projects\.github\repositories\dandoc\src\sql_db.py"
"E:\20-29 projects\.github\repositories\dandoc\src\db_csv.py"

"E:\20-29 projects\.github\repositories\dandoc\src\csv_db.py"
"E:\20-29 projects\.github\repositories\dandoc\src\db_sql.py"
"E:\20-29 projects\.github\repositories\dandoc\src\sql_json.py"
"E:\20-29 projects\.github\repositories\dandoc\src\json_yml.py"
"E:\20-29 projects\.github\repositories\dandoc\src\yml_txt.py"

-->
=======
-->
>>>>>>> refs/remotes/origin/master
