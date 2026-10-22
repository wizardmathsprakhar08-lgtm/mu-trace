from typing import Dict, Any, List
from core.schema import EvidenceItem

COMPANIES_SEED: List[Dict[str, Any]] = [
    # ========================================================
    # TOP INDIAN BANKS (BFSI)
    # ========================================================
    {
        "ticker": "HDFCBANK.NS",
        "clean_symbol": "HDFCBANK",
        "name": "HDFC Bank Limited",
        "sector": "Financial Services",
        "industry": "Private Sector Banking",
        "currency": "INR",
        "unit": "₹ Crore",
        "fiscal_year_end": "31st March",
        "is_bank": True,
        "current_price": 1685.0,
        "shares_count": 761.5,
        "financials": {
            "period": "FY24",
            "is_bank": True,
            "revenue_current": 108532.0, # Net Interest Income (NII)
            "nii_current": 108532.0,
            "nii_prior": 86842.0,
            "total_income": 157770.0,
            "pat_current": 64060.0,
            "pat_prior": 44108.0,
            "advances_current": 2484865.0, # Gross Advances ₹ 24.8 Lakh Cr
            "advances_prior": 1600586.0,
            "deposits_current": 2379760.0, # Total Deposits ₹ 23.8 Lakh Cr
            "deposits_prior": 1883395.0,
            "net_worth": 444320.0,
            "total_assets": 3617623.0,
            "gnpa_current": 1.24, # 1.24%
            "nnpa_current": 0.33, # 0.33%
            "pcr_ratio": 74.0,
            "nim_percent": 3.63,
            "casa_ratio": 38.2,
            "crar_ratio": 18.8,
            "cost_to_income": 40.4
        },
        "evidence": [
            {
                "id": "S1",
                "source_title": "HDFC Bank Annual Report FY24",
                "doc_type": "Annual Report",
                "period": "FY24",
                "page_number": 115,
                "table_cell": "Consolidated Financial Summary",
                "content": "Gross advances reached ₹ 24,84,865 crore ($298 billion) post-merger with HDFC Limited, reflecting steady corporate and retail credit off-take while asset quality remained prime with Gross NPA at 1.24%."
            },
            {
                "id": "S2",
                "source_title": "HDFC Bank Q4 Investor Presentation",
                "doc_type": "Earnings Release",
                "period": "Q4FY24",
                "page_number": 34,
                "table_cell": "Capital Adequacy & Liquidity",
                "content": "Total Capital Adequacy Ratio (CRAR) under Basel III stood at 18.8% against regulatory requirement of 11.7%, with Tier-1 Capital at 16.8%."
            },
            {
                "id": "S3",
                "source_title": "HDFC Bank Audited Balance Sheet Note 11",
                "doc_type": "Audited Filing",
                "period": "FY24",
                "page_number": 194,
                "table_cell": "Deposit Franchise Profile",
                "content": "Total customer deposits mobilized expanded to ₹ 23,79,760 crore, maintaining a resilient low-cost CASA deposit ratio of 38.2%."
            }
        ]
    },
    {
        "ticker": "ICICIBANK.NS",
        "clean_symbol": "ICICIBANK",
        "name": "ICICI Bank Limited",
        "sector": "Financial Services",
        "industry": "Private Sector Banking",
        "currency": "INR",
        "unit": "₹ Crore",
        "fiscal_year_end": "31st March",
        "is_bank": True,
        "current_price": 1260.0,
        "shares_count": 702.4,
        "financials": {
            "period": "FY24",
            "is_bank": True,
            "revenue_current": 74306.0,
            "nii_current": 74306.0,
            "nii_prior": 62128.0,
            "total_income": 99754.0,
            "pat_current": 40888.0,
            "pat_prior": 31896.0,
            "advances_current": 1184406.0,
            "advances_prior": 1019638.0,
            "deposits_current": 1412825.0,
            "deposits_prior": 1180841.0,
            "net_worth": 242780.0,
            "total_assets": 1968744.0,
            "gnpa_current": 2.16,
            "nnpa_current": 0.42,
            "pcr_ratio": 80.3,
            "nim_percent": 4.53,
            "casa_ratio": 42.2,
            "crar_ratio": 16.33,
            "cost_to_income": 39.2
        },
        "evidence": [
            {
                "id": "S1",
                "source_title": "ICICI Bank Annual Report FY24",
                "doc_type": "Annual Report",
                "period": "FY24",
                "page_number": 74,
                "table_cell": "Consolidated Financial Highlights",
                "content": "Net Interest Income (NII) surged by 19.6% YoY to ₹ 74,306 crore, supported by a healthy Net Interest Margin (NIM) of 4.53% and broad-based loan growth of 16.2%."
            },
            {
                "id": "S2",
                "source_title": "ICICI Bank Earnings Conference Call",
                "doc_type": "Transcript",
                "period": "Q4FY24",
                "transcript_timestamp": "00:18:40",
                "content": "Management confirmed that Net NPA declined to an industry-leading 0.42% with Provision Coverage Ratio (PCR) standing robust at 80.3%."
            }
        ]
    },
    {
        "ticker": "SBIN.NS",
        "clean_symbol": "SBIN",
        "name": "State Bank of India",
        "sector": "Financial Services",
        "industry": "Public Sector Banking",
        "currency": "INR",
        "unit": "₹ Crore",
        "fiscal_year_end": "31st March",
        "is_bank": True,
        "current_price": 795.0,
        "shares_count": 892.4,
        "financials": {
            "period": "FY24",
            "is_bank": True,
            "revenue_current": 159876.0,
            "nii_current": 159876.0,
            "nii_prior": 144841.0,
            "total_income": 224850.0,
            "pat_current": 61077.0,
            "pat_prior": 50232.0,
            "advances_current": 3767793.0, # ₹ 37.6 Lakh Cr
            "advances_prior": 3269242.0,
            "deposits_current": 4916077.0, # ₹ 49.1 Lakh Cr
            "deposits_prior": 4423778.0,
            "net_worth": 378410.0,
            "total_assets": 6179420.0,
            "gnpa_current": 2.24,
            "nnpa_current": 0.57,
            "pcr_ratio": 75.8,
            "nim_percent": 3.28,
            "casa_ratio": 41.1,
            "crar_ratio": 14.28,
            "cost_to_income": 52.8
        },
        "evidence": [
            {
                "id": "S1",
                "source_title": "SBI Annual Report FY24",
                "doc_type": "Annual Report",
                "period": "FY24",
                "page_number": 92,
                "table_cell": "Key Performance Indicators",
                "content": "State Bank of India recorded historic Net Profit of ₹ 61,077 crore, marking a 21.6% YoY expansion driven by loan growth across corporate, SME, and home loan portfolios."
            },
            {
                "id": "S2",
                "source_title": "SBI Analyst Meet Presentation",
                "doc_type": "Investor Presentation",
                "period": "FY24",
                "page_number": 45,
                "table_cell": "Asset Quality Trajectory",
                "content": "Gross NPA dropped to a decade-low of 2.24% with credit costs moderating to 0.29% on disciplined underwriting via the YONO digital platform."
            }
        ]
    },
    {
        "ticker": "AXISBANK.NS",
        "clean_symbol": "AXISBANK",
        "name": "Axis Bank Limited",
        "sector": "Financial Services",
        "industry": "Private Sector Banking",
        "currency": "INR",
        "unit": "₹ Crore",
        "fiscal_year_end": "31st March",
        "is_bank": True,
        "current_price": 1180.0,
        "shares_count": 308.8,
        "financials": {
            "period": "FY24",
            "is_bank": True,
            "revenue_current": 49894.0,
            "nii_current": 49894.0,
            "nii_prior": 42946.0,
            "total_income": 69820.0,
            "pat_current": 24861.0,
            "pat_prior": 9580.0,
            "advances_current": 965068.0,
            "advances_prior": 845303.0,
            "deposits_current": 1068644.0,
            "deposits_prior": 946945.0,
            "net_worth": 146430.0,
            "total_assets": 1477209.0,
            "gnpa_current": 1.43,
            "nnpa_current": 0.31,
            "pcr_ratio": 78.5,
            "nim_percent": 4.06,
            "casa_ratio": 43.1,
            "crar_ratio": 16.63,
            "cost_to_income": 48.1
        },
        "evidence": [
            {
                "id": "S1",
                "source_title": "Axis Bank Annual Report FY24",
                "doc_type": "Annual Report",
                "period": "FY24",
                "page_number": 68,
                "table_cell": "Financial Highlights",
                "content": "Net profit for FY24 escalated to ₹ 24,861 crore post full integration of Citibank consumer business, with Net NPA contained at 0.31%."
            }
        ]
    },
    {
        "ticker": "KOTAKBANK.NS",
        "clean_symbol": "KOTAKBANK",
        "name": "Kotak Mahindra Bank Limited",
        "sector": "Financial Services",
        "industry": "Private Sector Banking",
        "currency": "INR",
        "unit": "₹ Crore",
        "fiscal_year_end": "31st March",
        "is_bank": True,
        "current_price": 1780.0,
        "shares_count": 198.8,
        "financials": {
            "period": "FY24",
            "is_bank": True,
            "revenue_current": 25992.0,
            "nii_current": 25992.0,
            "nii_prior": 21552.0,
            "total_income": 36840.0,
            "pat_current": 13782.0,
            "pat_prior": 10939.0,
            "advances_current": 391729.0,
            "advances_prior": 319861.0,
            "deposits_current": 444391.0,
            "deposits_prior": 363096.0,
            "net_worth": 97840.0,
            "total_assets": 586400.0,
            "gnpa_current": 1.39,
            "nnpa_current": 0.34,
            "pcr_ratio": 76.0,
            "nim_percent": 5.22,
            "casa_ratio": 45.5,
            "crar_ratio": 20.5,
            "cost_to_income": 47.4
        },
        "evidence": [
            {
                "id": "S1",
                "source_title": "Kotak Mahindra Bank FY24 Disclosures",
                "doc_type": "Annual Report",
                "period": "FY24",
                "page_number": 80,
                "table_cell": "Capital and Asset Quality",
                "content": "Capital Adequacy Ratio (CRAR) remained at an exceptional 20.5% with Net Interest Margin at 5.22% and CASA ratio of 45.5%."
            }
        ]
    },

    # ========================================================
    # TOP INDIAN CONGLOMERATES & CORPORATES
    # ========================================================
    {
        "ticker": "RELIANCE.NS",
        "clean_symbol": "RELIANCE",
        "name": "Reliance Industries Limited",
        "sector": "Energy & Digital Services",
        "industry": "Oil to Chemicals, Retail, Telecom",
        "currency": "INR",
        "unit": "₹ Crore",
        "fiscal_year_end": "31st March",
        "current_price": 1285.50,
        "shares_count": 676.5,
        "financials": {
            "period": "FY24",
            "revenue_current": 901064.0,
            "revenue_prior": 879468.0,
            "revenue_3yr_ago": 486454.0,
            "ebitda_current": 178677.0,
            "ebitda_prior": 154691.0,
            "pat_current": 79020.0,
            "pat_prior": 73670.0,
            "total_debt": 324622.0,
            "cash_and_equivalents": 208341.0,
            "net_worth": 792751.0,
            "ebit_current": 128500.0,
            "interest_expense": 23293.0,
            "operating_cash_flow": 156372.0,
            "capital_expenditures": 131769.0,
            "trade_receivables": 25680.0,
            "inventory": 139870.0,
            "trade_payables": 118450.0
        },
        "evidence": [
            {
                "id": "S1",
                "source_title": "Reliance Industries Annual Report FY24",
                "doc_type": "Annual Report",
                "period": "FY24",
                "page_number": 142,
                "table_cell": "Consolidated Financial Performance Table 1",
                "content": "Consolidated gross turnover from operations reached ₹ 9,01,064 crore ($108.0 billion) for FY 2023-24, reflecting resilient consumer facing businesses and integrated energy operations."
            },
            {
                "id": "S2",
                "source_title": "Reliance Q4 FY24 Investor Presentation",
                "doc_type": "Investor Presentation",
                "period": "Q4FY24",
                "page_number": 28,
                "table_cell": "Jio & Retail Segment Highlights",
                "content": "Digital Services EBITDA grew 12.8% YoY driven by subscriber additions of 42.4 million and continuous 5G deployment across Pan-India."
            },
            {
                "id": "S3",
                "source_title": "Reliance FY24 Audited Financial Statements",
                "doc_type": "Audited Filing",
                "period": "FY24",
                "page_number": 298,
                "table_cell": "Balance Sheet Note 18",
                "content": "Consolidated net debt stood at ₹ 1,16,281 crore, supported by cash and cash equivalents of ₹ 2,08,341 crore and strong operating cash flows."
            }
        ]
    },
    {
        "ticker": "TCS.NS",
        "clean_symbol": "TCS",
        "name": "Tata Consultancy Services Limited",
        "sector": "Information Technology",
        "industry": "IT Consulting & Software",
        "currency": "INR",
        "unit": "₹ Crore",
        "fiscal_year_end": "31st March",
        "current_price": 4120.0,
        "shares_count": 361.8,
        "financials": {
            "period": "FY24",
            "revenue_current": 240893.0,
            "revenue_prior": 225458.0,
            "revenue_3yr_ago": 164177.0,
            "ebitda_current": 64278.0,
            "ebitda_prior": 59259.0,
            "pat_current": 46099.0,
            "pat_prior": 42303.0,
            "total_debt": 7774.0,
            "cash_and_equivalents": 46973.0,
            "net_worth": 90544.0,
            "ebit_current": 59344.0,
            "interest_expense": 779.0,
            "operating_cash_flow": 44342.0,
            "capital_expenditures": 3120.0,
            "trade_receivables": 44520.0,
            "inventory": 0.0,
            "trade_payables": 11340.0
        },
        "evidence": [
            {
                "id": "S1",
                "source_title": "TCS Annual Report FY24",
                "doc_type": "Annual Report",
                "period": "FY24",
                "page_number": 88,
                "table_cell": "Consolidated Statement of Profit and Loss",
                "content": "Revenue from operations crossed ₹ 2,40,893 crore, marking a 6.8% YoY reported growth driven by cloud transformation and generative AI deal wins."
            },
            {
                "id": "S2",
                "source_title": "TCS Audited Balance Sheet Note 14",
                "doc_type": "Audited Filing",
                "period": "FY24",
                "page_number": 210,
                "table_cell": "Cash and Liquid Investments",
                "content": "The company remains virtually debt-free with cash and investments of ₹ 46,973 crore and return on equity of 51%."
            }
        ]
    },
    {
        "ticker": "INFY.NS",
        "clean_symbol": "INFY",
        "name": "Infosys Limited",
        "sector": "Information Technology",
        "industry": "IT Software & Consulting",
        "currency": "INR",
        "unit": "₹ Crore",
        "fiscal_year_end": "31st March",
        "current_price": 1860.0,
        "shares_count": 415.0,
        "financials": {
            "period": "FY24",
            "revenue_current": 153670.0,
            "revenue_prior": 146767.0,
            "revenue_3yr_ago": 100472.0,
            "ebitda_current": 37210.0,
            "ebitda_prior": 35131.0,
            "pat_current": 26248.0,
            "pat_prior": 24108.0,
            "total_debt": 8420.0,
            "cash_and_equivalents": 38240.0,
            "net_worth": 86240.0,
            "ebit_current": 33810.0,
            "interest_expense": 490.0,
            "operating_cash_flow": 28140.0,
            "capital_expenditures": 2980.0,
            "trade_receivables": 31200.0,
            "inventory": 0.0,
            "trade_payables": 8450.0
        },
        "evidence": [
            {
                "id": "S1",
                "source_title": "Infosys Annual Report FY24",
                "doc_type": "Annual Report",
                "period": "FY24",
                "page_number": 102,
                "table_cell": "Segment Performance",
                "content": "Consolidated revenues reached ₹ 1,53,670 crore, supported by large deal total contract value of $17.7 billion and operating margins at 21.1%."
            }
        ]
    },
    {
        "ticker": "TATAMOTORS.NS",
        "clean_symbol": "TATAMOTORS",
        "name": "Tata Motors Limited",
        "sector": "Automobile",
        "industry": "Commercial & Passenger Vehicles, EV, JLR",
        "currency": "INR",
        "unit": "₹ Crore",
        "fiscal_year_end": "31st March",
        "current_price": 910.0,
        "shares_count": 368.5,
        "financials": {
            "period": "FY24",
            "revenue_current": 437928.0,
            "revenue_prior": 345967.0,
            "revenue_3yr_ago": 249795.0,
            "ebitda_current": 62800.0,
            "ebitda_prior": 37011.0,
            "pat_current": 31807.0,
            "pat_prior": 2690.0,
            "total_debt": 91800.0,
            "cash_and_equivalents": 48200.0,
            "net_worth": 84720.0,
            "ebit_current": 42100.0,
            "interest_expense": 9540.0,
            "operating_cash_flow": 52400.0,
            "capital_expenditures": 32100.0,
            "trade_receivables": 21800.0,
            "inventory": 48900.0,
            "trade_payables": 78200.0
        },
        "evidence": [
            {
                "id": "S1",
                "source_title": "Tata Motors Annual Report FY24",
                "doc_type": "Annual Report",
                "period": "FY24",
                "page_number": 84,
                "table_cell": "Consolidated Results",
                "content": "Tata Motors achieved record consolidated revenue of ₹ 4,37,928 crore, propelled by Jaguar Land Rover (JLR) turnaround and leadership in India EV market."
            }
        ]
    },
    {
        "ticker": "ITC.NS",
        "clean_symbol": "ITC",
        "name": "ITC Limited",
        "sector": "Consumer Goods",
        "industry": "FMCG, Cigarettes, Paperboards, Hotels, Agri",
        "currency": "INR",
        "unit": "₹ Crore",
        "fiscal_year_end": "31st March",
        "current_price": 480.0,
        "shares_count": 1248.0,
        "financials": {
            "period": "FY24",
            "revenue_current": 76840.0,
            "revenue_prior": 70937.0,
            "revenue_3yr_ago": 53155.0,
            "ebitda_current": 26210.0,
            "ebitda_prior": 24670.0,
            "pat_current": 20750.0,
            "pat_prior": 19477.0,
            "total_debt": 310.0,
            "cash_and_equivalents": 19400.0,
            "net_worth": 71420.0,
            "ebit_current": 24800.0,
            "interest_expense": 45.0,
            "operating_cash_flow": 18200.0,
            "capital_expenditures": 2900.0,
            "trade_receivables": 3100.0,
            "inventory": 13800.0,
            "trade_payables": 5100.0
        },
        "evidence": [
            {
                "id": "S1",
                "source_title": "ITC Annual Report FY24",
                "doc_type": "Annual Report",
                "period": "FY24",
                "page_number": 112,
                "table_cell": "Segment Review",
                "content": "Gross revenue from operations stood at ₹ 76,840 crore, with FMCG-Others revenue crossing ₹ 20,000 crore and operating cash flow at ₹ 18,200 crore."
            }
        ]
    },
    {
        "ticker": "LT.NS",
        "clean_symbol": "LT",
        "name": "Larsen & Toubro Limited",
        "sector": "Capital Goods",
        "industry": "EPC Infrastructure, Heavy Engineering, Defense",
        "currency": "INR",
        "unit": "₹ Crore",
        "fiscal_year_end": "31st March",
        "current_price": 3650.0,
        "shares_count": 137.5,
        "financials": {
            "period": "FY24",
            "revenue_current": 221113.0,
            "revenue_prior": 183341.0,
            "revenue_3yr_ago": 135979.0,
            "ebitda_current": 23640.0,
            "ebitda_prior": 20753.0,
            "pat_current": 15540.0,
            "pat_prior": 12625.0,
            "total_debt": 118400.0,
            "cash_and_equivalents": 34100.0,
            "net_worth": 92400.0,
            "ebit_current": 19800.0,
            "interest_expense": 3400.0,
            "operating_cash_flow": 19400.0,
            "capital_expenditures": 6200.0,
            "trade_receivables": 68400.0,
            "inventory": 8200.0,
            "trade_payables": 59100.0
        },
        "evidence": [
            {
                "id": "S1",
                "source_title": "Larsen & Toubro Annual Report FY24",
                "doc_type": "Annual Report",
                "period": "FY24",
                "page_number": 140,
                "table_cell": "Consolidated Order Book",
                "content": "L&T consolidated order book stood at an unprecedented ₹ 4,75,809 crore with international orders constituting 38% of total order inflow."
            }
        ]
    },
    {
        "ticker": "BHARTIARTL.NS",
        "clean_symbol": "BHARTIARTL",
        "name": "Bharti Airtel Limited",
        "sector": "Telecommunications",
        "industry": "Mobile, Broadband, Enterprise Digital Infrastructure",
        "currency": "INR",
        "unit": "₹ Crore",
        "fiscal_year_end": "31st March",
        "current_price": 1690.0,
        "shares_count": 570.0,
        "financials": {
            "period": "FY24",
            "revenue_current": 149982.0,
            "revenue_prior": 139145.0,
            "revenue_3yr_ago": 100616.0,
            "ebitda_current": 79250.0,
            "ebitda_prior": 71274.0,
            "pat_current": 10540.0,
            "pat_prior": 8346.0,
            "total_debt": 208400.0,
            "cash_and_equivalents": 18400.0,
            "net_worth": 88400.0,
            "ebit_current": 38400.0,
            "interest_expense": 18200.0,
            "operating_cash_flow": 64200.0,
            "capital_expenditures": 33400.0,
            "trade_receivables": 6800.0,
            "inventory": 210.0,
            "trade_payables": 38400.0
        },
        "evidence": [
            {
                "id": "S1",
                "source_title": "Bharti Airtel Annual Report FY24",
                "doc_type": "Annual Report",
                "period": "FY24",
                "page_number": 98,
                "table_cell": "Operational Metrics",
                "content": "India mobile Average Revenue Per User (ARPU) climbed to an industry-leading ₹ 209 per month with EBITDA margin at 52.8%."
            }
        ]
    }
]
