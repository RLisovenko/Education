::page{title="Hands-on Lab: Using Views in MySQL using phpMyAdmin"}

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/images/IBM_logo.png" width="300" alt="cognitiveclass.ai logo"> <br>

**Estimated time needed: 20 minutes**

In this lab, you will learn about using views. In SQL, a view is an alternative way of representing data that exists in one or more tables. Just like a real table, it contains rows and columns. The fields in a view are fields from one or more real tables in the database. Though views can be queried like a table, views are dynamic; only the definition of the view is stored, not the data.

## Objectives
After completing this lab, you will be able to:

*   Create a View and show a selection of data for a given table
*   Update a View to combine two or more tables in meaningful ways
*   Drop a created View

### Software Used in this Lab

In this lab, you will use <a href="https://www.mysql.com/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDB0110ENSkillsNetwork24601058-2021-01-01" target="_blank">MySQL</a>. MySQL is a Relational Database Management System (RDBMS) designed to efficiently store, manipulate, and retrieve data.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0110EN-SkillsNetwork/labs/Lab%20-%20Create%20Tables%20and%20Load%20Data%20in%20MySQL%20using%20phpMyAdmin/images/mysql.png" width="100" height="100" alt="MySQL logo.">
<p></p>

To complete this lab you will utilize MySQL relational database service available as part of IBM Skills Network Labs (SN Labs) Cloud IDE. SN Labs is a virtual lab environment used in this course.

::page{title="Database Used in this Lab"}

The database used in this lab is a sample HR database. This HR database schema consists of five tables called `EMPLOYEES`, `JOB_HISTORY`, `JOBS`, `DEPARTMENTS`, and `LOCATIONS`. Each table has a few rows of sample data. The following diagram shows the tables for the HR database:

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Labs_Coursera_V5/labs/Lab%20-%20Create%20tables%20using%20SQL%20scripts%20and%20Load%20data%20into%20tables/images/Sample_1.PNG" alt="Sample HR Database tables with the five included databases.">

Follow the steps below to create the database and the tables.

1. Open the MySQL interface from Skills Network menu.
2. Create a new database and name it `HR`.
3. Load and execute the script shared in the link below to create the necessary tables.

   [HR_Database_Create_Tables_Script.sql](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/MySQL/week2/HR_Database_Create_Tables_Script.sql "HR_Database_Create_Tables_Script.sql")

4. Load all the tables with the data available in the CSV files shared below.

   [Departments.csv](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Labs_Coursera_V5/datasets/HR_Database/Departments.csv "Departments.csv")
   [Employees.csv](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/MySQL/week2/data/Employees_updated.csv "Employees.csv")
   [Jobs.csv](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Labs_Coursera_V5/datasets/HR_Database/Jobs.csv "Jobs.csv")
   [Locations.csv](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/Labs_Coursera_V5/datasets/HR_Database/Locations.csv "Locations.csv")
   [JobsHistory.csv](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/MySQL/week2/data/JobsHistory.csv "JobsHistory.csv")

> Note: Please refer to the instruction in the lab <a href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/v8/Create_tables_using_script_MySQL.md.html" target="_blank">\"Create and Load Tables using SQL Scripts\"</a> for instructions regarding loading scripts in MySQL.

::page{title="Task 1: Create a View"}

In this exercise, you will create a View and show a selection of data for a given table.

1.  Let\'s create a view called `EMPSALARY` to display salary along with some basic sensitive data of employees from the HR database. To create the `EMPSALARY` view from the `EMPLOYEES` table, Copy the code below and paste it to the textarea of the **SQL** page. Click `Go`.

```
CREATE VIEW EMPSALARY AS
SELECT EMP_ID, F_NAME, L_NAME, B_DATE, SEX, SALARY
FROM EMPLOYEES;
```

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/MySQL/week6/images/1.1.png" alt="SQL page with code in text area.">

<p></p>

2.  Using SELECT, query the `EMPSALARY` view to retrieve all the records. Use the following statement.

```
SELECT * FROM EMPSALARY;
```

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/MySQL/week6/images/1.2.png" alt="SQL page with query results.">

::page{title="Task 2: Update a View"}

In this exercise, you will update a View to combine two or more tables in meaningful ways.

Assume that the `EMPSALARY` view we created in Task 1 doesn\'t contain enough salary information, such as max/min salary and the job title of the employees. For this, we need to get information from other tables in the database. You need all columns from `EMPLOYEES` table used above, except for `SALARY`. You also need the columns `JOB_TITLE`, `MIN_SALARY`, `MAX_SALARY` of the `JOBS` table.
The command to be used is as follows:

```
CREATE OR REPLACE VIEW EMPSALARY AS
SELECT EMP_ID, F_NAME, L_NAME, B_DATE, SEX, JOB_TITLE,
MIN_SALARY, MAX_SALARY
FROM EMPLOYEES, JOBS
WHERE EMPLOYEES.JOB_ID = JOBS.JOB_IDENT;
```

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/MySQL/week6/images/2.1.png" alt="SQL page with code from above.">

<p></p>

> **NOTE:** The technique used here to combine data from two tables is called implicit inner join. You will learn more about joins later on. For now, just assume you are combining the data of two different tables, `EMPLOYEES` and `JOBS` by connecting their respective columns `JOB_ID` and `JOB_IDENT`, since both the columns contain common unique data. You can have a look at the database description, shared at the beginning of the lab, to verify this.

<p></p>

2.  Using `SELECT`, query the updated `EMPSALARY` view to retrieve all the records. Copy the code below and paste it to the textarea of the **SQL** page. Click `Go`.

```
SELECT * FROM EMPSALARY;
```

![SQL page with query results.](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/MySQL/week6/images/2.2.png)

::page{title="Task 3: Drop a View"}

In this exercise, you will drop the created View `EMPSALARY`.
Use the code below.

```
DROP VIEW EMPSALARY;
```
<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/MySQL/week6/images/3.1.png" alt="SQL page with recent code.">

<p></p>

Using SELECT, you can verify whether the `EMPSALARY` view has been deleted or not. Copy the code below and paste it to the textarea of the `SQL` page. Click `Go`.

```
SELECT * FROM EMPSALARY;
```

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/MySQL/week6/images/3.2.png" alt="SQL page with new code.">

::page{title="Practice Problems"}

Try to solve the following practice problems based on your learning in this lab.

1. Create a view "EMP_DEPT" which has the following information.
`EMP_ID`, `FNAME`, `LNAME` and `DEP_ID` from `EMPLOYEES` table

<details>
<summary>Click here for the solution</summary>

```
CREATE VIEW EMP_DEPT AS
SELECT EMP_ID, F_NAME, L_NAME, DEP_ID
FROM EMPLOYEES;
```
</details>

2. Modify "EMP_DEPT" such that it displays Department names instead of Department IDs. For this, we need to combine information from `EMPLOYEES` and `DEPARTMENTS` as follows.

`EMP_ID`, `FNAME`, `LNAME` from `EMPLOYEES` table and
`DEP_NAME` from `DEPARTMENTS` table, combined over the columns `DEP_ID` and `DEPT_ID_DEP`.

<details>
<summary>Click here for the solution</summary>

```
CREATE OR REPLACE VIEW EMP_DEPT AS
SELECT EMP_ID, F_NAME, L_NAME, DEP_NAME
FROM EMPLOYEES, DEPARTMENTS
WHERE EMPLOYEES.DEP_ID = DEPARTMENTS.DEPT_ID_DEP;
```
</details>

3. Drop the view "EPM_DEPT".

<details>
<summary>Click here for the solution</summary>

```
DROP VIEW EMP_DEPT
```
</details>

::page{title="Conclusion"}

Congratulations on completing this lab. You now have hands-on knowledge of how to use Views in SQL.

You have now learned how to:

* Create a new View as per the requirement

* Modify a view to include data from multiple tables in the data set

* Drop a view

### Author(s)

[Lakshmi Holla](https://www.linkedin.com/in/lakshmi-holla-b39062149/) 

[Malika Singla](https://www.linkedin.com/in/malika-goyal-04798622/)

### Additional Contributor(s)

[Abhishek Gagneja](https://www.linkedin.com/in/abhishek-gagneja-23051987/)

## <h3 align="center"> © IBM Corporation 2023. All rights reserved. <h3/>

<!-- ### Changelog

| Date       | Version | Changed by | Change Description                   |
| ---------- | ------- | ---------- | ------------------------------------ |
| 2023-10-13 | 0.5 | Steve Hord | QA pass |
| 2023-09-13 | 0.4 | Misty Taylor | ID Check|
| 2023-09-10 | 0.3 | Abhishek Gagneja | Updated instructions|
| 2023-05-04        | 0.2     | Rahul Jaideep | Updated Markdown file |
| 2021-11-01 | 0.1  | Lakshmi Holla, Malika Singla | Initial Version       | --!>



