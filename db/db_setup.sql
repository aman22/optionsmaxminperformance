-- Drop the table if it already exists
DROP TABLE IF EXISTS options_flow;
DROP TABLE IF EXISTS tag;

-- Create the new table with "id" as the primary key
CREATE TABLE IF NOT EXISTS options_flow (
        id TEXT PRIMARY KEY,
        marketcap INTEGER,
        stock_multi_vol INTEGER,
        full_name TEXT,
        expiry DATE,
        no_side_vol INTEGER,
        nbbo_ask REAL,
        theta REAL,
        ask_vol INTEGER,
        volume INTEGER,
        price REAL,
        ewma_nbbo_bid REAL,
        open_interest INTEGER,
        nbbo_bid REAL,
        industry_type TEXT,
        implied_volatility REAL,
        er_time TEXT,
        sector TEXT,
        multi_vol INTEGER,
        gamma REAL,
        rule_id TEXT,
        underlying_symbol TEXT,
        executed_at DATETIME,
        strike REAL,
        rho REAL,
        vega REAL,
        flow_alert_id TEXT,
        delta REAL,
        size INTEGER,
        ewma_nbbo_ask REAL,
        option_type TEXT,
        underlying_price REAL,
        next_earnings_date DATE,
        upstream_condition_detail TEXT,
        bid_vol INTEGER,
        canceled BOOLEAN,
        exchange TEXT,
        theo REAL,
        premium REAL,
        option_chain_id TEXT,
        mid_vol INTEGER
    );

CREATE TABLE IF NOT EXISTS tag (
        flow_id TEXT,
        name TEXT,
        PRIMARY KEY (flow_id, name)
        );