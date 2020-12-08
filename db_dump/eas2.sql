create table eas
(
    id                SERIAL
        primary key,
    product_base_name varchar(510) default '' not null,
    trade_name_id     bigint                  null,
    trade_name        varchar(510) default '' not null,
    ean               float                   null
);

