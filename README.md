# Database Framework project
Here is the gouge on the markdown tags to improve this README:  [PyCharm Markdown Reference](https://www.jetbrains.com/help/pycharm/markdown.html)
<br>
<br>
This is a sample Python module for performing database access. Currently, it is tied to MS-SQL since that appears to be the Database of choice. There are also some implicit expectations that Pandas/DFs and SQLite will be used for either out of database transformation or some local optimizations.
## Description
Three classes: DB, ETL and QueryEngine. If greater functionality is needed it is assumed the classes will be extended.

| Class       | High Level Description                                                                                                                        | 
|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| DB (base)   | base class, does connections and standard operations that are expected from a database. Gets connection information from $HOME/.mssql_db.conf |
| ETL         | performs the typical Extract, Transform, Load of data on underlying database                                                                  | 
| QueryEngine | smart query class, can use 'standard' and jinja style template strings for quering the underlying database                                    |

## Getting Started
Take a look at main.py and start running from there

### Dependencies
1. This project started with Python 3.9+. It is assumed to be upward compatible with should be used with this, yymv with other versions
2. **requirements.txt** identifies python dependencies
3. _pytest_ is the testing framework.
### Installing
```
$ pip install -r requirements.txt
```
* DB connections are stored in ~/.mssql_db.conf
```
# NOTE: this file is only readable by owner, should get from VAULT ...

$ cat  ~/.mssql_db.conf   
[dev]
host        = waveland.database.windows.net
port        = 8675309
user        = G3n3ra1Ney1and
password    = S3Cru1esB1G
dbname      = sheffieldAvenue
```
* Config tags of [ dev | qa | uat | prod ] are assumed to delimit environments
* How/where to download your program
* Any modifications needed to be made to files/folders
### Executing the program
* How to run the program
* Step-by-step bullets
## Help
Any advice for common problems or issues.
```
sigh, it is expected to fail **loud** when there are issues
```
## Authors
yeah, you know how to get me ...

## Version History

## Data resources (for sample data)
* [NYSE tick data](https://datahub.io/awesome/stock-market-data#nyse-and-other-listings)
* [Economic data](https://www.aeaweb.org/resources/data)
* [Registry of Open Data on AWS](https://registry.opendata.aws/)
* [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php)
## License
This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments
The internet is awesome for collaboration. Software is a collaborative effort, without collaboration we'd be years behind.

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PyCharm Markdown Reference](https://www.jetbrains.com/help/pycharm/markdown.html)
