# create crypto database
CREATE DATABASE IF NOT EXISTS crypto;


USE crypto;
CREATE TABLE IF NOT EXISTS prices
(
id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
ts_local DATETIME NOT NULL,
ts_utc DATETIME NOT NULL,
btc_rate_usd FLOAT NOT NULL,
btc_rate_gbp FLOAT NOT NULL,
num_btc_owned FLOAT NOT NULL,
worth_gbp FLOAT NOT NULL,
container_version VARCHAR(8) NOT NULL
);
#CREATE INDEX actual_loc_ndx ON actual(location);
