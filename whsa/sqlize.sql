.log stderr
.bail on
.changes on
.echo on
.mode csv


DROP TABLE IF EXISTS employee;
CREATE TABLE employee (
    year INTEGER,
    president CHAR(30),
    last_name VARCHAR,
    first_name VARCHAR,
    middle_name VARCHAR,
    suffix VARCHAR,
    full_name VARCHAR,
    status VARCHAR,
    salary NUMERIC,
    pay_basis VARCHAR,
    position_title VARCHAR,
    white_house_review VARCHAR
);


.import data/wrangled/white_house_salaries.csv employee

-- Because .import includes the header, the first row of the dataset is
-- the header, which we obviously don't want. So we delete it:

DELETE FROM employee where rowid = 1 AND salary = 'salary';


CREATE INDEX employee_idx_last_first_name
    ON employee(last_name COLLATE NOCASE, first_name COLLATE NOCASE);

CREATE INDEX employee_idx_salary
    ON employee(salary);
