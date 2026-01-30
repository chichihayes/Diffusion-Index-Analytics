import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Unified mapping for transformations
unified_mapping = {
    "Higher": 1,
    "Lower": 3,
    "Same": 2,
    "Faster": 1,
    "Slower": 3
}

# Streamlit App
st.set_page_config(page_title="PMI Calculator", page_icon=":bar_chart:", layout="wide")

# Dark theme setup
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #2c2c2c;
    }
    .sidebar .sidebar-content {
        background-color: #1f1f1f;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
    }
    .stSlider>div>div {
        background-color: #1f1f1f;
    }
    .stSelectbox>div>div {
        background-color: #1f1f1f;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Purchasing Managers' Index (PMI) Calculator")

# File Upload
uploaded_file = st.file_uploader("Upload your PMI Excel file", type=["xlsx"])
if uploaded_file:
    # Load the dataset
    st.write("### Step 1: Load and View Dataset")
    df = pd.read_excel(uploaded_file, sheet_name=None)
    sheet_names = list(df.keys())
    sheet_name = st.selectbox("Select the sheet to analyze", sheet_names)
    df = df[sheet_name]
    st.write("Dataset Preview:")
    st.dataframe(df)

    # Column Selection and Weights
    st.write("### Step 2: Configure Columns and Weights")
    columns_to_transform = st.multiselect(
        "Select columns to transform",
        df.columns.tolist(),
        help="Choose the columns for PMI calculation based on their importance."
    )
    weights = {}
    for column in columns_to_transform:
        weight = st.slider(f"Weight for {column}:", 0.0, 1.0, 0.1, 0.05)
        weights[column] = weight

    # Filter Column
    filter_column = st.selectbox(
        "Select the filter column (e.g., sector):",
        df.columns,
        help="This column will be used to group data for sector-wise analysis."
    )

    if st.button("Calculate PMI"):
        # Unified transformation of selected columns
        for column in columns_to_transform:
            if column in df.columns:
                df[column] = df[column].astype(str).str.strip()  # Clean string data
                df[column] = df[column].map(unified_mapping)  # Apply mapping
            else:
                st.warning(f"Warning: Column '{column}' is missing in the dataset and was skipped.")

        # Get unique sectors
        if filter_column in df.columns:
            sectors = df[filter_column].dropna().unique()

            # Initialize dictionaries to store results
            sector_pmi = {}
            overall_pmi = {}
            column_details = {}
            
            # Create a dictionary to store composite data
            composite_counts = {}
            for column in columns_to_transform:
                composite_counts[column] = {1: 0, 2: 0, 3: 0}  # Keys: 1=Higher, 2=Same, 3=Lower
            
            # Perform sector-wise analysis and PMI calculation
            for sector in sectors:
                sector_data = df[df[filter_column] == sector]
                total_pmi = 0.0
                sector_details = {}

                for column, weight in weights.items():
                    if column in sector_data.columns:
                        # Count values for individual sector analysis
                        counts = sector_data[column].value_counts().sort_index()
                        total = counts.sum()
                        
                        # Calculate percentages
                        percentages = {}
                        for val in [1, 2, 3]:  # Higher, Same, Lower
                            if val in counts.index:
                                percentages[val] = (counts[val] / total * 100).round(2)
                            else:
                                percentages[val] = 0.0
                        
                        # CORRECTED PMI formula: Higher% + (0.5 * Higher%)
                        higher_pct = percentages.get(1, 0.0)
                        column_pmi = higher_pct + (0.5 * higher_pct)
                        
                        # Weighted PMI
                        weighted_pmi = column_pmi * weight
                        total_pmi += weighted_pmi
                        
                        # Store details for this column in this sector
                        sector_details[column] = {
                            "Higher%": higher_pct,
                            "Same%": percentages.get(2, 0.0),
                            "Lower%": percentages.get(3, 0.0),
                            "Column PMI": round(column_pmi, 2),
                            "Weighted Contribution": round(weighted_pmi, 2)
                        }
                        
                        # Accumulate counts for composite calculation
                        for val in [1, 2, 3]:  # Higher, Same, Lower
                            if val in counts.index:
                                composite_counts[column][val] += counts[val]

                # Save results
                overall_pmi[sector] = round(total_pmi, 2)
                column_details[sector] = sector_details
            
            # Calculate Composite PMI
            composite_pmi = 0.0
            composite_results = {}
            
            for column, weight in weights.items():
                column_total = sum(composite_counts[column].values())
                
                # Calculate percentages
                higher_count = composite_counts[column].get(1, 0)
                higher_pct = (higher_count / column_total * 100) if column_total > 0 else 0
                same_count = composite_counts[column].get(2, 0)
                same_pct = (same_count / column_total * 100) if column_total > 0 else 0
                lower_count = composite_counts[column].get(3, 0)
                lower_pct = (lower_count / column_total * 100) if column_total > 0 else 0
                
                # CORRECTED PMI calculation: Higher% + (0.5 * Higher%)
                column_pmi = higher_pct + (0.5 * higher_pct)
                
                # Weighted contribution to composite PMI
                weighted_column_pmi = column_pmi * weight
                composite_pmi += weighted_column_pmi
                
                # Store detailed results for this column
                composite_results[column] = {
                    "Higher%": round(higher_pct, 2),
                    "Same%": round(same_pct, 2),
                    "Lower%": round(lower_pct, 2),
                    "Column PMI": round(column_pmi, 2),
                    "Weighted Contribution": round(weighted_column_pmi, 2)
                }
            
            # Round the final composite PMI
            composite_pmi = round(composite_pmi, 2)

            # Display Results (Only sector name and overall PMI)
            st.write("### Results: PMI Analysis")
            for sector, pmi in overall_pmi.items():
                st.write(f"#### Sector: {sector} - Overall PMI: {pmi}")
                
                # Display detailed breakdown for this sector
                st.write(f"Detailed breakdown for {sector}:")
                sector_df = pd.DataFrame(column_details[sector]).T
                sector_df.index.name = "Column"
                st.dataframe(sector_df)
            
            # Display Composite PMI Section
            st.write("### Composite PMI Analysis")
            st.write(f"#### Overall Composite PMI: {composite_pmi}")
            
            # Display detailed composite breakdown
            st.write("#### Composite Breakdown by Column:")
            composite_df = pd.DataFrame(composite_results).T
            composite_df.index.name = "Column"
            st.dataframe(composite_df)

            # Create a bar plot for overall PMI by sector in descending order
            sector_names = list(overall_pmi.keys())
            pmi_values = list(overall_pmi.values())

            # Sort results by overall PMI
            sorted_sectors = [x for _, x in sorted(zip(pmi_values, sector_names), reverse=True)]
            sorted_pmi = sorted(pmi_values, reverse=True)

            plt.figure(figsize=(10, 6))
            plt.barh(sorted_sectors, sorted_pmi, color='blue')
            plt.xlabel('Overall PMI')
            plt.ylabel('Sector')
            plt.title('PMI by Sector (Descending Order)')
            plt.gca().invert_yaxis()  # To display the highest PMI at the top
            plt.tight_layout()

            # Display the plot
            st.pyplot(plt)
            
            # Create a separate bar showing composite alongside sectors
            all_names = sorted_sectors + ["COMPOSITE"]
            all_pmi = sorted_pmi + [composite_pmi]
            
            colors = ['blue'] * len(sorted_sectors) + ['red']
            
            plt.figure(figsize=(10, 6))
            plt.barh(all_names, all_pmi, color=colors)
            plt.xlabel('PMI Value')
            plt.ylabel('Sector/Composite')
            plt.title('PMI by Sector with Composite')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            
            # Display the second plot
            st.pyplot(plt)

            # Save results to Excel
            output = pd.ExcelWriter("transformed_pmi_results.xlsx", engine='openpyxl')
            
            # Save transformed data
            df.to_excel(output, sheet_name="Transformed Data", index=False)
            
            # Save sector PMI values
            pd.Series(overall_pmi, name="PMI").to_excel(output, sheet_name="Sector PMI")
            
            # Save sector details
            for sector in sectors:
                sector_df = pd.DataFrame(column_details[sector]).T
                sector_df.to_excel(output, sheet_name=f"{sector[:31]}")  # Excel sheet name limit
            
            # Save composite results
            composite_df.to_excel(output, sheet_name="Composite PMI")
            
            output.close()
            
            st.download_button(
                label="Download Complete PMI Results",
                data=open("transformed_pmi_results.xlsx", "rb").read(),
                file_name="transformed_pmi_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error(f"The filter column '{filter_column}' is not found in the dataset!")
