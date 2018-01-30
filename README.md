# TornadoPractice
Practice for using tornado

Used packages: `pymysql`, `tornado`  

**Structure of database**

`ws_account`:


| Field    | Type             | Null | Key | Default | Extra          |
|----------|------------------|------|-----|---------|----------------|
| uid      | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| username | varchar(25)      | NO   |     | NULL    |                |
| email    | varchar(50)      | NO   |     | NULL    |                |
| password | varchar(64)      | NO   |     | NULL    |                |
| reg_time | datetime         | YES  |     | NULL    |                |
| session  | varchar(64)      | YES  |     | NULL    |                |
`ws_record`:


| Field   | Type                | Null | Key | Default | Extra          |
|---------|---------------------|------|-----|---------|----------------|
| id      | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
| uid     | int(10) unsigned    | NO   |     | NULL    |                |
| content | text                | NO   |     | NULL    |                |
| date    | datetime            | YES  |     | NULL    |                |

## Version 1
Register and login function  
Online chat function supported by webscoket  
