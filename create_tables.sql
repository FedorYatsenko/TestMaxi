IF (NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'Fedor'))
BEGIN
    EXEC ('CREATE SCHEMA [Fedor]')
END;

IF object_id('Fedor.Orders', 'Table') IS NOT NULL DROP TABLE Fedor.Orders
IF object_id('Fedor.Counterparty', 'Table') IS NOT NULL DROP TABLE Fedor.Counterparty

CREATE TABLE Fedor.Counterparty
(
  counterparty_uuid          NVARCHAR(36)          NOT NULL,
  name                       NVARCHAR(100)         NOT NULL,
  CONSTRAINT PK_Counterparty PRIMARY KEY(counterparty_uuid)
);

CREATE TABLE Fedor.Orders
(
    id            NVARCHAR(36)    NOT NULL,
    name            NVARCHAR(5)     NOT NULL,
    description         NVARCHAR(MAX)   NULL,
    moment              DATETIME        NULL,
    sum                 INT             NULL,
    counterparty_uuid   NVARCHAR(36)    NOT NULL,
    CONSTRAINT PK_Orders PRIMARY KEY(id),
    CONSTRAINT FK_Orders_Counterparty FOREIGN KEY(counterparty_uuid)
    REFERENCES Fedor.Counterparty(counterparty_uuid)
);