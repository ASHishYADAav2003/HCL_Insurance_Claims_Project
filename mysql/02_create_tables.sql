
-- ==================================================
-- INSURANCE CLAIMS DATA WAREHOUSE
-- CREATE FIVE SOURCE TABLES
-- ==================================================

USE insurance_claims_db;

-- 1. POLICIES TABLE
CREATE TABLE IF NOT EXISTS policies (
    id INT PRIMARY KEY,
    policy_number VARCHAR(30) NOT NULL,
    policy_type VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL
) ENGINE=InnoDB;


-- 2. BENEFICIARIES TABLE
CREATE TABLE IF NOT EXISTS beneficiaries (
    id INT PRIMARY KEY,
    policy_id INT NOT NULL,
    name VARCHAR(150) NULL,
    relationship VARCHAR(50) NULL,
    date_of_birth DATE NOT NULL,

    CONSTRAINT fk_beneficiaries_policy
        FOREIGN KEY (policy_id)
        REFERENCES policies(id)
) ENGINE=InnoDB;


-- 3. CLAIMS TABLE
CREATE TABLE IF NOT EXISTS claims (
    id INT PRIMARY KEY,
    policy_id INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    amount DECIMAL(12,2) NULL,
    submitted_at DATE NOT NULL,
    created_at DATE NOT NULL,
    updated_at DATE NULL,

    CONSTRAINT fk_claims_policy
        FOREIGN KEY (policy_id)
        REFERENCES policies(id)
) ENGINE=InnoDB;


-- 4. CLAIMS FRAUD TABLE
CREATE TABLE IF NOT EXISTS claims_fraud (
    id INT PRIMARY KEY,
    claim_id INT NOT NULL,
    investigation_notes TEXT NOT NULL,
    created_at DATE NOT NULL,
    fraud_type VARCHAR(50) NOT NULL,
    outcome VARCHAR(50) NOT NULL,

    CONSTRAINT fk_fraud_claim
        FOREIGN KEY (claim_id)
        REFERENCES claims(id)
) ENGINE=InnoDB;


-- 5. CLAIMS NOTES TABLE
CREATE TABLE IF NOT EXISTS claims_notes (
    id INT PRIMARY KEY,
    claim_id INT NOT NULL,
    note TEXT NOT NULL,
    created_at DATE NOT NULL,
    priority VARCHAR(30) NOT NULL,
    updated_at DATE NOT NULL,

    CONSTRAINT fk_notes_claim
        FOREIGN KEY (claim_id)
        REFERENCES claims(id)
) ENGINE=InnoDB;


-- ==================================================
-- VERIFY TABLE CREATION
-- ==================================================

SHOW TABLES;
