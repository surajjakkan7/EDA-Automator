# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page layout
st.set_page_config(layout="wide")

# Title and description
st.title('EDA Automator App')
st.write('Upload your dataset and perform Exploratory Data Analysis effortlessly.')

# Upload file
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    # Read data
    @st.cache_data
    def load_data(file):
        return pd.read_csv(file)

    df = load_data(uploaded_file)

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

    # Data Cleaning Options
    st.subheader('Data Cleaning')
    if st.checkbox('Handle Missing Values'):
        missing_value_option = st.selectbox('Select missing value handling option', 
                                            ('None', 'Drop rows with missing values', 'Fill missing values with mean', 'Fill missing values with median'))
        if missing_value_option == 'Drop rows with missing values':
            df = df.dropna()
        elif missing_value_option == 'Fill missing values with mean':
            df = df.fillna(df.mean())
        elif missing_value_option == 'Fill missing values with median':
            df = df.fillna(df.median())

    # Column Selection
    selected_columns = st.multiselect('Select columns for analysis', df.columns.tolist(), default=df.columns.tolist())
    if selected_columns:
        df = df[selected_columns]

    # Show correlation heatmap
    if st.checkbox('Show Correlation Heatmap'):
        corr_matrix = df.corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", square=True, ax=ax)
        st.pyplot(fig)

    # Show distribution of numerical columns
    if st.checkbox('Show Distribution Plots'):
        numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        for col in numerical_columns:
            st.subheader(f'Distribution of {col}')
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.histplot(df[col], kde=True, ax=ax)
            st.pyplot(fig)

    # Customizable Plotting Options
    st.subheader('Customizable Plots')
    plot_column = st.selectbox('Select column to plot', df.columns.tolist())
    plot_type = st.selectbox('Select plot type', ('Line Plot', 'Scatter Plot', 'Box Plot', 'Bar Plot'))
    if plot_type == 'Line Plot':
        fig, ax = plt.subplots()
        ax.plot(df[plot_column])
        st.pyplot(fig)
    elif plot_type == 'Scatter Plot':
        scatter_column = st.selectbox('Select column for x-axis', df.columns.tolist())
        fig, ax = plt.subplots()
        ax.scatter(df[scatter_column], df[plot_column])
        st.pyplot(fig)
    elif plot_type == 'Box Plot':
        fig, ax = plt.subplots()
        sns.boxplot(y=df[plot_column], ax=ax)
        st.pyplot(fig)
    elif plot_type == 'Bar Plot':
        fig, ax = plt.subplots()
        sns.barplot(x=df.index, y=df[plot_column], ax=ax)
        st.pyplot(fig)

    # Show pairplot
    if st.checkbox('Show Pairplot'):
        fig = sns.pairplot(df, diag_kind='kde')
        st.pyplot(fig)

    # Show correlation with target variable
    target_variable = st.selectbox('Select target variable (if applicable)', df.columns.tolist())
    if target_variable and target_variable in df.columns:
        st.subheader(f'Correlation of {target_variable} with other variables')
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(df.corr()[[target_variable]].sort_values(by=target_variable, ascending=False),
                    annot=True, cmap='coolwarm', fmt=".2f", square=True, ax=ax)
        st.pyplot(fig)

    # Download the processed dataset
    st.subheader('Download Processed Dataset')
    csv = df.to_csv(index=False)
    st.download_button(label="Download CSV", data=csv, file_name='processed_data.csv', mime='text/csv')

else:
    st.info('Please upload a CSV file.')

# Sidebar content

st.sidebar.markdown('---')

developer_expander = st.sidebar.expander('Contact Developer ', expanded=False)

with developer_expander:
    st.text('Developed By:')
    st.text("Suraj Jakkan")
    st.text("Email_Id:")
    st.text('surajjakkan@outlook.com')
    st.text("Profile")
    st.markdown('[Link to Profile](https://surajjakkan7.github.io/profile/)')

# Contact form
# Contact form expander
contact_expander = st.sidebar.expander('Contact Form', expanded=False)

with contact_expander:
    name = st.text_input('Name')
    email = st.text_input('Email')
    message = st.text_area('Message', height=150)

    if st.button('Send Message'):
        # Here you can add code to handle the message submission, like sending an email or storing in a database
        st.success('Message sent successfully!')