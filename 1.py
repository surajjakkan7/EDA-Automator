# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page layout
st.set_page_config(layout="wide")

# Title and description
st.title('EDA Automator')
st.write('Upload your dataset and perform Exploratory Data Analysis effortlessly.')

# Upload file
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    # Read data
    @st.cache  # Cache data for faster reloads
    def load_data(file):
        try:
            return pd.read_csv(file)
        except Exception as e:
            st.error(f"Error: {e}")
            return None

    df = load_data(uploaded_file)

    if df is not None:
        # Display dataset
        st.subheader('Dataset Overview')
        st.write(df.head())

        # Perform EDA
        st.subheader('Exploratory Data Analysis')

        # Show dataset details
        if st.checkbox('Show Dataset Info'):
            st.write('Number of rows:', df.shape[0])
            st.write('Number of columns:', df.shape[1])
            st.write('Columns:', df.columns.tolist())
            st.write('Data Types:', df.dtypes)

        # Show summary statistics
        if st.checkbox('Show Summary Statistics'):
            st.write(df.describe())

        # Column Selection
        selected_columns = st.multiselect('Select columns for analysis', df.columns.tolist(), default=df.columns.tolist())
        if selected_columns:
            df_selected = df[selected_columns]

            # Show correlation heatmap (only for numeric columns)
            numerical_columns = df_selected.select_dtypes(include=[np.number]).columns.tolist()
            if st.checkbox('Show Correlation Heatmap'):
                corr_matrix = df_selected[numerical_columns].corr()
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", square=True, ax=ax)
                st.pyplot(fig)

            # Show distribution of numerical columns
            if st.checkbox('Show Distribution Plots'):
                for col in numerical_columns:
                    st.subheader(f'Distribution of {col}')
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sns.histplot(df_selected[col], kde=True, ax=ax)
                    st.pyplot(fig)

            # Customizable Plotting Options
            st.subheader('Customizable Plots')
            plot_column = st.selectbox('Select column to plot', df_selected.columns.tolist())
            plot_type = st.selectbox('Select plot type', ('Line Plot', 'Scatter Plot', 'Box Plot', 'Bar Plot'))
            if plot_type == 'Line Plot':
                fig, ax = plt.subplots()
                ax.plot(df_selected[plot_column])
                st.pyplot(fig)
            elif plot_type == 'Scatter Plot':
                scatter_column = st.selectbox('Select column for x-axis', df_selected.columns.tolist())
                fig, ax = plt.subplots()
                ax.scatter(df_selected[scatter_column], df_selected[plot_column])
                st.pyplot(fig)
            elif plot_type == 'Box Plot':
                fig, ax = plt.subplots()
                sns.boxplot(y=df_selected[plot_column], ax=ax)
                st.pyplot(fig)
            elif plot_type == 'Bar Plot':
                fig, ax = plt.subplots()
                sns.barplot(x=df_selected.index, y=df_selected[plot_column], ax=ax)
                st.pyplot(fig)

            # Show pairplot
            if st.checkbox('Show Pairplot'):
                fig = sns.pairplot(df_selected, diag_kind='kde')
                st.pyplot(fig)

            # Show correlation with target variable
             
            target_variable = st.selectbox('Select target variable (if applicable)', df_selected.columns.tolist())
            if target_variable and target_variable in df_selected.columns:
                st.subheader(f'Correlation of {target_variable} with other variables')
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(df_selected[numerical_columns].corr()[[target_variable]].sort_values(by=target_variable, ascending=False),
                            annot=True, cmap='coolwarm', fmt=".2f", square=True, ax=ax)
                st.pyplot(fig)
            
            # Show unique values and counts for selected columns
            st.subheader('Unique Values and Counts')
            selected_column = st.selectbox('Select a column to show unique values and counts', df_selected.columns.tolist())
            if selected_column:
                if selected_column in df_selected.columns:
                    if df_selected[selected_column].dtype == 'object':  # Check if the selected column is of type 'object' (i.e., string)
                        value_counts = df_selected[selected_column].value_counts()
                        st.write(value_counts)
                    else:
                        st.write('Selected column is not of type "object" (string).')
                else:
                    st.write(f'Column "{selected_column}" does not exist in the dataset.')

            # Download the processed dataset
            st.subheader('Download Processed Dataset')
            csv = df_selected.to_csv(index=False)
            st.download_button(label="Download CSV", data=csv, file_name='processed_data.csv', mime='text/csv')

else:
    st.info('Please upload a CSV file.')

# Sidebar content
st.sidebar.markdown('---')

# Contact Developer expander
developer_expander = st.sidebar.expander('Contact Developer', expanded=False)
with developer_expander:
    st.text('Developed By:')
    st.text("Suraj Jakkan")
    st.text("Email:")
    st.text('surajjakkan@outlook.com')
    st.markdown('[Link to Profile](https://surajjakkan7.github.io/profile/)')

# Contact form expander
contact_expander = st.sidebar.expander('Contact Form', expanded=False)
with contact_expander:
    name = st.text_input('Name')
    email = st.text_input('Email')
    message = st.text_area('Message', height=150)

    if st.button('Send Message'):
        # Placeholder code for handling message submission
        st.success('Message sent successfully!')
