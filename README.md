# 📊 Revenue Analytics Dashboard

A desktop application for advanced revenue analysis and market insights, built using Python.
The dashboard enables interactive exploration of sales data, identification of key markets, and tracking of performance trends over time.

---

## 🚀 Key Features

* 📈 Interactive revenue visualization (bar & donut charts)
* 🌍 Market segmentation and distribution analysis
* 🏆 Identification of top-performing markets
* 📊 Multi-period trend analysis across months
* 📂 Excel-based data ingestion
* 📉 Product-level performance breakdown
* 🔍 Automated market expansion & contraction insights
* 💡 Data-driven recommendations for revenue optimization

---

## 🛠️ Technology Stack

* **Python**
* **Tkinter** — desktop GUI framework
* **Matplotlib** — data visualization
* **Pandas** — data processing and aggregation
* **mplcursors** — interactive chart exploration

---

## 📊 Data Model (Excel Input)

The application is designed to work with structured Excel datasets.

### Required Fields:

* `Country`
* `Revenue`

### Extended Schema (Recommended):

| Field         | Description                          |
| ------------- | ------------------------------------ |
| Date          | Time dimension for trend analysis    |
| Product       | Enables product-level insights       |
| Quantity      | Sales volume                         |
| Price         | Unit price                           |
| Revenue       | Total transaction value              |
| Channels      | Sales channel (Online, Retail, etc.) |
| Customer type | B2B / B2C segmentation               |

---

## 🧠 Analytical Capabilities

* **Revenue Aggregation:** Consolidates data across countries and time periods
* **Trend Detection:** Identifies growth patterns and performance shifts
* **Top Market Analysis:** Highlights highest revenue-generating regions
* **Product Insights:** Determines best-performing products per market
* **Market Change Detection:** Tracks entry and exit of markets over time
* **Recommendation Engine:** Suggests focus areas based on top-performing products

---

## ⚠️ Considerations

* Input data must follow the defined schema for full functionality
* Time-series analysis depends on properly formatted date fields
* Performance may vary with very large datasets

---

## 📌 Future Enhancements

* Integration with relational databases (PostgreSQL / MySQL)
* Automated data pipeline (ETL processing)
* Exportable analytical reports (PDF / Excel summaries)
* Advanced forecasting (time-series models)
* Role-based data access and multi-user support
* API layer for integration with external systems

---

## 👤 Author

Adin
