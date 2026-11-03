# Insurance Claims Data Warehouse with GenAI

## Complete Technical Viva Questions and Answers

This guide is tailored to the project built for the Cloud Data Engineer
hackathon. Answers describe the actual implementation. The dataset is
synthetic; PySpark runs locally in Ubuntu WSL2; the Gold Parquet
datasets are stored in S3 and queried through Athena; Glue tables were
registered manually through Athena DDL; Ollama summarizes claim notes
but does not make claim or fraud decisions.

## How to use this guide

-   Understand the answer and practise explaining it in your own words.
-   For project-specific questions, explain what you actually
    implemented.
-   Do not claim that an optional or future feature is already
    implemented.

------------------------------------------------------------------------

# 1. Project Overview and Architecture

### 1. What is your project?

**Answer:** My project is an Insurance Claims Data Warehouse with
Generative AI. It ingests five insurance CSV datasets, stores structured
data in MySQL, processes data using PySpark, organizes it into Bronze,
Silver, and Gold layers, stores datasets in Amazon S3, and uses AWS Glue
Data Catalog and Athena for analytics. I also integrated Ollama Cloud to
summarize claim notes and built a Streamlit dashboard.

### 2. What problem does your project solve?

**Answer:** Insurance information is spread across policies,
beneficiaries, claims, fraud investigations, and claim notes. It can be
difficult to validate and analyze these datasets separately. My project
brings the data into a structured pipeline, checks data quality, creates
analytics-ready datasets, and presents business insights through SQL
queries and a dashboard.

### 3. What is a data warehouse?

**Answer:** A data warehouse is a system that stores integrated,
structured, historical data for reporting and analysis. It is optimized
for analytical queries rather than day-to-day transaction processing.

### 4. What is a data lake?

**Answer:** A data lake stores data in its original or processed form,
often in object storage such as Amazon S3. It can hold structured,
semi-structured, and unstructured data.

### 5. What is the difference between a data lake and a data warehouse?

**Answer:** A data lake can store raw files in many formats and schemas.
A traditional data warehouse stores data in a more structured and
governed format optimized for analytics. In this project, S3 provides
data lake storage and Athena provides SQL analytics over the Gold
Parquet files.

### 6. Explain your project architecture.

**Answer:** The source CSV files are explored and loaded into MySQL
using Python. PySpark reads the datasets, cleans and transforms them,
and creates Silver and Gold Parquet outputs. Raw, processed, and Gold
datasets are stored in S3 Bronze, Silver, and Gold locations. Gold
tables are registered in Glue Data Catalog and queried using Athena.
Streamlit displays analytics and claim details, while Ollama Cloud
generates summaries from claim notes.

### 7. What is ETL?

**Answer:** ETL means Extract, Transform, Load. Extract reads data from
a source, Transform cleans and reshapes it, and Load writes it to a
destination. In this project, Python and PySpark perform ingestion and
transformation, while MySQL and S3 are storage destinations.

### 8. What is ELT? How is it different from ETL?

**Answer:** ELT means Extract, Load, Transform. Data is loaded into the
target platform first and transformed there. ETL transforms before
loading into the target. Modern cloud platforms often use ELT because
scalable storage and compute can process data after ingestion.

### 9. What is a batch processing pipeline?

**Answer:** Batch processing handles a group of records together at
scheduled or manually initiated intervals. This project is
batch-oriented because it processes CSV datasets as a set rather than
continuously processing each new record.

### 10. Is your pipeline real-time or batch?

**Answer:** It is a batch-processing pipeline. The source is a set of
CSV files and the PySpark scripts process those files when executed. It
does not currently use streaming services such as Kinesis.

### 11. What is a data pipeline?

**Answer:** A data pipeline is a sequence of steps that moves data from
sources through ingestion, validation, transformation, storage, and
analytics.

### 12. What are the main outputs?

**Answer:** Five MySQL tables, cleaned Silver Parquet datasets, three
Gold Parquet datasets, three Athena tables, a Streamlit dashboard, and
AI-generated summaries of claim notes.

### 13. How many records are in your dataset?

**Answer:** The five synthetic CSV datasets contain 590 source records:
50 policies, 100 beneficiaries, 100 claims, 102 fraud investigation
records, and 238 claim notes.

### 14. Why did you choose the insurance domain?

**Answer:** Insurance data has meaningful relationships between
policies, beneficiaries, claims, investigations, and notes. It provides
opportunities to demonstrate relational database design, data quality
checks, joins, aggregations, and text summarization.

### 15. What are the limitations of your project?

**Answer:** The dataset is synthetic and relatively small. The pipeline
is batch-oriented and run manually rather than through a production
orchestrator. Glue tables are registered manually. AI output is advisory
and requires human review. A production version would need stronger
access controls, monitoring, orchestration, testing, and larger-scale
validation.

------------------------------------------------------------------------

# 2. Python and Data Ingestion

### 16. Why did you use Python?

**Answer:** Python is easy to read and has libraries for data
processing, database connectivity, APIs, and application development. I
used it for data exploration, schema reporting, loading CSV files into
MySQL, calling Ollama Cloud, and building the Streamlit application.

### 17. What is Pandas?

**Answer:** Pandas is a Python library for tabular data analysis. Its
main data structures are Series and DataFrame. I used it to read CSV
files, inspect columns, count missing values, check duplicates, and
prepare data for MySQL loading.

### 18. What is a DataFrame?

**Answer:** A DataFrame is a two-dimensional labelled table with rows
and columns. Pandas and PySpark both provide DataFrame APIs, but their
execution models differ.

### 19. How do you read a CSV using Pandas?

**Answer:**

``` python
import pandas as pd
df = pd.read_csv("data/raw/claims.csv.csv")
print(df.head())
print(df.shape)
print(df.info())
```

`read_csv()` loads the file, `head()` displays sample rows, `shape`
gives row and column counts, and `info()` displays column types and
non-null counts.

### 20. How did you identify missing values?

**Answer:** I used `isnull()` and `sum()` to count missing values by
column.

``` python
df.isnull().sum()
```

### 21. How do you identify duplicates?

**Answer:** I used `duplicated()` to identify duplicate rows.

``` python
df.duplicated().sum()
```

For a particular key: `df["id"].duplicated().sum()`.

### 22. Difference between `dropna()` and `fillna()`?

**Answer:** `dropna()` removes rows or columns containing missing values
according to its options. `fillna()` replaces missing values. The choice
depends on business meaning; missing data should not automatically be
deleted or replaced.

### 23. Why not replace missing claim amounts with zero?

**Answer:** A missing amount does not necessarily mean the claim amount
is zero. Replacing it with zero changes the meaning and can distort
totals and averages. I preserve or separately count missing amounts
unless a justified business rule exists.

### 24. What is schema validation?

**Answer:** It checks whether a dataset has expected columns, data
types, and structure before processing. It prevents unexpected source
changes from silently corrupting downstream processing.

### 25. Why generate a schema report?

**Answer:** It documents each dataset's row count, column names, data
types, missing values, and duplicate checks. It helps understand the
source before loading and transformation.

### 26. What is a Python virtual environment?

**Answer:** It isolates a project's Python packages from other projects,
reducing dependency conflicts and making the environment easier to
reproduce.

### 27. Why do you have `.venv` and `.venv-linux`?

**Answer:** `.venv` is the Windows environment for Python scripts, MySQL
loading, Ollama, and Streamlit. `.venv-linux` is the Ubuntu environment
for PySpark. They are separate because Windows and Linux use different
executables and installed packages.

### 28. What is `requirements.txt`?

**Answer:** It lists the Python packages required by the project.
Dependencies can be installed with `pip install -r requirements.txt`.

### 29. What is an exception in Python?

**Answer:** An exception is an error that occurs while a program is
running. `try` and `except` blocks handle expected failures such as a
missing file or database connection error.

### 30. Why use `pathlib`?

**Answer:** `pathlib` provides an object-oriented way to build and work
with file paths and is generally more portable than manually
concatenating path strings.

### 31. Why use `getpass` in the MySQL loader?

**Answer:** It prompts for a password without displaying the typed
characters. This is safer than hardcoding the password or displaying it
in the terminal.

### 32. Why use SQLAlchemy and PyMySQL?

**Answer:** SQLAlchemy provides database connection and SQL execution
tools. PyMySQL is the driver that lets Python communicate with MySQL.
Together they support loading the CSV data into MySQL.

### 33. Why map source `type` to MySQL `policy_type`?

**Answer:** The source policies CSV uses `type`, while the MySQL table
uses the clearer name `policy_type`. The loader maps the source column
to the database column during ingestion.

### 34. How do you prevent duplicate loading?

**Answer:** The loader checks whether target tables already contain
records and stops rather than inserting the same data again. A
production pipeline could use batch IDs, staging tables, upserts, or
idempotent load logic.

### 35. What is idempotency?

**Answer:** An operation is idempotent when repeating it with the same
input produces the same final state without unintended duplicate
effects. It is important because pipeline jobs may need retries.

### 36. What happens if a source CSV is missing?

**Answer:** The pipeline should stop with a clear error instead of
silently processing incomplete data. A robust implementation validates
file existence and expected columns before loading.

------------------------------------------------------------------------

# 3. SQL and MySQL

### 37. What is MySQL?

**Answer:** MySQL is a relational database management system. It stores
data in tables and supports SQL queries, constraints, indexes, and
transactions.

### 38. Why did you use MySQL?

**Answer:** The insurance datasets have clear relationships. MySQL lets
me represent and validate them using primary and foreign keys and
analyze the structured data with SQL.

### 39. What is a database?

**Answer:** An organized collection of data that can be stored,
retrieved, updated, and managed.

### 40. What is a table?

**Answer:** A table stores data in rows and columns. Each row is a
record and each column is an attribute.

### 41. What is a primary key?

**Answer:** A primary key uniquely identifies each row. It cannot
contain duplicate values or NULL.

### 42. What is a foreign key?

**Answer:** A foreign key is a column or set of columns that references
a key in another table. It helps maintain referential integrity.

### 43. Explain your database relationships.

**Answer:** `policies.id` is referenced by `beneficiaries.policy_id` and
`claims.policy_id`. `claims.id` is referenced by `claims_fraud.claim_id`
and `claims_notes.claim_id`. These connect policies to beneficiaries and
claims, and claims to investigations and notes.

### 44. What is referential integrity?

**Answer:** It ensures that a foreign key references an existing parent
record, unless NULL is allowed by the schema. It prevents invalid
relationships.

### 45. What is normalization?

**Answer:** Normalization organizes relational data to reduce
unnecessary duplication and update anomalies by separating entities into
related tables.

### 46. What is denormalization?

**Answer:** Denormalization combines or duplicates data to make
analytical queries faster or simpler. Data warehouses often use
denormalized structures for reporting.

### 47. Difference between OLTP and OLAP?

**Answer:** OLTP handles frequent operational transactions. OLAP is
optimized for analytical queries over larger amounts of data. MySQL
stores the project's relational data, while Gold datasets and Athena
support analytics.

### 48. What are DDL, DML, DQL, and DCL?

**Answer:** DDL defines database objects (`CREATE`, `ALTER`, `DROP`);
DML changes data (`INSERT`, `UPDATE`, `DELETE`); DQL retrieves data
(`SELECT`); DCL controls permissions (`GRANT`, `REVOKE`).

### 49. What is a JOIN?

**Answer:** A JOIN combines rows from two or more tables using related
columns.

### 50. Difference between INNER JOIN and LEFT JOIN?

**Answer:** INNER JOIN returns matching rows in both tables. LEFT JOIN
returns every row from the left table and matching rows from the right;
unmatched right-side columns are NULL.

### 51. Why use LEFT JOIN for policy analysis?

**Answer:** It keeps all policies even if a policy has no claims. This
makes the analysis more complete than an INNER JOIN when reporting on
every policy.

### 52. What is GROUP BY?

**Answer:** It groups rows with the same values so aggregate functions
can calculate metrics for each group.

``` sql
SELECT status, COUNT(*)
FROM claims
GROUP BY status;
```

### 53. Difference between WHERE and HAVING?

**Answer:** WHERE filters rows before grouping. HAVING filters groups
after aggregation.

### 54. What are aggregate functions?

**Answer:** Functions that calculate results from multiple rows, such as
`COUNT()`, `SUM()`, `AVG()`, `MIN()`, and `MAX()`.

### 55. What is NULL?

**Answer:** NULL represents missing or unknown information. It is not
the same as zero or an empty string. Use `IS NULL` or `IS NOT NULL` to
test it.

### 56. Difference between `COUNT(column)` and `COUNT(*)`?

**Answer:** `COUNT(*)` counts rows. `COUNT(column)` counts only rows
where that column is not NULL.

### 57. What is an index?

**Answer:** An index is a data structure that can speed up retrieval for
selected queries. It uses storage and can slow some writes, so it should
be chosen based on query patterns.

### 58. What is a transaction?

**Answer:** A transaction is a group of database operations treated as
one unit. ACID means Atomicity, Consistency, Isolation, and Durability.

### 59. Difference between DELETE, TRUNCATE, and DROP?

**Answer:** DELETE removes selected rows and can use WHERE. TRUNCATE
removes all rows. DROP removes the table definition and its data. Their
transaction and foreign-key behavior can differ by database engine.

### 60. How did you validate MySQL tables?

**Answer:** I used the existing `mysql/03_validate_tables.sql` file. It
lists tables, counts records, and includes data-quality and analytical
queries. Expected counts are 50 policies, 100 beneficiaries, 100 claims,
102 fraud records, and 238 notes.

### 61. What is an orphan record?

**Answer:** A record whose foreign key does not match an existing parent
record. For example, a claim whose `policy_id` does not exist in
`policies`.

### 62. What were your orphan check results?

**Answer:** The validation checks found zero orphan claims and zero
orphan fraud records.

### 63. Query to find missing claim amounts?

**Answer:**

``` sql
SELECT COUNT(*) AS missing_amounts
FROM claims
WHERE amount IS NULL;
```

The project data contains 73 missing claim amounts.

### 64. Query to count claims by status?

**Answer:**

``` sql
SELECT status, COUNT(*) AS total_claims
FROM claims
GROUP BY status
ORDER BY total_claims DESC;
```

### 65. Query to find claims with policy type?

**Answer:**

``` sql
SELECT c.id AS claim_id, c.status, c.amount, p.policy_type
FROM claims c
JOIN policies p ON c.policy_id = p.id;
```

### 66. How would you find policies with no claims?

**Answer:**

``` sql
SELECT p.id, p.policy_number
FROM policies p
LEFT JOIN claims c ON p.id = c.policy_id
WHERE c.id IS NULL;
```

### 67. How do you calculate average non-NULL claim amount?

**Answer:**

``` sql
SELECT AVG(amount) AS average_claim_amount
FROM claims;
```

`AVG()` ignores NULL values.

### 68. What is a subquery?

**Answer:** A query nested inside another SQL statement. It can filter,
calculate, or compare results.

------------------------------------------------------------------------

# 4. Data Warehousing and Medallion Architecture

### 69. What is a fact table?

**Answer:** A fact table stores measurable business events, such as
claims, claim amounts, or transactions. It typically contains foreign
keys to dimensions.

### 70. What is a dimension table?

**Answer:** A dimension table stores descriptive attributes used to
analyze facts, such as policy type, customer category, or date.

### 71. What is a star schema?

**Answer:** A star schema has a central fact table connected to
denormalized dimension tables. It is commonly used in analytical data
warehouses.

### 72. What is a snowflake schema?

**Answer:** A snowflake schema is a dimensional model in which
dimensions are further normalized into related tables.

### 73. Did you implement a star schema?

**Answer:** The current implementation uses relational source tables in
MySQL and three aggregated Gold datasets. It does not implement a
complete dimensional star schema with separately designed fact and
dimension tables. That could be a future improvement.

### 74. What is a surrogate key?

**Answer:** An artificial key, often an integer, used to identify a
record independently of its business attributes.

### 75. What is a natural key?

**Answer:** A key with business meaning, such as a policy number.

### 76. What is a slowly changing dimension?

**Answer:** A method for managing changes to dimension attributes over
time. Type 1 overwrites old values; Type 2 creates a new version to
preserve history.

### 77. What is Medallion Architecture?

**Answer:** A layered data architecture with Bronze, Silver, and Gold
layers. Bronze stores raw data, Silver stores cleaned and standardized
data, and Gold stores aggregated or business-ready data.

### 78. Why separate Bronze, Silver, and Gold?

**Answer:** It preserves source data, makes cleaning traceable, and
provides stable datasets for analytics. It also makes debugging and
reprocessing easier.

### 79. Should raw data be overwritten?

**Answer:** Generally, raw source data should be preserved.
Transformations should create new outputs in later layers so the
original source can be revisited.

### 80. What is data lineage?

**Answer:** Data lineage describes where data came from and how it
changed through a pipeline. It helps with debugging, auditing, and
understanding analytical results.

### 81. What is data quality?

**Answer:** Data quality describes whether data is fit for its intended
use. Common dimensions include accuracy, completeness, consistency,
validity, uniqueness, and timeliness.

### 82. What is schema evolution?

**Answer:** Handling changes to a dataset's structure over time, such as
new columns, removed columns, or changed data types.

------------------------------------------------------------------------

# 5. PySpark and Big Data

### 83. What is Apache Spark?

**Answer:** Apache Spark is a data processing engine designed for
large-scale data processing and analytics.

### 84. What is PySpark?

**Answer:** PySpark is the Python API for Apache Spark. It lets Python
developers use Spark DataFrames, SQL, and distributed processing
features.

### 85. Why use PySpark instead of only Pandas?

**Answer:** Pandas is convenient for small datasets and local analysis.
PySpark is designed to scale to larger datasets using distributed
processing. I used PySpark to demonstrate a scalable transformation
approach even though this demonstration dataset is small.

### 86. What is a SparkSession?

**Answer:** The main entry point for Spark SQL and DataFrame
functionality.

``` python
from pyspark.sql import SparkSession
spark = (SparkSession.builder
         .appName("InsuranceClaims")
         .master("local[*]")
         .getOrCreate())
```

### 87. What does `local[*]` mean?

**Answer:** It tells Spark to run locally and use the available logical
CPU cores. It does not create a multi-machine cluster.

### 88. What is a Spark DataFrame?

**Answer:** A distributed collection of data organized into named
columns. It supports transformations and actions.

### 89. Difference between Pandas and Spark DataFrames?

**Answer:** A Pandas DataFrame is generally processed in a single Python
process and memory space. A Spark DataFrame is processed by Spark's
execution engine and can be distributed across partitions and machines.

### 90. What is a transformation in Spark?

**Answer:** A transformation creates a new DataFrame from an existing
one. Examples include `select()`, `filter()`, `withColumn()`, `join()`,
and `groupBy()`.

### 91. What is an action in Spark?

**Answer:** An action triggers execution and returns a result or writes
output. Examples include `show()`, `count()`, `collect()`, and `write`.

### 92. What is lazy evaluation?

**Answer:** Spark generally records transformations as a logical
execution plan and delays execution until an action is called. This
allows Spark to optimize the plan.

### 93. What is a partition?

**Answer:** A partition is a logical division of a dataset that Spark
can process as a unit. Multiple partitions allow work to be performed in
parallel.

### 94. What is a shuffle?

**Answer:** A shuffle redistributes data across partitions, often
between executors. Large joins and groupBy operations can require
shuffles, which may be expensive.

### 95. Difference between `repartition()` and `coalesce()`?

**Answer:** `repartition()` can increase or decrease partitions and
generally causes a shuffle. `coalesce()` is commonly used to reduce
partitions with less data movement when possible.

### 96. What is a Spark schema?

**Answer:** A schema defines DataFrame column names and data types.
Explicit schemas can improve reliability and avoid unwanted type
inference.

### 97. Difference between `select()` and `withColumn()`?

**Answer:** `select()` chooses or derives columns for a new DataFrame.
`withColumn()` adds a new column or replaces an existing one.

### 98. What is `groupBy()` used for?

**Answer:** It groups records by one or more columns so aggregate
functions can calculate counts, sums, averages, and other metrics.

### 99. How did you create claim summary?

**Answer:** I grouped the claims DataFrame by status and calculated
total claims, total claim amount, average claim amount, and missing
amount count. I wrote the resulting DataFrame to the Gold
`claim_summary` Parquet folder.

### 100. How did you create policy analysis?

**Answer:** I joined policies with claims using policy ID, grouped by
policy type, and calculated claim counts, total claim amounts, and
average claim amounts.

### 101. Why use LEFT JOIN in policy analysis?

**Answer:** It keeps policies even when they do not have matching
claims. This avoids dropping policies without claims from the analysis.

### 102. How did you create fraud analysis?

**Answer:** I grouped fraud investigation records by fraud type and
outcome and counted investigations in each group.

### 103. How do you handle NULL values in Spark?

**Answer:** Spark provides `isNull()`, `isNotNull()`, `fillna()`, and
`dropna()`. The correct method depends on the meaning of the missing
data and transformation requirements.

### 104. What is Parquet?

**Answer:** A columnar storage format designed for analytical workloads.
It supports compression and efficient reading of selected columns.

### 105. Why Parquet instead of CSV?

**Answer:** Parquet is efficient for analytics because it stores data by
column and supports column pruning and compression. CSV is
human-readable and convenient for source exchange but less efficient for
repeated analytical processing.

### 106. What is predicate pushdown?

**Answer:** Applying filters as close to the data source as possible so
unnecessary data does not need to be read. Supported file formats and
query engines can use it to reduce I/O.

### 107. What is the Catalyst optimizer?

**Answer:** Spark SQL's query optimizer. It analyzes and optimizes
logical plans before execution.

### 108. What is the Tungsten execution engine?

**Answer:** Tungsten refers to Spark execution improvements for memory
management and CPU efficiency, including optimized binary processing and
code generation.

### 109. Why use Ubuntu WSL2 for Spark?

**Answer:** The initial Windows Spark run encountered Hadoop native
binary configuration errors. I used Ubuntu WSL2 with Java 17 and a
separate Linux virtual environment, where the PySpark scripts ran
successfully.

### 110. Did you create a Hadoop cluster?

**Answer:** No. The project uses Spark in local mode with `local[*]`. It
does not require a separate Hadoop cluster or HDFS installation for this
workload.

### 111. Is Spark running across multiple machines?

**Answer:** No. It runs locally using the available CPU cores. The code
uses Spark's DataFrame processing model, but the current deployment is
not a multi-node cluster.

### 112. What would you change for a very large dataset?

**Answer:** I would deploy Spark on an appropriately sized distributed
or managed cluster, tune partitions, use suitable file sizes, monitor
shuffles and memory, optimize joins, and introduce orchestration and
monitoring.

------------------------------------------------------------------------

# 6. AWS, S3, Glue, and Athena

### 113. What is AWS?

**Answer:** Amazon Web Services is a cloud platform that provides
services for compute, storage, databases, networking, and analytics.

### 114. Why did you use AWS?

**Answer:** I used AWS to demonstrate cloud data lake storage and
serverless analytics. S3 stores the data, Glue Data Catalog stores
metadata, and Athena queries the Gold Parquet files.

### 115. What is Amazon S3?

**Answer:** Amazon Simple Storage Service is object storage. It stores
objects in buckets and is commonly used for data lakes, backups, and
application files.

### 116. What is an S3 bucket?

**Answer:** A bucket is a top-level container for objects in S3. This
project uses `hcl-insurance-claims-1` in the Sydney region,
`ap-southeast-2`.

### 117. What is an S3 object?

**Answer:** An object is data stored in S3 together with its key and
metadata. The object key identifies its location in the bucket
namespace.

### 118. Does S3 have real folders?

**Answer:** S3 is object storage rather than a traditional file system.
What looks like folders is generally a key prefix, such as
`gold/claim_summary/`.

### 119. What is AWS Glue?

**Answer:** AWS Glue is a managed data integration service. It provides
data cataloging, ETL capabilities, and metadata management.

### 120. What is Glue Data Catalog?

**Answer:** A centralized metadata repository containing databases,
tables, columns, data types, and storage locations.

### 121. What is a Glue crawler?

**Answer:** A crawler scans data sources, infers schemas, and can create
or update table definitions in the Data Catalog.

### 122. Did you use a Glue crawler?

**Answer:** I attempted to create one, but the AWS account denied
crawler creation. I used Athena DDL statements to manually register the
external table definitions in Glue Data Catalog instead. The three Gold
tables were successfully queried through Athena.

### 123. Is a crawler mandatory for Athena?

**Answer:** No. Athena needs table metadata in the Data Catalog, but
metadata can be created manually using DDL or through other supported
methods. A crawler is convenient automation, not a requirement.

### 124. What is Amazon Athena?

**Answer:** Athena is a serverless query service that uses SQL to
analyze data stored in S3. It commonly uses Glue Data Catalog for table
metadata.

### 125. Why Athena instead of another database server?

**Answer:** Athena can query supported data formats directly in S3
without requiring me to manage a separate database server. It is useful
for serverless analytics.

### 126. What is an external table?

**Answer:** An external table stores metadata describing data located
outside a database engine's managed storage, such as Parquet files in
S3. Its definition points to the data location.

### 127. Difference between S3 and Glue Data Catalog?

**Answer:** S3 stores the actual data files. Glue Data Catalog stores
metadata describing the files, such as table names, column names, types,
and S3 locations.

### 128. Difference between Glue and Athena?

**Answer:** Glue provides data integration and metadata cataloging.
Athena is the SQL query service that uses metadata to query data in S3.

### 129. What is the Athena query result location?

**Answer:** Athena writes query results and related output files to a
configured S3 location. In this project it is
`s3://hcl-insurance-claims-1/athena-results/`.

### 130. How does Athena charge for queries?

**Answer:** Athena pricing commonly depends on the amount of data
scanned, subject to the pricing model and region. Columnar formats,
compression, partitions, and focused queries can reduce scanned data.

### 131. How can you reduce Athena query cost?

**Answer:** Use Parquet or other efficient formats, select only required
columns, filter data, partition large datasets appropriately, and avoid
repeatedly scanning unnecessary data.

### 132. What is partitioning in a data lake?

**Answer:** Partitioning organizes data into directory prefixes based on
column values, such as year and month. Query engines can skip irrelevant
partitions when filters match partition columns.

### 133. Did you partition your Gold datasets?

**Answer:** The current Gold outputs are Parquet datasets, but the
project does not implement a deliberate partitioning strategy.
Partitioning could be added if the dataset grows and query patterns
justify it.

### 134. What is IAM?

**Answer:** AWS Identity and Access Management controls who can access
AWS resources and which actions they can perform. It uses users, roles,
policies, and permissions.

### 135. What is least privilege?

**Answer:** Granting only the minimum permissions required to perform a
task. It reduces accidental or unauthorized access.

### 136. How would you secure your S3 bucket?

**Answer:** Keep public access blocked, use least-privilege IAM
policies, apply encryption, enable appropriate logging and monitoring,
and avoid embedding access keys in source code.

### 137. What if Athena cannot find a table?

**Answer:** I would check the selected Glue database, whether the table
exists, the S3 location in the table definition, permissions to read S3
and Glue metadata, and whether files match the declared schema and
format.

------------------------------------------------------------------------

# 7. GenAI and Ollama

### 138. What is Generative AI?

**Answer:** Generative AI refers to models that generate new content,
such as text, images, or code, based on input and learned patterns.

### 139. Why add GenAI to this project?

**Answer:** Claim notes contain unstructured text. The GenAI assistant
summarizes notes for a selected claim so a user can review information
more quickly. It demonstrates how AI can complement a data engineering
pipeline.

### 140. What is Ollama?

**Answer:** Ollama provides tools and services for running and accessing
large language models. This project uses the Ollama Cloud API to
generate summaries.

### 141. What is an LLM?

**Answer:** A Large Language Model is a machine learning model trained
on large amounts of text to understand and generate language.

### 142. What is a prompt?

**Answer:** A prompt is the instruction and context provided to a
language model. It guides the model's response.

### 143. What is prompt engineering?

**Answer:** Designing clear instructions and context to improve the
relevance, consistency, and usefulness of model outputs.

### 144. How does your AI Claims Assistant work?

**Answer:** The user selects a claim ID. The application filters claim
notes for that ID, combines the notes into a prompt, sends the prompt to
Ollama Cloud, and displays the generated summary.

### 145. What is an API?

**Answer:** An Application Programming Interface allows software systems
to communicate through defined requests and responses. The application
calls the Ollama API to send prompts and receive model output.

### 146. Why store the API key in `.env`?

**Answer:** It separates sensitive credentials from source code. The
`.env` file is excluded from Git using `.gitignore`, reducing accidental
exposure.

### 147. What is hallucination in GenAI?

**Answer:** A hallucination occurs when a model generates information
that sounds plausible but is unsupported or incorrect. AI-generated
summaries must be checked against the original notes.

### 148. Can the AI decide whether a claim is fraudulent?

**Answer:** No. The current feature summarizes claim notes and may
highlight observations. It is not a validated fraud detection model and
does not make final fraud or claim decisions. A human reviewer must
assess the original evidence.

### 149. How would you improve the AI feature?

**Answer:** I would add structured output, source-note references, input
length controls, stronger prompt instructions, evaluation datasets,
human feedback, logging, access controls, and safeguards against
sensitive-data leakage. I would measure summary accuracy and
consistency.

### 150. Difference between summarization and classification?

**Answer:** Summarization produces a shorter representation of source
text. Classification assigns an item to predefined categories. The
current AI feature performs summarization, not a validated fraud
classification task.

### 151. What is temperature in a language model?

**Answer:** Temperature controls randomness in token selection. Lower
values generally produce more predictable outputs, while higher values
can produce more varied outputs. Available settings depend on the API
and model.

### 152. What is RAG?

**Answer:** Retrieval-Augmented Generation combines retrieval of
relevant external information with generation by a language model.
Retrieved context is supplied to the model to ground its answer. The
current project does not implement a full RAG architecture; it retrieves
notes for a selected claim and sends them directly in a prompt.

### 153. Difference between a chatbot and an AI summarizer?

**Answer:** A chatbot is designed for conversational interaction across
turns. A summarizer focuses on condensing source information. The
project's AI feature is primarily a claim-note summarizer.

------------------------------------------------------------------------

# 8. Streamlit and Frontend

### 154. What is Streamlit?

**Answer:** Streamlit is a Python framework for building interactive
data applications. It lets developers create web interfaces using Python
without a separate frontend application.

### 155. Why did you use Streamlit?

**Answer:** It allowed me to build a working dashboard quickly using the
Python ecosystem. It supports metrics, charts, tables, user inputs, and
downloads.

### 156. What pages are in your application?

**Answer:** Dashboard, Claim Details, and AI Claims Assistant.

### 157. What is displayed on the Dashboard?

**Answer:** Claim metrics, approved and denied counts, approval
percentage, claim status analysis, policy analysis, fraud investigation
analysis, and missing amount information.

### 158. What does Claim Details do?

**Answer:** It lets a user select a claim ID, view associated notes, see
the note count, and download selected notes as a CSV file.

### 159. What does the AI Claims Assistant do?

**Answer:** It retrieves notes for a selected claim and sends them to
Ollama Cloud to generate a summary and observations.

### 160. What is Plotly?

**Answer:** Plotly is a visualization library used to create interactive
charts, including hover information, zooming, and interactive legends.

### 161. How do you run Streamlit?

**Answer:**

``` powershell
.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

The app normally opens at `http://localhost:8501`.

### 162. What is `st.cache_data`?

**Answer:** It caches results of data-loading or data-processing
functions so Streamlit does not repeat expensive work on every rerun.
Cached data should be refreshed when its source changes.

### 163. How does Streamlit handle user interaction?

**Answer:** Streamlit reruns the application script when a user
interacts with a widget. Widget values are used to update displayed
content.

### 164. How would you deploy Streamlit?

**Answer:** I could deploy it on a suitable hosting platform or cloud
compute service. Production deployment would need secure secrets,
authentication, network controls, logging, and resource limits.

------------------------------------------------------------------------

# 9. Security, GitHub, and Testing

### 165. What is Git?

**Answer:** Git is a distributed version control system used to track
changes in source code.

### 166. What is GitHub?

**Answer:** GitHub is a platform for hosting Git repositories and
collaborating on software projects.

### 167. What is `.gitignore`?

**Answer:** It specifies files and folders Git should not track, such as
virtual environments, cache files, temporary files, and local secrets.

### 168. Why should `.env` not be uploaded?

**Answer:** It contains secrets such as API keys. If exposed, another
person could misuse the credentials. It should be excluded from Git, and
credentials should be rotated if exposed.

### 169. Does `.gitignore` remove a file already committed?

**Answer:** No. `.gitignore` prevents untracked matching files from
being added in the future. A file already tracked must be removed from
tracking. Exposed secrets must be rotated and may need removal from Git
history.

### 170. What is a Git commit?

**Answer:** A recorded snapshot of tracked changes in a Git repository.

### 171. What is a Git push?

**Answer:** `git push` uploads local commits to a remote repository such
as GitHub.

### 172. What is a Git pull?

**Answer:** `git pull` fetches changes from a remote repository and
integrates them into the current local branch.

### 173. What is a Git branch?

**Answer:** An independent line of development. It allows changes to be
developed without directly modifying the main branch.

### 174. How do you list files tracked by Git?

**Answer:**

``` bash
git ls-files
```

### 175. How do you check the working tree?

**Answer:**

``` bash
git status
```

### 176. What testing did you perform?

**Answer:** I checked dataset exploration and row counts, validated
MySQL tables and relationships, ran PySpark read, clean, and Gold
scripts, verified Athena Gold tables and queries, tested the Ollama
summarizer, and tested the Streamlit pages.

### 177. What is unit testing?

**Answer:** Unit testing checks a small unit of code, such as a
function, independently from the rest of the system.

### 178. What is integration testing?

**Answer:** Integration testing checks whether multiple components work
together, such as Python connecting to MySQL or Streamlit calling the
Ollama API.

### 179. What is end-to-end testing?

**Answer:** End-to-end testing checks a complete workflow from input to
final output. For this project, that includes verifying data pipeline
outputs, cloud analytics, and frontend behavior.

### 180. What is logging?

**Answer:** Logging records events, warnings, errors, and execution
information. It helps diagnose failures and monitor pipeline behavior.

### 181. How would you monitor a production pipeline?

**Answer:** I would record job start and end times, row counts, rejected
records, execution status, processing duration, and errors. I would
configure alerts and retain logs for troubleshooting.

------------------------------------------------------------------------

# 10. Scenario-Based Questions

### 182. What if input record counts suddenly drop?

**Answer:** Compare incoming file counts with historical counts,
validate file completeness, inspect source changes, and stop downstream
processing if input is incomplete. Log the issue and notify the
responsible team.

### 183. What if a new column appears in a source CSV?

**Answer:** Detect the schema change, determine whether the new column
is required, update schema and transformation logic if appropriate, and
test downstream outputs before release.

### 184. What if a claim has no matching policy?

**Answer:** Flag it as a data-quality issue and investigate the source.
A database foreign key should prevent invalid references if enforced
during insertion. Do not silently discard the record without a
documented rule.

### 185. What if an Athena query returns no rows?

**Answer:** Check the table's S3 location, whether files exist, selected
database, table schema, file format, and IAM permissions. Run a small
preview query.

### 186. What if the Ollama API is unavailable?

**Answer:** Show a clear error, log the failure without logging the API
key, and allow non-AI dashboard functionality to continue. Do not
present a fabricated summary.

### 187. What if the same CSV is loaded twice?

**Answer:** The current loader checks whether target tables already
contain records and stops to prevent accidental duplicate loading. A
production pipeline should use stronger idempotent loading, such as
batch identifiers, staging tables, unique constraints, and controlled
upserts.

### 188. What if a PySpark job fails halfway through?

**Answer:** Inspect logs and identify the failing stage. Check whether
partial outputs were written and make the job safe to rerun. Production
pipelines can write to temporary locations and publish completed outputs
only after validation.

### 189. What if the dataset grows from hundreds to millions of rows?

**Answer:** Use an appropriately sized Spark environment, tune
partitions, optimize joins, use Parquet, consider partitioning, monitor
execution and memory, and use orchestration to manage jobs.

### 190. How would you make this project production-ready?

**Answer:** Add automated orchestration, scheduled ingestion,
data-quality gates, monitoring and alerts, retries, structured logging,
IAM least privilege, encryption, secrets management, CI/CD, automated
tests, data lineage, and recovery procedures.

### 191. How would you handle personally identifiable information?

**Answer:** Identify sensitive fields, minimize collected data, apply
role-based access controls, encrypt data, mask or tokenize fields where
appropriate, define retention policies, and avoid sending unnecessary
personal data to external AI services.

### 192. Would you send every claim field to GenAI?

**Answer:** No. I would send only the minimum relevant notes and context
required for summarization. I would mask unnecessary sensitive
information and follow organizational privacy and vendor policies.

------------------------------------------------------------------------

# 11. Quick-Fire Questions

  -----------------------------------------------------------------------
  Question                            Answer
  ----------------------------------- -----------------------------------
  What does CSV stand for?            Comma-Separated Values

  What does ETL stand for?            Extract, Transform, Load

  What does ELT stand for?            Extract, Load, Transform

  What does OLTP stand for?           Online Transaction Processing

  What does OLAP stand for?           Online Analytical Processing

  What does ACID stand for?           Atomicity, Consistency, Isolation,
                                      Durability

  What does JVM stand for?            Java Virtual Machine

  What does API stand for?            Application Programming Interface

  What does IAM stand for?            Identity and Access Management

  What does AWS stand for?            Amazon Web Services

  What does S3 stand for?             Simple Storage Service

  What does DDL stand for?            Data Definition Language

  What does DML stand for?            Data Manipulation Language

  What does DQL stand for?            Data Query Language

  What does NULL mean?                Missing or unknown value

  What is a primary key?              Uniquely identifies a row

  What is a foreign key?              References a key in another table

  What is Parquet?                    Columnar file format optimized for
                                      analytics

  What is a data catalog?             Repository of metadata describing
                                      datasets and tables

  What is a data pipeline?            Sequence of steps that ingests,
                                      transforms, validates, and delivers
                                      data

  What is a data lake?                Storage for raw and processed data
                                      in different formats

  What is a data warehouse?           Integrated data system for
                                      reporting and analytics

  What is a crawler?                  Tool that scans data sources and
                                      infers catalog metadata

  What is a serverless service?       A service where the provider
                                      manages underlying infrastructure

  What is a data-quality check?       Validation against requirements for
                                      completeness, accuracy,
                                      consistency, validity, or
                                      uniqueness
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 12. Project-Specific Questions You Must Know

### 193. What are the five datasets?

**Answer:** Policies, beneficiaries, claims, claims fraud, and claims
notes.

### 194. How many records are in each dataset?

**Answer:** Policies: 50; beneficiaries: 100; claims: 100; claims fraud:
102; claims notes: 238. Total: 590.

### 195. What are the three Gold datasets?

**Answer:** `claim_summary`, `policy_analysis`, and `fraud_analysis`.

### 196. What columns are calculated in claim summary?

**Answer:** Status, total claims, total claim amount, average claim
amount, and missing amount count.

### 197. What does policy analysis calculate?

**Answer:** It groups claims by policy type and calculates total claims,
total claim amount, and average claim amount.

### 198. What does fraud analysis calculate?

**Answer:** It groups investigations by fraud type and outcome and
calculates the total investigations in each group.

### 199. Where are Gold datasets stored locally?

**Answer:** Under `data/gold/`, in `claim_summary`, `policy_analysis`,
and `fraud_analysis` folders.

### 200. Where are Gold datasets stored in AWS?

**Answer:** Under `s3://hcl-insurance-claims-1/gold/`, with one prefix
for each Gold dataset.

### 201. What is your AWS region?

**Answer:** `ap-southeast-2`, Asia Pacific (Sydney).

### 202. What is your Glue database name?

**Answer:** `insurance_claims_catalog`.

### 203. What is your Athena results location?

**Answer:** `s3://hcl-insurance-claims-1/athena-results/`.

### 204. Why did you not use a Glue crawler?

**Answer:** Crawler creation was denied by the AWS account. I manually
created the external table definitions through Athena DDL, which
registered the tables in Glue Data Catalog.

### 205. What are the three Streamlit pages?

**Answer:** Dashboard, Claim Details, and AI Claims Assistant.

### 206. Which file runs the frontend?

**Answer:** The root-level `app.py` file.

### 207. Which command starts the frontend?

**Answer:**

``` powershell
python -m streamlit run app.py
```

### 208. Which file contains the Ollama configuration?

**Answer:** The root-level `.env` file. It is excluded from Git.

### 209. Which file loads CSV data into MySQL?

**Answer:** `python/03_load_csv_to_mysql.py`.

### 210. Which file creates the schema report?

**Answer:** `python/02_generate_schema_report.py`.

### 211. Which file creates the Gold datasets?

**Answer:** `pyspark/03_create_gold.py`.

### 212. Which file validates MySQL tables?

**Answer:** `mysql/03_validate_tables.sql`.

### 213. Where do you run PySpark?

**Answer:** In Ubuntu WSL2, using `.venv-linux`.

### 214. Where do you run Streamlit and Ollama Python scripts?

**Answer:** In Windows PowerShell, using `.venv`.

------------------------------------------------------------------------

# 13. Suggested Live Demonstration

Use this sequence for a short project demonstration:

1.  **Introduction:** Explain the business problem and project
    objective.
2.  **Dataset:** Show the five CSV files and explain their
    relationships.
3.  **MySQL:** Show the five tables and execute a count or join query.
4.  **PySpark:** Explain the three scripts and show Silver and Gold
    output folders.
5.  **AWS S3:** Show the Bronze, Silver, and Gold prefixes.
6.  **Glue and Athena:** Show the Glue database and execute a Gold
    query.
7.  **Streamlit:** Show Dashboard, Claim Details, and AI Claims
    Assistant.
8.  **Conclusion:** Summarize technologies and what you learned.

Do not spend too much time showing setup screens. Focus on the working
pipeline, results, and technical decisions.

------------------------------------------------------------------------

# 14. Final Viva Preparation Advice

## Questions you should answer confidently

1.  Explain the complete architecture in two minutes.
2.  Why did you choose MySQL?
3.  Why did you use PySpark for a small dataset?
4.  What is the Medallion Architecture?
5.  Difference between Bronze, Silver, and Gold?
6.  Why did you choose Parquet?
7.  Difference between S3 and Glue Data Catalog?
8.  Why did you use Athena?
9.  Why did you manually create Glue tables?
10. Explain relationships between your five MySQL tables.
11. Explain your three Gold datasets.
12. How does the AI assistant work?
13. How do you protect your API key?
14. What happens if the API is unavailable?
15. What would you improve for production?

## A simple structure for answering technical questions

1.  **Definition:** Explain what the technology or concept means.
2.  **Purpose:** Explain why it is needed.
3.  **Implementation:** Explain where and how you used it.
4.  **Result:** Explain what it produced in your project.

Example:

**Question: Why did you use Amazon Athena?**

**Answer:** Athena is a serverless SQL query service. I used it because
my Gold datasets are stored as Parquet files in Amazon S3. I registered
the table definitions in Glue Data Catalog and used Athena to run SQL
queries on the Gold data without managing a database server.

------------------------------------------------------------------------

# Final Reminder

Understand your own code and be honest about the implementation.

Do not claim that: - The project is real-time when it is batch-based. -
Spark is running on a multi-node cluster when it is running in local
mode. - A Glue crawler was successfully used when tables were registered
manually. - The AI assistant detects fraud when it only summarizes claim
notes. - A complete star schema or production orchestration has been
implemented when it has not.

A clear explanation of what you built, why you built it, what worked,
and what you would improve is stronger than memorized answers.
