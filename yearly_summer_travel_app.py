import streamlit as st  # Import Streamlit library to create web application
import csv  # Import CSV module to read comma-separated value files
import matplotlib.pyplot as plt  # Import matplotlib for creating visualizations

def load_and_process_data():
    month_map = {'5': 'May', '6': 'June', '7': 'July', '8': 'August'}  # Create a dictionary to map numeric month values to their names
    
    # Initialize empty lists to store our data
    year = []  # Will store the years from the dataset
    months = []  # Will store the months from the dataset
    domestic_Num_Of_flts = []  # Will store the number of domestic flights
    
    summer_months = ['5', '6', '7', '8'] # Define months to analyze (summer months)
    
    with open("US_Airline_Traffic_data_From_2003_To_2023", "r") as air_Tra_Data:
        content = csv.reader(air_Tra_Data) # Create a CSV reader object to read the file
        next(content) # Skip the first row (header row) of the CSV file
        
        for data_row in content: # Iterate through each row in the CSV file
            if data_row[1] in summer_months: # Check if the month is one of our summer months
                year.append(data_row[0])
                months.append(data_row[1])
                
                domestic_flights = data_row[5].replace(",", "") # Remove commas from the flight number and convert to integer
                domestic_Num_Of_flts.append(int(domestic_flights)) # Add the number of domestic flights to our list
    
    return year, months, domestic_Num_Of_flts, month_map # Return all the collected data

def prepare_data(year_label, year, months, domestic_Num_Of_flts, month_map):
    selected_year_indices = [] # Initialize a list to store indices of rows matching the selected year
    
    for index in range(0, len(year)): # Find all indices where the year matches the selected year
        if year[index] == year_label:
            selected_year_indices.append(index) # Store the index of matching rows
    
    # Initialize lists to store months and flights for the selected year
    selected_plot_months = []
    selected_plot_flights = []
    
    for index in selected_year_indices: # Collect months and flight numbers for the selected year
        selected_plot_months.append(months[index])
        selected_plot_flights.append(domestic_Num_Of_flts[index]) # Add the corresponding number of flights
    
    selected_plot_month_names = []
    
    for month in selected_plot_months: # Convert numeric month values to month names
        selected_plot_month_names.append(month_map[month]) # Use the month_map to convert numbers to names
    
    return selected_plot_month_names, selected_plot_flights # Return the list of month names and flight numbers

def main():
    st.title('Domestic Flights in Summer Months')
    year, months, domestic_Num_Of_flts, month_map = load_and_process_data() # Load and process the data from the CSV file
    unique_years = sorted(set(year)) # Get a sorted list of unique years from the dataset
    selected_year = st.selectbox('Select a Year', unique_years) # Create a dropdown to select a specific year
    
    # Prepare the data for the selected year
    plot_month_names, plot_flights = prepare_data(
        selected_year, year, months, domestic_Num_Of_flts, month_map
    )
    
    fig, ax = plt.subplots(figsize=(10, 6)) # Create a new matplotlib figure
    ax.plot(plot_month_names, plot_flights, marker='o', linestyle='-', color='b') # Plot the data as a line graph with markers
    ax.set_title('Domestic Flights in Summer Months of ' + selected_year)
    ax.set_xlabel('Month (Summer Months)')
    ax.set_ylabel('Number of Domestic Flights')
    ax.set_xticklabels(plot_month_names, rotation=45)
    st.pyplot(fig) # Display the plot in the Streamlit application

# This ensures the main function runs only when the script is run directly
if __name__ == "__main__":
    main()