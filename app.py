import streamlit as st
import pandas as pd

st.title("My Sales Dashboard")

# ------------------------------
# Step 1: Load CSV safely
# ------------------------------
csv_path = r"C:\Users\HP\Downloads\Data_Visualization_Project\data.csv"

try:
    data = pd.read_csv("data_small.csv", encoding='cp1252')
except UnicodeDecodeError:
    st.error("Failed to read CSV. Try another encoding like 'latin1'.")
    st.stop()
except FileNotFoundError:
    st.error(f"CSV file not found at {csv_path}. Make sure it exists.")
    st.stop()

# ------------------------------
# Step 2: Preview and show columns
# ------------------------------
st.subheader("Columns in dataset")
st.write(data.columns.tolist())

st.subheader("Dataset Preview")
st.dataframe(data.head())

# ------------------------------
# Step 3: Identify numeric, categorical, and datetime columns
# ------------------------------
numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
datetime_cols = data.select_dtypes(include=['datetime64', 'object']).columns.tolist()

# Try to parse date columns automatically
for col in datetime_cols:
    try:
        data[col] = pd.to_datetime(data[col])
    except:
        pass

# ------------------------------
# Step 4: Filter data interactively
# ------------------------------
st.subheader("Filter Data")
filters = {}
for col in categorical_cols:
    options = ["All"] + data[col].dropna().unique().tolist()
    selected = st.selectbox(f"Select {col}", options, key=col)
    if selected != "All":
        filters[col] = selected

filtered_data = data.copy()
for col, val in filters.items():
    filtered_data = filtered_data[filtered_data[col] == val]

st.subheader("Filtered Dataset Preview")
st.dataframe(filtered_data.head())

# ------------------------------
# Step 5: First Chart - Bar chart by categorical column
# ------------------------------
st.subheader("Bar Chart")

if categorical_cols and numeric_cols:
    category_col = st.selectbox("Categorical Column (X-axis)", categorical_cols, key="bar_cat")
    value_col = st.selectbox("Numeric Column (Y-axis)", numeric_cols, key="bar_num")

    chart_data = filtered_data.groupby(category_col)[value_col].sum()
    st.bar_chart(chart_data)

    if not chart_data.empty:
        max_val = chart_data.idxmax()
        st.write(f"Insight: The {category_col} with the highest {value_col} is **{max_val}**.")

# ------------------------------
# Step 6: Second Chart - Line chart by datetime column
# ------------------------------
st.subheader("Line Chart Over Time")

if datetime_cols and numeric_cols:
    date_col = st.selectbox("Datetime Column (X-axis)", datetime_cols, key="line_date")
    value_col2 = st.selectbox("Numeric Column (Y-axis)", numeric_cols, key="line_num")

    try:
        line_data = filtered_data.groupby(date_col)[value_col2].sum().sort_index()
        st.line_chart(line_data)
        if not line_data.empty:
            max_date = line_data.idxmax().strftime("%Y-%m-%d")
            st.write(f"Insight: The highest {value_col2} occurred on **{max_date}**.")
    except:

        st.warning("Could not create line chart. Make sure the selected column is a date or numeric type.")
