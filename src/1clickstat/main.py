import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="1ClickStat",
    page_icon="📊",
    layout="wide"
)


# =========================================
# SESSION STATE
# =========================================

if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = None

if "active_filter_column" not in st.session_state:
    st.session_state.active_filter_column = None

if "active_filter_values" not in st.session_state:
    st.session_state.active_filter_values = []


# =========================================
# HELPER FUNCTION
# =========================================

def load_data(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    elif file_name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)

    elif file_name.endswith(".json"):
        return pd.read_json(uploaded_file)

    else:
        return None


# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.title("📊 1ClickStat")

    st.write("Business Data Analysis Tool")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "📄 Dataset Preview",
            "🔎 Filter Data",
            "📌 Dataset Overview",
            "⚠️ Data Quality",
            "🔍 Column Information",
            "📈 Numerical Statistics",
            "💼 Business Analysis",
            "🔗 Correlation Analysis",
            "📊 Visualizations",
            "📊 Group Analysis"
        ]
    )

    st.divider()

    st.caption("Upload → Filter → Analyze")


# =========================================
# MAIN TITLE
# =========================================

st.title("📊 1ClickStat")

st.write(
    "Upload your dataset and get useful business insights in one place."
)


# =========================================
# FILE UPLOAD
# =========================================

uploaded_file = st.file_uploader(
    "📁 Upload your dataset",
    type=["csv", "xlsx", "json"]
)


# =========================================
# NO FILE
# =========================================

if uploaded_file is None:

    st.info("👆 Upload a CSV, Excel, or JSON file to get started.")

    st.stop()


# =========================================
# LOAD DATA
# =========================================

try:

    df = load_data(uploaded_file)

    if df is None:
        st.error("Unsupported file format.")
        st.stop()

except Exception as e:

    st.error(f"Error loading file: {e}")

    st.stop()


# =========================================
# GET FILTERED DATA
# =========================================

if st.session_state.filtered_df is not None:

    data = st.session_state.filtered_df

else:

    data = df.copy()


# =========================================
# HOME
# =========================================

if page == "🏠 Home":

    st.success("Dataset loaded successfully! 🎉")

    st.subheader("Welcome to 1ClickStat")

    st.write(
        """
        **1ClickStat** helps you quickly explore and analyze business datasets.

        Use the sidebar to:

        - 📄 Preview your dataset
        - 🔎 Filter data
        - 📌 View dataset overview
        - ⚠️ Check data quality
        - 📈 Analyze numerical statistics
        - 💼 Perform business calculations
        - 🔗 Find correlations
        - 📊 Generate automatic visualizations
        - 📦 Analyze data using groups
        """
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Rows", len(df))

    col2.metric("Total Columns", len(df.columns))

    col3.metric(
        "Current Rows",
        len(data)
    )


# =========================================
# DATASET PREVIEW
# =========================================

elif page == "📄 Dataset Preview":

    st.header("📄 Dataset Preview")

    st.write(
        f"Showing **{len(data)} rows** and "
        f"**{len(data.columns)} columns**"
    )

    st.dataframe(
        data,
        use_container_width=True,
        height=500
    )


# =========================================
# FILTER DATA
# =========================================

elif page == "🔎 Filter Data":

    st.header("🔎 Filter Data")

    st.write(
        "Select a column and choose values to filter your dataset."
    )

    filter_column = st.selectbox(
        "Select Column",
        df.columns
    )

    unique_values = (
        df[filter_column]
        .dropna()
        .unique()
        .tolist()
    )

    selected_values = st.multiselect(
        "Select Value(s)",
        unique_values
    )


    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "✅ Apply Filter",
            use_container_width=True
        ):

            if selected_values:

                filtered_df = df[
                    df[filter_column].isin(selected_values)
                ].copy()

            else:

                filtered_df = df.copy()


            st.session_state.filtered_df = filtered_df

            st.session_state.active_filter_column = filter_column

            st.session_state.active_filter_values = selected_values

            st.success("Filter applied successfully!")


    with col2:

        if st.button(
            "🔄 Clear Filter",
            use_container_width=True
        ):

            st.session_state.filtered_df = None

            st.session_state.active_filter_column = None

            st.session_state.active_filter_values = []

            st.success("Filter cleared!")


    st.divider()


    # Get current filtered data again

    if st.session_state.filtered_df is not None:

        filtered_data = st.session_state.filtered_df

        st.subheader("📄 Filtered Data Preview")

        if st.session_state.active_filter_values:

            st.write(
                f"Filtered by **{st.session_state.active_filter_column}**"
            )

        st.metric(
            "Rows After Filtering",
            len(filtered_data)
        )

        st.dataframe(
            filtered_data,
            use_container_width=True,
            height=500
        )

    else:

        st.subheader("📄 Current Dataset")

        st.write("No filter is currently applied.")

        st.dataframe(
            df,
            use_container_width=True,
            height=500
        )


# =========================================
# DATASET OVERVIEW
# =========================================

elif page == "📌 Dataset Overview":

    st.header("📌 Dataset Overview")

    numerical_columns = data.select_dtypes(
        include="number"
    ).columns

    categorical_columns = data.select_dtypes(
        exclude="number"
    ).columns


    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Rows",
        data.shape[0]
    )

    col2.metric(
        "Columns",
        data.shape[1]
    )

    col3.metric(
        "Numerical Columns",
        len(numerical_columns)
    )

    col4.metric(
        "Other Columns",
        len(categorical_columns)
    )


    st.divider()

    st.subheader("Dataset Shape")

    st.write(
        f"**{data.shape[0]} rows × {data.shape[1]} columns**"
    )


# =========================================
# DATA QUALITY
# =========================================

elif page == "⚠️ Data Quality":

    st.header("⚠️ Data Quality")

    missing_values = data.isnull().sum().sum()

    duplicate_rows = data.duplicated().sum()


    col1, col2 = st.columns(2)

    col1.metric(
        "Missing Values",
        missing_values
    )

    col2.metric(
        "Duplicate Rows",
        duplicate_rows
    )


    st.divider()


    missing_per_column = data.isnull().sum()

    missing_per_column = missing_per_column[
        missing_per_column > 0
    ]


    if not missing_per_column.empty:

        st.subheader("Missing Values by Column")

        missing_df = missing_per_column.reset_index()

        missing_df.columns = [
            "Column",
            "Missing Values"
        ]

        st.dataframe(
            missing_df,
            use_container_width=True
        )

    else:

        st.success("🎉 No missing values found!")


# =========================================
# COLUMN INFORMATION
# =========================================

elif page == "🔍 Column Information":

    st.header("🔍 Column Information")


    column_info = pd.DataFrame({

        "Column": data.columns,

        "Data Type": data.dtypes.astype(str).values,

        "Non-Null Values": data.notnull().sum().values,

        "Unique Values": data.nunique().values

    })


    st.dataframe(
        column_info,
        use_container_width=True,
        height=500
    )


# =========================================
# NUMERICAL STATISTICS
# =========================================

elif page == "📈 Numerical Statistics":

    st.header("📈 Numerical Statistics")


    numerical_columns = data.select_dtypes(
        include="number"
    ).columns


    if len(numerical_columns) > 0:

        statistics = pd.DataFrame({

            "Count": data[numerical_columns].count(),

            "Sum": data[numerical_columns].sum(),

            "Mean": data[numerical_columns].mean(),

            "Median": data[numerical_columns].median(),

            "Minimum": data[numerical_columns].min(),

            "Maximum": data[numerical_columns].max(),

            "Standard Deviation":
                data[numerical_columns].std(),

            "Variance":
                data[numerical_columns].var()

        })


        st.dataframe(
            statistics,
            use_container_width=True,
            height=500
        )


    else:

        st.info(
            "No numerical columns found."
        )


# =========================================
# BUSINESS ANALYSIS
# =========================================

elif page == "💼 Business Analysis":

    st.header("💼 Business Analysis")

    st.write(
        "Quick calculations for sales, revenue, profit, and other business metrics."
    )


    numerical_columns = data.select_dtypes(
        include="number"
    ).columns.tolist()


    if len(numerical_columns) == 0:

        st.info("No numerical columns available.")

        st.stop()


    analysis_column = st.selectbox(
        "Select a numerical column",
        numerical_columns
    )


    series = data[analysis_column].dropna()


    # Metrics

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total",
        round(series.sum(), 2)
    )

    col2.metric(
        "Average",
        round(series.mean(), 2)
    )

    col3.metric(
        "Maximum",
        round(series.max(), 2)
    )

    col4.metric(
        "Minimum",
        round(series.min(), 2)
    )


    st.divider()


    # Max row

    st.subheader("🏆 Highest Value")

    max_index = data[analysis_column].idxmax()

    st.dataframe(
        data.loc[[max_index]],
        use_container_width=True
    )


    # Min row

    st.subheader("📉 Lowest Value")

    min_index = data[analysis_column].idxmin()

    st.dataframe(
        data.loc[[min_index]],
        use_container_width=True
    )


    # Mode

    st.subheader("Most Common Value")

    mode_values = series.mode()

    if not mode_values.empty:

        st.write(
            mode_values.tolist()
        )


# =========================================
# CORRELATION ANALYSIS
# =========================================

elif page == "🔗 Correlation Analysis":

    st.header("🔗 Correlation Analysis")


    numerical_columns = data.select_dtypes(
        include="number"
    ).columns


    if len(numerical_columns) >= 2:

        correlation = data[
            numerical_columns
        ].corr()


        st.dataframe(
            correlation,
            use_container_width=True
        )


    else:

        st.info(
            "At least 2 numerical columns are required."
        )


# =========================================
# VISUALIZATIONS
# =========================================

elif page == "📊 Visualizations":

    st.header("📊 Automatic Visualizations")


    numerical_columns = data.select_dtypes(
        include="number"
    ).columns.tolist()


    categorical_columns = data.select_dtypes(
        exclude="number"
    ).columns.tolist()


    # -----------------------------------------
    # NUMERICAL CHARTS
    # -----------------------------------------

    if len(numerical_columns) > 0:

        st.subheader("📈 Numerical Distributions")


        for i in range(
            0,
            len(numerical_columns),
            2
        ):

            col1, col2 = st.columns(2)


            # First chart

            with col1:

                column = numerical_columns[i]

                fig, ax = plt.subplots(
                    figsize=(5, 3)
                )

                ax.hist(
                    data[column].dropna(),
                    bins=20
                )

                ax.set_title(
                    f"Distribution of {column}"
                )

                ax.set_xlabel(column)

                ax.set_ylabel("Frequency")

                st.pyplot(
                    fig,
                    use_container_width=True
                )

                plt.close(fig)


            # Second chart

            if i + 1 < len(numerical_columns):

                with col2:

                    column = numerical_columns[i + 1]

                    fig, ax = plt.subplots(
                        figsize=(5, 3)
                    )

                    ax.hist(
                        data[column].dropna(),
                        bins=20
                    )

                    ax.set_title(
                        f"Distribution of {column}"
                    )

                    ax.set_xlabel(column)

                    ax.set_ylabel("Frequency")

                    st.pyplot(
                        fig,
                        use_container_width=True
                    )

                    plt.close(fig)


    # -----------------------------------------
    # CATEGORICAL CHARTS
    # -----------------------------------------

    if len(categorical_columns) > 0:

        st.subheader("📊 Categorical Distributions")


        valid_columns = [

            column

            for column in categorical_columns

            if data[column].nunique() <= 20

        ]


        for i in range(
            0,
            len(valid_columns),
            2
        ):

            col1, col2 = st.columns(2)


            # First chart

            with col1:

                column = valid_columns[i]

                value_counts = (
                    data[column]
                    .value_counts()
                )

                fig, ax = plt.subplots(
                    figsize=(5, 3)
                )

                ax.bar(
                    value_counts.index.astype(str),
                    value_counts.values
                )

                ax.set_title(
                    f"Distribution of {column}"
                )

                ax.set_xlabel(column)

                ax.set_ylabel("Count")

                plt.xticks(
                    rotation=45
                )

                st.pyplot(
                    fig,
                    use_container_width=True
                )

                plt.close(fig)


            # Second chart

            if i + 1 < len(valid_columns):

                with col2:

                    column = valid_columns[i + 1]

                    value_counts = (
                        data[column]
                        .value_counts()
                    )

                    fig, ax = plt.subplots(
                        figsize=(5, 3)
                    )

                    ax.bar(
                        value_counts.index.astype(str),
                        value_counts.values
                    )

                    ax.set_title(
                        f"Distribution of {column}"
                    )

                    ax.set_xlabel(column)

                    ax.set_ylabel("Count")

                    plt.xticks(
                        rotation=45
                    )

                    st.pyplot(
                        fig,
                        use_container_width=True
                    )

                    plt.close(fig)


# =========================================
# GROUP ANALYSIS
# =========================================

elif page == "📊 Group Analysis":

    st.header("📊 Group Analysis")

    st.write(
        "Analyze a numerical column grouped by another column."
    )


    numerical_columns = data.select_dtypes(
        include="number"
    ).columns.tolist()


    all_columns = data.columns.tolist()


    if len(numerical_columns) == 0:

        st.info(
            "No numerical columns available for analysis."
        )

        st.stop()


    group_column = st.selectbox(
        "Group By",
        all_columns
    )


    analysis_column = st.selectbox(
        "Analyze Column",
        numerical_columns
    )


    operation = st.selectbox(
        "Operation",
        [
            "Sum",
            "Average",
            "Count",
            "Maximum",
            "Minimum"
        ]
    )


    # =====================================
    # GROUP ANALYSIS CALCULATION
    # =====================================

    try:

        grouped_data = (
            data
            .groupby(
                group_column,
                dropna=False
            )[analysis_column]
        )


        if operation == "Sum":

            result = grouped_data.sum()


        elif operation == "Average":

            result = grouped_data.mean()


        elif operation == "Count":

            result = grouped_data.count()


        elif operation == "Maximum":

            result = grouped_data.max()


        elif operation == "Minimum":

            result = grouped_data.min()


        # Convert safely to DataFrame

        result_df = result.reset_index()

        result_df.columns = [
            group_column,
            f"{operation} of {analysis_column}"
        ]


        st.subheader("📊 Group Analysis Result")

        st.dataframe(
            result_df,
            use_container_width=True
        )


        # Chart

        st.subheader("📈 Visualization")

        fig, ax = plt.subplots(
            figsize=(8, 4)
        )

        ax.bar(
            result_df[group_column].astype(str),
            result_df.iloc[:, 1]
        )

        ax.set_title(
            f"{operation} of {analysis_column} by {group_column}"
        )

        ax.set_xlabel(group_column)

        ax.set_ylabel(operation)

        plt.xticks(
            rotation=45
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


    except Exception as e:

        st.error(
            f"Error performing group analysis: {e}"
        )


# =========================================
# SIDEBAR FILTER STATUS
# =========================================

with st.sidebar:

    st.divider()

    if st.session_state.active_filter_column:

        st.success("🔎 Filter Active")

        st.caption(
            f"Column: {st.session_state.active_filter_column}"
        )

        st.caption(
            f"Rows: {len(data)}"
        )

    else:

        st.caption("No filter applied")