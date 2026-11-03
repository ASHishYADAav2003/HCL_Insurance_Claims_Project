USE insurance_claims_db;

-- Display all tables
SHOW TABLES;

-- Count records in each table
SELECT 'policies' AS table_name, COUNT(*) AS total_rows
FROM policies

UNION ALL

SELECT 'beneficiaries', COUNT(*)
FROM beneficiaries

UNION ALL

SELECT 'claims', COUNT(*)
FROM claims

UNION ALL

SELECT 'claims_fraud', COUNT(*)
FROM claims_fraud

UNION ALL

SELECT 'claims_notes', COUNT(*)
FROM claims_notes;


-- =========================================
-- DATA QUALITY CHECKS
-- =========================================

-- 1. Check missing claim amounts
SELECT
    COUNT(*) AS total_claims,
    SUM(amount IS NULL) AS missing_amounts
FROM claims;

-- 2. Check missing beneficiary details
SELECT
    SUM(name IS NULL) AS missing_names,
    SUM(relationship IS NULL) AS missing_relationships
FROM beneficiaries;

-- 3. Check policies with no end date
SELECT
    COUNT(*) AS policies_without_end_date
FROM policies
WHERE end_date IS NULL;

-- 4. Check claims with no updated date
SELECT
    COUNT(*) AS claims_without_updated_date
FROM claims
WHERE updated_at IS NULL;

-- 5. Check claims referring to missing policies
SELECT COUNT(*) AS orphan_claims
FROM claims c
LEFT JOIN policies p
    ON c.policy_id = p.id
WHERE p.id IS NULL;

-- 6. Check fraud records referring to missing claims
SELECT COUNT(*) AS orphan_fraud_records
FROM claims_fraud f
LEFT JOIN claims c
    ON f.claim_id = c.id
WHERE c.id IS NULL;


-- =========================================
-- SQL ANALYTICS
-- =========================================

-- 1. Claim count by status
SELECT
    status,
    COUNT(*) AS total_claims
FROM claims
GROUP BY status
ORDER BY total_claims DESC;


-- 2. Fraud investigation outcome analysis
SELECT
    outcome,
    COUNT(*) AS total_cases
FROM claims_fraud
GROUP BY outcome
ORDER BY total_cases DESC;


-- 3. Total claim amount by policy type
SELECT
    p.policy_type,
    COUNT(c.id) AS total_claims,
    SUM(c.amount) AS total_claim_amount,
    ROUND(AVG(c.amount), 2) AS average_claim_amount
FROM policies p
LEFT JOIN claims c
    ON p.id = c.policy_id
GROUP BY p.policy_type
ORDER BY total_claim_amount DESC;