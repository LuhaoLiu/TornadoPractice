# TornadoPractice
Practice for using tornado.  
Online multiplayer chat website with authentication function.

Used packages: `pymysql`, `tornado`  

**Structure of database**

* `ws_account`:


| Field    | Type             | Null | Key | Default | Extra          |
|----------|------------------|------|-----|---------|----------------|
| uid      | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| username | varchar(25)      | NO   | UNI | NULL    |                |
| email    | varchar(50)      | NO   | UNI | NULL    |                |
| password | varchar(64)      | NO   |     | NULL    |                |
| reg_time | datetime         | NO   |     | NULL    |                |
| session  | varchar(64)      | YES  |     | NULL    |                |

* `ws_record`:


| Field   | Type                | Null | Key | Default | Extra          |
|---------|---------------------|------|-----|---------|----------------|
| id      | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
| uid     | int(10) unsigned    | NO   | MUL | NULL    |                |
| content | text                | NO   |     | NULL    |                |
| date    | datetime            | YES  |     | NULL    |                |

## Change Log

### Version 1
Register and login function  
Online chat function supported by webscoket  

#### Version 1.0.1
Save server information and mysql information in the json file 
`/info/server.json` and `/info/mysql.json` 
instead of saving in the source code.