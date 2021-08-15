# create crypto database - hold eth and btc
CREATE DATABASE IF NOT EXISTS crypto_btc;


USE crypto;
CREATE TABLE IF NOT EXISTS btc_prices
(
id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
ts_local DATETIME NOT NULL,
ts_utc DATETIME NOT NULL,
btc_rate_usd FLOAT NOT NULL,
btc_rate_gbp FLOAT NOT NULL,
btc_rate_eur FLOAT NOT NULL,
btc_avg_50 FLOAT NOT NULL,
btc_avg_200 FLOAT NOT NULL,
btc_volume FLOAT NOT NULL,
btc_avg_volume FLOAT NOT NULL,
container_version VARCHAR(8) NOT NULL
);

# Blockchain basic metrics
USE crypto;
CREATE TABLE IF NOT EXISTS btc_bchain
(
id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
ts_local DATETIME NOT NULL,
ts_utc DATETIME NOT NULL,
btc_nodes INT NOT NULL,
difficulty FLOAT NOT NULL,
network_hashrate FLOAT NOT NULL,
pooledtx INT NOT NULL,
container_version VARCHAR(8) NOT NULL
);
# Num wallets ?

#CREATE TABLE IF NOT EXISTS eth
#(
#id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
#ts_local DATETIME NOT NULL,
#ts_utc DATETIME NOT NULL,
#eth_rate_usd FLOAT NOT NULL,
#eth_rate_gbp FLOAT NOT NULL,
#eth_rate_eur FLOAT NOT NULL,
#eth_avg_50 FLOAT NOT NULL,
#eth_avg_200 FLOAT NOT NULL,
#eth_volume FLOAT NOT NULL,
#eth_avg_volume FLOAT NOT NULL,
#container_version VARCHAR(8) NOT NULL
#);


#CREATE INDEX actual_loc_ndx ON actual(location);
# put my own holdings in another database
#num_btc_owned FLOAT NOT NULL,
#worth_gbp FLOAT NOT NULL,
#create similar for Ethereum