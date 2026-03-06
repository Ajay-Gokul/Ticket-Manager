# Ticket Manager Database Plan (MSSQL)

This document outlines the database schema for the Ticket Manager application using Microsoft SQL Server (MSSQL).

## Database System

- **Engine**: Microsoft SQL Server
- **Schema Strategy**: PascalCase. Primary keys use `UID` (UNIQUEIDENTIFIER). No table name prefixes in column names. Configuration tables for Roles and Statuses.

## Tables Schema

### 1. Roles (Configuration Table)

Stores the available user roles.

| Column | Type             | Constraints      | Description                               |
| :----- | :--------------- | :--------------- | :---------------------------------------- |
| UID    | UNIQUEIDENTIFIER | PRIMARY KEY      | Unique identifier for the role.           |
| Name   | VARCHAR(50)      | NOT NULL, UNIQUE | Name of the role (e.g., 'Admin', 'User'). |

### 2. Statuses (Configuration Table)

Stores the possible ticket statuses.

| Column | Type             | Constraints      | Description                                    |
| :----- | :--------------- | :--------------- | :--------------------------------------------- |
| UID    | UNIQUEIDENTIFIER | PRIMARY KEY      | Unique identifier for the status.              |
| Name   | VARCHAR(50)      | NOT NULL, UNIQUE | Name of the status (e.g., 'Open', 'Resolved'). |

### 3. Users

Stores user information and their assigned role.

| Column       | Type             | Constraints         | Description                     |
| :----------- | :--------------- | :------------------ | :------------------------------ |
| UID          | UNIQUEIDENTIFIER | PRIMARY KEY         | Unique identifier for the user. |
| Username     | VARCHAR(100)     | NOT NULL, UNIQUE    | Unique login name.              |
| Email        | VARCHAR(255)     | NOT NULL, UNIQUE    | User's email address.           |
| PasswordHash | VARCHAR(MAX)     | NOT NULL            | Securely hashed password.       |
| RoleUID      | UNIQUEIDENTIFIER | FOREIGN KEY (Roles) | Reference to the user's role.   |
| CreatedAt    | DATETIME         | NOT NULL            | Account creation timestamp.     |

### 4. Tickets

Stores ticket details and tracking information.

| Column      | Type             | Constraints            | Description                           |
| :---------- | :--------------- | :--------------------- | :------------------------------------ |
| UID         | UNIQUEIDENTIFIER | PRIMARY KEY            | Unique identifier for the ticket.     |
| Title       | VARCHAR(255)     | NOT NULL               | Short summary of the issue.           |
| Description | VARCHAR(MAX)     | NOT NULL               | Detailed explanation of the issue.    |
| StatusUID   | UNIQUEIDENTIFIER | FOREIGN KEY (Statuses) | Reference to the current status.      |
| Priority    | VARCHAR(50)      | NOT NULL               | Priority level (e.g., 'High', 'Low'). |
| CreatorUID  | UNIQUEIDENTIFIER | FOREIGN KEY (Users)    | The user who raised the ticket.       |
| AssigneeUID | UNIQUEIDENTIFIER | FOREIGN KEY (Users)    | The admin assigned to the ticket.     |
| CreatedAt   | DATETIME         | NOT NULL               | Ticket creation timestamp.            |
| UpdatedAt   | DATETIME         | NOT NULL               | Last update timestamp.                |

## Relationships

- **Users to Roles**: Many-to-One.
- **Tickets to Statuses**: Many-to-One.
- **Tickets to Users (Creator)**: Many-to-One.
- **Tickets to Users (Assignee)**: Many-to-One.

## SQL Initialization (MSSQL)

```sql
-- Create Roles Table
CREATE TABLE [config].Roles (
    UID UNIQUEIDENTIFIER PRIMARY KEY,
    Name VARCHAR(50) NOT NULL UNIQUE
);

-- Create Statuses Table
CREATE TABLE [config].Statuses (
    UID UNIQUEIDENTIFIER PRIMARY KEY,
    Name VARCHAR(50) NOT NULL UNIQUE
);

-- Create Users Table
CREATE TABLE [data].Users (
    UID UNIQUEIDENTIFIER PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE,
    Email VARCHAR(255) NOT NULL UNIQUE,
    PasswordHash VARCHAR(MAX) NOT NULL,
    RoleUID UNIQUEIDENTIFIER NOT NULL,
    CreatedAt DATETIME NOT NULL,
    CONSTRAINT FK_Users_Roles FOREIGN KEY (RoleUID) REFERENCES [config].Roles(UID)
);

-- Create Tickets Table
CREATE TABLE [data].Tickets (
    UID UNIQUEIDENTIFIER PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Description VARCHAR(MAX) NOT NULL,
    StatusUID UNIQUEIDENTIFIER NOT NULL,
    Priority VARCHAR(50) NOT NULL,
    CreatorUID UNIQUEIDENTIFIER NOT NULL,
    AssigneeUID UNIQUEIDENTIFIER NULL,
    CreatedAt DATETIME NOT NULL,
    UpdatedAt DATETIME NOT NULL,
    CONSTRAINT FK_Tickets_Statuses FOREIGN KEY (StatusUID) REFERENCES [config].Statuses(UID),
    CONSTRAINT FK_Tickets_Users_Creator FOREIGN KEY (CreatorUID) REFERENCES [data].Users(UID),
    CONSTRAINT FK_Tickets_Users_Assignee FOREIGN KEY (AssigneeUID) REFERENCES [data].Users(UID)
);
```
