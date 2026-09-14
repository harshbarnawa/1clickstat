import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="1ClickStat",
    page_icon="📊",
    layout="wide"
)


# ---------------- TITLE ----------------

st.title("📊 1ClickStat")

st.write(
    "Upload your dataset, filter it, and get useful business insights in one click."
)


# ---------------- FILE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "xlsx", "json"]
)


# ---------------- LOAD DATA ----------------

if uploaded_file is not None:

    try:

        file_name = uploaded_file.name.lower()

        # CSV
        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        # EXCEL
        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        # JSON
        elif file_name.endswith(".json"):
            df = pd.read_json(uploaded_file)


        # ---------------- SUCCESS ----------------

        st.success("Dataset uploaded successfully! 🎉")


        # ---------------- DATASET PREVIEW ----------------

        st.subheader("📄 Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True
        )


        # ---------------- ANALYZE BUTTON ----------------

        if "show_analysis" not in st.session_state:
            st.session_state.show_analysis = False


        if st.button("⚡ Analyze Data"):
            st.session_state.show_analysis = True


        # =====================================================
        # ANALYSIS START
        # =====================================================

        if st.session_state.show_analysis:

            st.header("📊 Analysis Report")


            # =====================================================
            # FILTER DATA
            # =====================================================

            st.subheader("🔎 Filter Data")

            filter_column = st.selectbox(
                "Select a column to filter",
                df.columns
            )


            # Get unique values

            unique_values = sorted(
                df[filter_column]
                .dropna()
                .astype(str)
                .unique()
            )


            selected_values = st.multiselect(
                "Select value(s)",
                unique_values
            )


            # Apply filter

            if selected_values:

                filtered_df = df[
                    df[filter_column]
                    .astype(str)
                    .isin(selected_values)
                ]

            else:

                filtered_df = df.copy()


            # =====================================================
            # FILTERED DATA PREVIEW
            # =====================================================

            st.subheader("📄 Filtered Data Preview")

            st.write(
                f"Showing **{len(filtered_df)} rows**"
            )

            st.dataframe(
                filtered_df,
                use_container_width=True
            )


            # Use filtered data everywhere

            data = filtered_df


            # Get column types

            numerical_columns = data.select_dtypes(
                include="number"
            ).columns.tolist()


            categorical_columns = data.select_dtypes(
                exclude="number"
            ).columns.tolist()


            # =====================================================
            # DATASET OVERVIEW
            # =====================================================

            st.subheader("📌 Dataset Overview")


            total_rows = data.shape[0]

            total_columns = data.shape[1]


            col1, col2, col3, col4 = st.columns(4)


            col1.metric(
                "Rows",
                total_rows
            )


            col2.metric(
                "Columns",
                total_columns
            )


            col3.metric(
                "Numerical Columns",
                len(numerical_columns)
            )


            col4.metric(
                "Other Columns",
                len(categorical_columns)
            )


            # =====================================================
            # DATA QUALITY
            # =====================================================

            st.subheader("⚠️ Data Quality")


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


            # Missing values per column

            missing_per_column = data.isnull().sum()

            missing_per_column = missing_per_column[
                missing_per_column > 0
            ]


            if not missing_per_column.empty:

                st.write("### Missing Values by Column")

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

                st.success(
                    "No missing values found! 🎉"
                )


            # =====================================================
            # COLUMN INFORMATION
            # =====================================================

            st.subheader("🔍 Column Information")


            column_info = pd.DataFrame({

                "Column": data.columns,

                "Data Type": data.dtypes.astype(str).values,

                "Non-Null Values":
                    data.notnull().sum().values,

                "Unique Values":
                    data.nunique().values

            })


            st.dataframe(
                column_info,
                use_container_width=True
            )


            # =====================================================
            # NUMERICAL STATISTICS
            # =====================================================

            st.subheader("📈 Numerical Statistics")


            if len(numerical_columns) > 0:

                statistics = pd.DataFrame({

                    "Count":
                        data[numerical_columns].count(),

                    "Sum":
                        data[numerical_columns].sum(),

                    "Mean":
                        data[numerical_columns].mean(),

                    "Median":
                        data[numerical_columns].median(),

                    "Minimum":
                        data[numerical_columns].min(),

                    "Maximum":
                        data[numerical_columns].max(),

                    "Standard Deviation":
                        data[numerical_columns].std(),

                    "Variance":
                        data[numerical_columns].var()

                })


                st.dataframe(
                    statistics,
                    use_container_width=True
                )


            else:

                st.info(
                    "No numerical columns found."
                )


            # =====================================================
            # CORRELATION ANALYSIS
            # =====================================================

            st.subheader("🔗 Correlation Analysis")


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


            # =====================================================
            # BUSINESS GROUP ANALYSIS
            # =====================================================

            st.subheader("📊 Group Analysis")

            st.write(
                "Analyze a numerical column grouped by another column."
            )


            if len(data.columns) >= 2 and len(numerical_columns) > 0:


                col1, col2, col3 = st.columns(3)


                # GROUP BY COLUMN

                with col1:

                    group_column = st.selectbox(
                        "Group By",
                        data.columns,
                        key="group_column"
                    )


                # ANALYSIS COLUMN

                with col2:

                    available_analysis_columns = [

                        column

                        for column in numerical_columns

                        if column != group_column

                    ]


                    if available_analysis_columns:

                        analysis_column = st.selectbox(
                            "Analyze Column",
                            available_analysis_columns,
                            key="analysis_column"
                        )

                    else:

                        analysis_column = None

                        st.warning(
                            "Select a different Group By column."
                        )


                # OPERATION

                with col3:

                    operation = st.selectbox(
                        "Operation",
                        [
                            "Sum",
                            "Average",
                            "Count",
                            "Minimum",
                            "Maximum"
                        ],
                        key="operation"
                    )


                # ---------------- GROUP ANALYSIS ----------------

                if analysis_column is not None:


                    grouped_data = (
                        data
                        .groupby(group_column)[analysis_column]
                    )


                    if operation == "Sum":

                        result = grouped_data.sum()


                    elif operation == "Average":

                        result = grouped_data.mean()


                    elif operation == "Count":

                        result = grouped_data.count()


                    elif operation == "Minimum":

                        result = grouped_data.min()


                    elif operation == "Maximum":

                        result = grouped_data.max()


                    # Convert safely to dataframe

                    result_df = result.reset_index(
                        name=f"{operation} of {analysis_column}"
                    )


                    # Sort result

                    result_df = result_df.sort_values(
                        by=f"{operation} of {analysis_column}",
                        ascending=False
                    )


                    st.dataframe(
                        result_df,
                        use_container_width=True
                    )


                    # ---------------- GROUP CHART ----------------

                    st.subheader("📊 Group Analysis Chart")


                    fig, ax = plt.subplots(
                        figsize=(7, 4)
                    )


                    ax.bar(

                        result_df[group_column].astype(str),

                        result_df[
                            f"{operation} of {analysis_column}"
                        ]

                    )


                    ax.set_title(
                        f"{operation} of {analysis_column} by {group_column}"
                    )


                    ax.set_xlabel(group_column)

                    ax.set_ylabel(
                        f"{operation} of {analysis_column}"
                    )


                    plt.xticks(
                        rotation=45
                    )


                    plt.tight_layout()


                    st.pyplot(
                        fig,
                        use_container_width=True
                    )


                    plt.close(fig)


            else:

                st.info(
                    "Group Analysis requires at least one numerical column."
                )


            # =====================================================
            # AUTOMATIC VISUALIZATIONS
            # =====================================================

            st.subheader("📊 Automatic Visualizations")


            # ---------------- NUMERICAL GRAPHS ----------------

            if len(numerical_columns) > 0:

                st.write(
                    "### 📈 Numerical Distributions"
                )


                for i in range(
                    0,
                    len(numerical_columns),
                    2
                ):


                    col1, col2 = st.columns(2)


                    # FIRST GRAPH

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


                        plt.tight_layout()


                        st.pyplot(
                            fig,
                            use_container_width=True
                        )


                        plt.close(fig)


                    # SECOND GRAPH

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


                            plt.tight_layout()


                            st.pyplot(
                                fig,
                                use_container_width=True
                            )


                            plt.close(fig)


            # ---------------- CATEGORICAL GRAPHS ----------------

            if len(categorical_columns) > 0:


                st.write(
                    "### 📊 Categorical Distributions"
                )


                valid_categorical_columns = [

                    column

                    for column in categorical_columns

                    if data[column].nunique() <= 20

                ]


                for i in range(
                    0,
                    len(valid_categorical_columns),
                    2
                ):


                    col1, col2 = st.columns(2)


                    # FIRST GRAPH

                    with col1:


                        column = valid_categorical_columns[i]


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


                        plt.tight_layout()


                        st.pyplot(
                            fig,
                            use_container_width=True
                        )


                        plt.close(fig)


                    # SECOND GRAPH

                    if i + 1 < len(valid_categorical_columns):


                        with col2:


                            column = valid_categorical_columns[i + 1]


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


                            plt.tight_layout()


                            st.pyplot(
                                fig,
                                use_container_width=True
                            )


                            plt.close(fig)


    except Exception as e:

        st.error(
            f"Error loading or analyzing file: {e}"
        )