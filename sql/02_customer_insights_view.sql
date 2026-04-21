/* 
   Customer Insights View (RFM + Behavioural Metrics)
   --------------------------------------------------
   Produces customer-level metrics including:
   - Recency, Frequency, Monetary (RFM)
   - Net profit allocation
   - CSAT and ticket behaviour
   - Customer status (Active / At-Risk / Churned)
   - Revenue and profit buckets
*/


CREATE OR ALTER VIEW dbo.vw_CustomerInsights AS 
WITH MaxDate AS (
    SELECT MAX(OrderDate) AS MaxOrderDate
    FROM dbo.Fact_Sales
),
Raw_metrics AS (
    SELECT
        s.CustomerKey,
        s.OrderID,
        s.OrderDate,
        s.TotalRevenue,
        s.ShippingCost,
        -- ALLOCATED SHIPPING LOGIC
        ((p.UnitPrice - p.CostPrice) * s.Quantity) - 
        (s.ShippingCost / COUNT(*) OVER(PARTITION BY s.OrderID)) AS NetProfit,
        DATEDIFF(
            DAY,
            s.OrderDate,
            LEAD(s.OrderDate) OVER (PARTITION BY s.CustomerKey ORDER BY s.OrderDate)
        ) AS DaysToNextOrder
    FROM dbo.Fact_Sales s
    JOIN dbo.Dim_Products p 
        ON s.ProductKey = p.ProductKey
),
CSAT AS (
    SELECT 
        S.CustomerKey,
        ROUND(AVG(CAST(ST.CSAT_Score AS FLOAT)), 2) AS AvgCSATScore,
        COUNT(ST.TicketID) AS TicketCount
    FROM dbo.Fact_Sales S
    JOIN dbo.Fact_Support_Tickets ST
        ON S.SalesID = ST.SalesID
    GROUP BY S.CustomerKey
),
Customer_Aggregation AS (
    SELECT
        r.CustomerKey,
        MIN(r.OrderDate) AS First_Order_Date,
        DATEDIFF(
            DAY, 
            MAX(r.OrderDate), 
            MAX(m.MaxOrderDate)
        ) AS Recency,
        COUNT(DISTINCT r.OrderID) AS Frequency_Count,
        -- Note: Avg_Cadence_Days will naturally be NULL for one-time buyers. 
               AVG(r.DaysToNextOrder) AS Avg_Cadence_Days,
        SUM(r.TotalRevenue) AS Total_Revenue,
        SUM(r.NetProfit) AS Total_Net_Profit,
        MAX(cs.AvgCSATScore) AS Avg_CSAT_Score,
        ISNULL(MAX(cs.TicketCount), 0) AS Total_Tickets_Count
    FROM Raw_metrics r
    CROSS JOIN MaxDate m
    LEFT JOIN CSAT cs
        ON r.CustomerKey = cs.CustomerKey
    GROUP BY r.CustomerKey
),
Bucketed AS (
    SELECT
        CA.*,
        C.Region,
        CASE 
            WHEN CA.Recency <= 60 THEN 'Active'
            WHEN CA.Recency BETWEEN 61 AND 180 THEN 'At-Risk'
            ELSE 'Churned'
        END AS Customer_Status,
        NTILE(4) OVER (ORDER BY CA.Total_Revenue) AS Revenue_Bucket,
        NTILE(4) OVER (ORDER BY CA.Total_Net_Profit) AS Profit_Bucket,
        (CA.Total_Net_Profit / NULLIF(CA.Total_Revenue, 0)) AS [Net_Margin%],
        C.Tier AS Customer_Tier
    FROM Customer_Aggregation CA
    INNER JOIN dbo.Dim_Customers C
        ON CA.CustomerKey = C.CustomerKey
)
SELECT * FROM Bucketed;
GO
