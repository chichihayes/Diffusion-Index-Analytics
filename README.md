# PMI Calculator 📊

A web-based **Purchasing Managers' Index (PMI) Calculator** built with **Python** and **Streamlit** for analyzing survey-based economic and business activity data.

The application allows users to upload Excel datasets, configure weighted indicators, calculate sector-wise PMI values, generate composite PMI results, visualize the data, and export all results into an Excel workbook.

---

# Features

- Upload Excel (`.xlsx`) datasets
- Dynamic worksheet selection
- Select indicator columns for PMI analysis
- Assign custom weights to indicators
- Sector-wise PMI calculation
- Composite PMI analysis
- Interactive tables and visualizations
- Export results to Excel
- Dark-themed Streamlit interface

---

# Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- OpenPyXL

---

# Installation

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <repository-folder>
```

---

## 2. Create a Virtual Environment (Optional)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

Create a `requirements.txt` file containing:

```txt
streamlit
pandas
matplotlib
numpy
openpyxl
```

---

# Running the Application

Run the Streamlit app:

```bash
streamlit run app.py
```

Replace `app.py` with your actual filename if different.

---

# Input Dataset Format

The uploaded Excel file should contain:

- One or more worksheets
- Survey response columns
- A grouping/filter column (e.g., sector)

Example:

| Sector | New Orders | Production | Employment |
|--------|------------|------------|------------|
| Manufacturing | Higher | Same | Lower |
| Services | Higher | Higher | Same |

---

# Response Mapping

The application converts survey responses into numerical values using the following mapping:

| Response | Value |
|----------|------|
| Higher | 1 |
| Same | 2 |
| Lower | 3 |
| Faster | 1 |
| Slower | 3 |

---

# PMI Calculation Logic

For each selected indicator:

1. Count response frequencies
2. Calculate percentages
3. Compute PMI using:

```text
PMI = Higher% + (0.5 × Higher%)
```

4. Apply assigned weights:

```text
Weighted PMI = Column PMI × Weight
```

5. Sum weighted contributions to obtain:
- Sector PMI
- Composite PMI

---

# Workflow

## Step 1 — Upload Dataset
Upload an Excel workbook (`.xlsx`).

## Step 2 — Select Worksheet
Choose the worksheet to analyze.

## Step 3 — Configure Indicators
- Select columns for PMI calculation
- Assign weights using sliders

## Step 4 — Select Filter Column
Choose the grouping column (e.g., sector).

## Step 5 — Calculate PMI
The app:
- Cleans the data
- Applies mappings
- Computes sector PMI
- Computes composite PMI
- Generates tables and charts

## Step 6 — Download Results
Export all processed results into Excel format.

---

# Generated Outputs

The application produces:

## Sector PMI Table
Displays:
- Higher %
- Same %
- Lower %
- Column PMI
- Weighted Contribution

## Composite PMI Table
Aggregated analysis across all sectors.

## Charts
- PMI by sector
- Composite PMI comparison

## Excel Export
Generated file includes:
- Transformed dataset
- Sector PMI sheets
- Composite PMI sheet

---

# File Structure

```bash
project-folder/
│
├── app.py
├── requirements.txt
├── README.md
└── transformed_pmi_results.xlsx
```

---

# Example Use Cases

- Manufacturing PMI analysis
- Supply chain monitoring
- Business confidence surveys
- Economic trend analysis
- Corporate performance tracking
- Sector comparison studies

---

# Known Limitation

The implemented PMI formula currently uses:

```text
PMI = Higher% + (0.5 × Higher%)
```

Traditional PMI methodology typically uses:

```text
PMI = Higher% + (0.5 × Same%)
```

You may modify the formula depending on your analytical methodology.

---

# Future Improvements

Potential enhancements include:

- Real PMI formula implementation
- Time-series PMI tracking
- Dashboard KPIs
- Forecasting models
- PDF report generation
- Interactive filtering
- Database integration
- Machine learning predictions

---

# License

This project is open-source and available for educational, research, and commercial use.

---


- Streamlit
- Pandas
- Matplotlib
