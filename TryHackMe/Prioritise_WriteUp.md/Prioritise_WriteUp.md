**Challenge Description**
Name: Prioritise
Category: Web / SQL Injection
Difficulty: Medium
Objective: Exploit a less common SQL injection technique to retrieve
the flag from the database.

#1. Initial Reconnaissance

The target application is a "To-Do List" manager. 
Upon visiting the site, we see a table of tasks with columns: 
*Title, Done, and Due Date.*

A 'feroxbuster' scan revealed a '/new' endpoint, but the primary interest was
the sorting functionality on the index page.
**Observed Parameter**

Interacting with the "Sort by" dropdown menu generates a GET request:
'http://10.82.175.152/?order=title'

The 'order' parameter is directly tied to the 'SQL ORDER BY' clause,
which is a common but often overlooked injection point.

#2. Vulnerability Analysis
Standard 'UNION'-based injection does not work in an 'ORDER BY' clause because 
the database expects a column name or a conditional expression, not a result set.

To confirm the injection, I tested Boolean-based inference using a 'CASE' statement:

    True Condition: /?order=(CASE WHEN (1=1) THEN title ELSE date END) (Items sorted by title)

    False Condition: /?order=(CASE WHEN (1=2) THEN title ELSE date END) (Items sorted by date)

Because the application returned different row orders for these requests, the injection was confirmed.

#3. Exploitation

**Automated Discovery with SQLMap**

Since manual extraction of a flag character-by-character is time-consuming, I used 'sqlmap' to automate 
the blind injection.

**Initial Scan:**

'''sqlmap -u "http://10.82.175.152/?order=title" --batch --dbms=sqlite --level 5 --risk 3'''

'sqlmap' identified two injection types:

    Boolean-based blind: Using CASE and JSON errors.

    Time-based blind: Using RANDOMBLOB to create heavy processing delays.

**Data Extraction**

With the injection confirmed as SQLite, I proceeded to enumerate the database schema.

1. Listing Tables:

'''sqlmap -u "http://10.82.175.152/?order=title" --batch --dbms=sqlite --tables'''

*Result:* Found two tables: todos and flag.

2. Dumping the Flag:

'''sqlmap -u "http://10.82.175.152/?order=title" --batch --dbms=sqlite -T flag --dump'''

#4. Conclusion
The challenge demonstrated **Blind SQL Injection in an ORDER BY** clause. Unlike typical injections in a 
'WHERE' clause, this requires observing the sorting order of the returned data or triggering **database** 
**errors** (500 Internal Server Errors) to leak information character by character.

Flag: flag{}

