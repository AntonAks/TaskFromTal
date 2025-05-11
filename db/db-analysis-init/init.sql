CREATE DATABASE analysis_db;

\c analysis_db;

CREATE TABLE IF NOT EXISTS organization_statistics (
    organization_name VARCHAR(1024) NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (organization_name)
);

CREATE TABLE IF NOT EXISTS organization_type_statistics (
    organization_type VARCHAR(1024) NOT NULL,
    quantity_studies INTEGER NOT NULL,
    quantity_organizations INTEGER NOT NULL,
    PRIMARY KEY (organization_type)
);