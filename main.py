# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql_query(
	"""SELECT e.firstName, e.lastName
	   FROM employees AS e
	   JOIN offices AS o ON e.officeCode = o.officeCode
	   WHERE o.city = 'Boston'
	   ORDER BY e.firstName, e.lastName""",
	conn,
)

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql_query(
	"""SELECT o.officeCode, o.city
	   FROM offices AS o
	   LEFT JOIN employees AS e ON o.officeCode = e.officeCode
	   WHERE e.employeeNumber IS NULL""",
	conn,
)

# STEP 3
# Replace None with your code
df_employee = pd.read_sql_query(
	"""SELECT e.firstName, e.lastName, o.city, o.state
	   FROM employees AS e
	   LEFT JOIN offices AS o ON e.officeCode = o.officeCode
	   ORDER BY e.firstName, e.lastName""",
	conn,
)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql_query(
	"""SELECT c.contactFirstName, c.contactLastName, c.phone,
			  c.salesRepEmployeeNumber
	   FROM customers AS c
	   LEFT JOIN orders AS ord ON c.customerNumber = ord.customerNumber
	   WHERE ord.orderNumber IS NULL
	   ORDER BY c.contactLastName""",
	conn,
)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql_query(
	"""SELECT c.contactFirstName, c.contactLastName,
			  p.amount, p.paymentDate
	   FROM payments AS p
	   JOIN customers AS c ON p.customerNumber = c.customerNumber
	   ORDER BY CAST(p.amount AS REAL) DESC""",
	conn,
)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql_query(
		"""SELECT e.employeeNumber, e.firstName, e.lastName,
							COUNT(c.customerNumber) AS numcustomers
			 FROM employees AS e
			 JOIN customers AS c
				 ON e.employeeNumber = c.salesRepEmployeeNumber
			 GROUP BY e.employeeNumber, e.firstName, e.lastName
			 HAVING AVG(CAST(c.creditLimit AS REAL)) > 90000
			 ORDER BY numcustomers DESC""",
		conn,
)

# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql_query(
	"""SELECT p.productName,
			  COUNT(od.orderNumber) AS numorders,
			  SUM(od.quantityOrdered) AS totalunits
	   FROM products AS p
	   JOIN orderdetails AS od ON p.productCode = od.productCode
	   GROUP BY p.productCode, p.productName
	   ORDER BY totalunits DESC""",
	conn,
)

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql_query(
	"""SELECT p.productName, p.productCode,
			  COUNT(DISTINCT ord.customerNumber) AS numpurchasers
	   FROM products AS p
	   JOIN orderdetails AS od ON p.productCode = od.productCode
	   JOIN orders AS ord ON od.orderNumber = ord.orderNumber
	   GROUP BY p.productCode, p.productName
	   ORDER BY numpurchasers DESC""",
	conn,
)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql_query(
		"""SELECT o.officeCode, o.city,
							COUNT(DISTINCT c.customerNumber) AS n_customers
			 FROM offices AS o
			 JOIN employees AS e ON o.officeCode = e.officeCode
			 JOIN customers AS c
				 ON e.employeeNumber = c.salesRepEmployeeNumber
			 GROUP BY o.officeCode, o.city
			 ORDER BY o.officeCode""",
		conn,
)

# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql_query(
		"""WITH underperforming_products AS (
					 SELECT od.productCode
					 FROM orderdetails AS od
					 JOIN orders AS ord ON od.orderNumber = ord.orderNumber
					 GROUP BY od.productCode
					 HAVING COUNT(DISTINCT ord.customerNumber) < 20
			 )
			 SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName,
							o.city, o.officeCode
			 FROM employees AS e
			 JOIN customers AS c
				 ON e.employeeNumber = c.salesRepEmployeeNumber
			 JOIN orders AS ord ON c.customerNumber = ord.customerNumber
			 JOIN orderdetails AS od ON ord.orderNumber = od.orderNumber
			 JOIN underperforming_products AS up
				 ON od.productCode = up.productCode
			 JOIN offices AS o ON e.officeCode = o.officeCode
			 ORDER BY e.lastName, e.firstName""",
		conn,
)

conn.close()