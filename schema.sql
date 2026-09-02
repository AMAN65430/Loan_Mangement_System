
CREATE DATABASE IF NOT EXISTS loan_management_system
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE loan_management_system;

CREATE TABLE IF NOT EXISTS admins (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50)  NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    created_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS loan_applications (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    full_name         VARCHAR(100)  NOT NULL,
    email             VARCHAR(100)  NOT NULL,
    mobile_number     VARCHAR(15)   NOT NULL,
    age               INT           NOT NULL,
    monthly_income    DECIMAL(12,2) NOT NULL,
    employment_type   ENUM('Salaried', 'Self-Employed') NOT NULL,
    loan_amount       DECIMAL(12,2) NOT NULL,
    loan_purpose      VARCHAR(255)  NOT NULL,
    credit_score      INT           NOT NULL,
    eligible_amount   DECIMAL(12,2) NOT NULL,
    risk_level        ENUM('Low', 'Medium', 'High') NOT NULL,
    status            ENUM('Approved', 'Pending', 'Rejected') NOT NULL DEFAULT 'Pending',
    created_at        TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_full_name (full_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


