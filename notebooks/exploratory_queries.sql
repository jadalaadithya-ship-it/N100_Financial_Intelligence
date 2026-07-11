-- 1. Total companies
SELECT COUNT(*) FROM companies;

-- 2. Top 10 companies by sales
SELECT company_id, sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;

-- 3. Top 10 companies by net profit
SELECT company_id, net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;

-- 4. Companies with negative net profit
SELECT company_id, year, net_profit
FROM profitandloss
WHERE net_profit < 0;

-- 5. Balance sheet verification
SELECT company_id, year
FROM balancesheet
WHERE total_assets != total_liabilities;

-- 6. Total market capitalization
SELECT SUM(market_cap_crore)
FROM market_cap;

-- 7. Number of documents
SELECT COUNT(*)
FROM documents;

-- 8. Number of stock price records
SELECT COUNT(*)
FROM stock_prices;

-- 9. Distinct sectors
SELECT DISTINCT broad_sector
FROM sectors;

-- 10. Companies with highest ROE
SELECT company_id, return_on_equity_pct
FROM financial_ratios
ORDER BY return_on_equity_pct DESC
LIMIT 10;