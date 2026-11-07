# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.
 
import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
 
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)
 
# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")
 
# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("What is your favorite NFL team?")
    value_input = st.text_input("About how many NFL games do you watch per season? (number)")
 
    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")
 
    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        category_clean = category_input.strip().title()
        value_clean = value_input.strip()
 
        # Validate input before writing
        if category_clean == "" or value_clean == "":
            st.error("Please fill out both fields.")
            st.stop()
        try:
            float(value_clean)
        except ValueError:
            st.error("The value must be a number.")
            st.stop()
 
        # Append a new row to data.csv (write the header if the file is new/empty)
        file_exists = os.path.exists('data.csv') and os.path.getsize('data.csv') > 0
        needs_newline = False
        if file_exists:
            with open('data.csv', 'rb') as f:
                f.seek(-1, os.SEEK_END)
                needs_newline = f.read(1) not in (b'\n', b'\r')
 
        with open('data.csv', 'a', newline='') as f:
            if not file_exists:
                f.write('Category,Value\n')
            elif needs_newline:
                f.write('\n')
            f.write(f'"{category_clean}",{value_clean}\n')
 
        st.success("Your data has been submitted!")
        st.write(f"You entered: **Category:** {category_clean}, **Value:** {value_clean}")
 
 
# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")
 
# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
