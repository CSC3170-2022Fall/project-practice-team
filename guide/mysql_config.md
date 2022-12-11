#### Mysql Configuration

Before running /server/database/init/db_insert.py

You need to create the database in the first place by

```
$ mysql -u root -p
> type your password
$ CREATE DATABASE AGDP;
```

Also reconfig root password type is required due to contraint of the mysql python package we choose

```
$ mysql -u root -p
$ ALTER USER '<user_name>'@'localhost' IDENTIFIED WITH mysql_native_password BY '<password>';
```

