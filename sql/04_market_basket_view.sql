/* 
   Market Basket Analysis View
   ---------------------------
   Computes product-pair metrics including:
   - Support
   - Confidence
   - Lift
   - Combined pair net profit

   Used to identify cross-sell opportunities and profitable product associations.
*/

CREATE OR ALTER VIEW dbo.vw_MarketBasketAnalysis AS
WITH Total_Orders AS (
    SELECT COUNT(DISTINCT OrderID) AS Total_Unique_Orders 
    FROM dbo.Fact_Sales
),
Product_Frequencies AS (
    SELECT ProductKey, COUNT(DISTINCT OrderID) AS Prod_Order_Count
    FROM dbo.Fact_Sales 
    GROUP BY ProductKey
),
Line_Level_Profit AS (
    SELECT 
        s.OrderID, 
        s.ProductKey,
        -- Profit after split shipping cost
        ((p.UnitPrice - p.CostPrice) * s.Quantity) - 
        (s.ShippingCost / COUNT(*) OVER(PARTITION BY s.OrderID)) AS AllocatedNetProfit
    FROM dbo.Fact_Sales s
    JOIN dbo.Dim_Products p ON s.ProductKey = p.ProductKey
),
Pairs AS (
    SELECT 
        LPA.OrderID,
        LPA.ProductKey AS Product_A,
        LPA.AllocatedNetProfit AS Profit_A,
        LPB.ProductKey AS Product_B,
        LPB.AllocatedNetProfit AS Profit_B
    FROM Line_Level_Profit LPA
    JOIN Line_Level_Profit LPB ON LPA.OrderID = LPB.OrderID
    WHERE LPA.ProductKey < LPB.ProductKey
),
Pair_Aggregates AS (
    SELECT 
        p.Product_A,
        p.Product_B,
        COUNT(p.OrderID) AS Pair_Frequency,
        SUM(p.Profit_A + p.Profit_B) AS Total_Pair_Net_Profit
    FROM Pairs p
    GROUP BY p.Product_A, p.Product_B
)
SELECT 
    agg.Product_A,
    PA.ProductName AS Product_A_Name,
    agg.Product_B,
    PB.ProductName AS Product_B_Name,
    agg.Pair_Frequency,

    -- 1. Support: % of all orders that contain this pair
    CAST(agg.Pair_Frequency * 1.0 / NULLIF(t.Total_Unique_Orders, 0) AS DECIMAL(10,4)) AS Support,

    -- 2. Confidence: How likely is B given A?
    CAST(agg.Pair_Frequency * 1.0 / NULLIF(pf1.Prod_Order_Count, 0) AS DECIMAL(10,4)) AS Confidence,

    -- 3. Lift: Strength of association (safeguarded against divide-by-zero)
    CAST((agg.Pair_Frequency * 1.0 / NULLIF(pf1.Prod_Order_Count, 0)) / 
        NULLIF((pf2.Prod_Order_Count * 1.0 / NULLIF(t.Total_Unique_Orders, 0)), 0) AS DECIMAL(10,4)) AS Lift,

    -- 4. Financials
    agg.Total_Pair_Net_Profit
FROM Pair_Aggregates agg
CROSS JOIN Total_Orders t
JOIN Product_Frequencies pf1 
    ON agg.Product_A = pf1.ProductKey
JOIN Product_Frequencies pf2 
    ON agg.Product_B = pf2.ProductKey
JOIN dbo.Dim_Products PA 
    ON agg.Product_A = PA.ProductKey
JOIN dbo.Dim_Products PB 
    ON agg.Product_B = PB.ProductKey;
GO
