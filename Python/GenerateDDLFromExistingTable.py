# includes
import pymssql
from datetime import datetime

# Declarations

path = "d:\\Users\\ffortunato\\Documents\\"

host = "devadw"
# user =
# password =
database = "ODS"
schema = "loan"
table = "LaunchLoanSummary"

current_date = datetime.today().strftime('%Y%m%d')
print(current_date)

header = """
/******************************************************************************
file:           @@@SchemaName@@@.@@@TableName@@@.sql
name:           @@@TableName@@@

purpose:        To attain enlightenment.

author:         Auto Generated
date:           @@@Date@@@
******************************************************************************/

Create Table @@@SchemaName@@@.@@@TableName@@@ (
\t ODS@@@TableName@@@Id bigint identity(1,1)
"""

footer = """\t,IssueId\t\t\tint not null
\t,ODSCreatedDate\t\tdatetime2 not null
\t,ODSCreatedBy\t\tvarchar(250) not null
\t,ODSCreatedProcess\tvarchar(250) not null
\t,ODSModifiedDate\tdatetime2 not null
\t,ODSModifiedBy\t\tvarchar(250) not null
\t,ODSModifiedProcess\tvarchar(250) not null
) On [Primary]

/******************************************************************************
\t\tchange history
*******************************************************************************
date\t\tauthor\t\t\tdescription
--------\t-------------\t---------------------------------------------------
@@@Date@@@\tAuto Generated\tinitial iteration

******************************************************************************/
"""

table_sql = """
    SELECT	COLUMN_NAME ColumnName
		,case DATA_TYPE
			when 'money' then DATA_TYPE \
			when 'decimal' then DATA_TYPE + '(' + cast(NUMERIC_PRECISION as varchar(10)) + ',' + cast(NUMERIC_SCALE as varchar(10)) + ')'\
		    when 'numeric' then DATA_TYPE + '(' + cast(NUMERIC_PRECISION as varchar(10)) + ',' + cast(NUMERIC_SCALE as varchar(10)) + ')'
			when 'varchar' then DATA_TYPE + '(' + cast(CHARACTER_MAXIMUM_LENGTH as varchar(10)) + ')'\
			when 'char' then DATA_TYPE + '(' + cast(CHARACTER_MAXIMUM_LENGTH as varchar(10)) + ')'\
			when 'nvarchar' then DATA_TYPE + '(' + cast(CHARACTER_MAXIMUM_LENGTH as varchar(10)) + ')'\
			else DATA_TYPE end DataType
		,Case IS_NULLABLE
		    when 'Yes' then 'NULL'
		    when 'No' then 'NOT NULL'
		    else 'NOT NULL'
		 end    Nullable
		,DATA_TYPE
		,CHARACTER_MAXIMUM_LENGTH
		,NUMERIC_PRECISION
		,NUMERIC_SCALE
		,DATETIME_PRECISION
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = '@@@TableName@@@'
AND TABLE_SCHEMA = '@@@SchemaName@@@'"""

view_sql = """
select schema_name(v.schema_id) as schema_name
        ,object_name(c.object_id) as view_name
        ,c.column_id
        ,c.name as column_name
        ,case  type_name(user_type_id)
			when 'money' then type_name(user_type_id) + '(' + cast(PRECISION as varchar(10)) + ',' + cast(SCALE as varchar(10)) + ')'
			when 'decimal' then type_name(user_type_id) + '(' + cast(PRECISION as varchar(10)) + ',' + cast(SCALE as varchar(10)) + ')'
			when 'numeric' then type_name(user_type_id) + '(' + cast(PRECISION as varchar(10)) + ',' + cast(SCALE as varchar(10)) + ')'
			when 'varchar' then type_name(user_type_id) + '(' + cast(max_length as varchar(10)) + ')'
			when 'char' then type_name(user_type_id) + '(' + cast(max_length as varchar(10)) + ')'
			when 'nvarchar' then  case max_length when -1 then  type_name(user_type_id) + '(max)'
					else type_name(user_type_id) + '(' + cast(max_length/2 as varchar(10)) + ')'
					end
			else type_name(user_type_id) end datatype
		,case IS_NULLABLE
			when 0 then 'not null'
			else 'null'
			end nullable
       ,type_name(user_type_id) as data_type
       ,c.max_length
       ,c.precision
from sys.columns c
join sys.views v 
     on v.object_id = c.object_id
where v.name = '@@ViewName@@@'
order by schema_name,
         view_name,
         column_id;
"""

# Database connections



print(__name__, ': Beginning Script')

try:
    db_conn = pymssql.connect(server=host, database=database)
    cursor = db_conn.cursor(as_dict=True)
except pymssql.Error as err:
    print("connection.connect_database :: Connection error.", err)

my_table_sql = table_sql.replace('@@@SchemaName@@@', schema)
my_table_sql = my_table_sql.replace('@@@TableName@@@', table)
my_header = header.replace('@@@Date@@@', current_date)
my_header = my_header.replace('@@@SchemaName@@@', schema)
my_header = my_header.replace('@@@TableName@@@', table)
my_footer = footer.replace('@@@Date@@@', current_date)

cursor.execute(my_table_sql)
rows = cursor.fetchall()

file_name = path + table + ".sql"
f = open(file_name, "a")  # Open and append file.
f.write(my_header)


for row in rows:
    line = "\t," + row['ColumnName'] + "\t" + row['DataType'] + "\t" + row['Nullable'] + "\n"
    f.write(line)

f.write(my_footer)
f.close()
