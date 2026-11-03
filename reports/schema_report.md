# Insurance Claims - Dataset Schema Report


## Dataset: beneficiaries.csv.csv

- Rows: 100
- Columns: 5
- Duplicate rows: 0

### Column details

| Column | Pandas Type | Missing Values |
|---|---|---:|
| id | int64 | 0 |
| policy_id | int64 | 0 |
| name | str | 49 |
| relationship | str | 9 |
| date_of_birth | str | 0 |

### Sample records

```text
 id  policy_id           name relationship date_of_birth
  1         26 Grace Hoffmann       spouse    1982-06-08
  2         25  Ibrahim Silva       spouse    2008-10-23
  3         18    James Smith       spouse    1940-08-20
  4         27            NaN          NaN    2001-04-07
  5          7            NaN        child    2008-11-14
```

## Dataset: claims.csv.csv

- Rows: 100
- Columns: 7
- Duplicate rows: 0

### Column details

| Column | Pandas Type | Missing Values |
|---|---|---:|
| id | int64 | 0 |
| policy_id | int64 | 0 |
| status | str | 0 |
| amount | float64 | 73 |
| submitted_at | str | 0 |
| created_at | str | 0 |
| updated_at | str | 5 |

### Sample records

```text
 id  policy_id    status  amount submitted_at created_at updated_at
  1         22 in_review  204.47   2024-08-04 2024-10-12 2024-12-01
  2         20 submitted     NaN   2024-11-06 2023-01-12 2023-11-03
  3          5 in_review 3833.36   2024-04-25 2023-06-17 2023-09-19
  4         46    denied  367.32   2024-08-14 2024-07-22 2023-08-02
  5          6 submitted     NaN   2024-01-31 2024-07-08 2024-05-20
```

## Dataset: claims_fraud.csv.csv

- Rows: 102
- Columns: 6
- Duplicate rows: 0

### Column details

| Column | Pandas Type | Missing Values |
|---|---|---:|
| id | int64 | 0 |
| claim_id | int64 | 0 |
| investigation_notes | str | 0 |
| created_at | str | 0 |
| fraud_type | str | 0 |
| outcome | str | 0 |

### Sample records

```text
 id  claim_id                                                    investigation_notes created_at fraud_type     outcome
  1        47                          A routine follow-up: the claim was processed. 2024-07-21   internal   dismissed
  2        72      The supplier confirmed the details and the request was processed. 2024-11-08   internal   dismissed
  3        15                Support asked for a change and the refund was replaced. 2024-10-17   external   confirmed
  4        71 The account owner confirmed the details and the account was processed. 2024-02-06   internal   dismissed
  5        11          The reviewer reported an urgent issue; the item was replaced. 2023-06-30   internal unconfirmed
```

## Dataset: claims_notes.csv.csv

- Rows: 238
- Columns: 6
- Duplicate rows: 0

### Column details

| Column | Pandas Type | Missing Values |
|---|---|---:|
| id | int64 | 0 |
| claim_id | int64 | 0 |
| note | str | 0 |
| created_at | str | 0 |
| priority | str | 0 |
| updated_at | str | 0 |

### Sample records

```text
 id  claim_id                                                               note created_at priority updated_at
  1        90     The courier reported a standard issue; the ticket was updated. 2023-08-10      low 2023-07-06
  2         1 The reviewer confirmed the details and the delivery was cancelled. 2024-12-04   medium 2023-11-14
  3        14                   The claim was completed following a late review. 2024-07-23      low 2024-07-26
  4        59             Flagged as partial. The supplier replaced the request. 2023-04-25   medium 2023-05-08
  5        22                         A partial ticket was updated the same day. 2024-08-23   medium 2023-08-09
```

## Dataset: policies.csv.csv

- Rows: 50
- Columns: 5
- Duplicate rows: 0

### Column details

| Column | Pandas Type | Missing Values |
|---|---|---:|
| id | int64 | 0 |
| policy_number | str | 0 |
| type | str | 0 |
| start_date | str | 0 |
| end_date | str | 7 |

### Sample records

```text
 id policy_number type start_date   end_date
  1      POL-0108 home 2023-02-16 2025-09-30
  2      POL-7806 home 2024-01-26 2024-03-16
  3      POL-5222 home 2023-01-06 2024-12-24
  4      POL-4040 auto 2024-04-15 2025-11-11
  5      POL-8891 auto 2024-10-02 2025-06-11
```