import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="MatriX",
    page_icon="⚜️",  # ⚜️ эмодзи во вкладке
)

# Function to load data from an Excel file
def load_data(path: str):
    data = pd.read_excel(path)
    return data

uploaded_file = st.sidebar.file_uploader("📁 Choose file")

if uploaded_file is None:
    st.info("Upload a file through the file uploader", icon="ℹ️")
    st.stop()

df = load_data(uploaded_file)

st.sidebar.header("🌎 Choose country:")
# Get unique country values from the 'Country' column
countries = df['Country'].unique()
selected_countries = st.sidebar.multiselect("Pick countries ", countries)

st.header("📋 Data Analysis")

# Add a multiselect to choose the chart type
chart_types = st.sidebar.multiselect("Select Chart Types", ["Line Chart", "Bar Chart", "Pie Chart"])

# Display the Excel table
with st.expander("📋 Excel Table", expanded=True):
    st.write(df)


if chart_types:
    if "Pie Chart" in chart_types and selected_countries:
        st.subheader("📊  Pie Chart - Analysis for Selected Countries")
        # Calculate data counts for selected countries
        data_counts = df[df['Country'].isin(selected_countries)].groupby('Country').size()
        max_data_country = data_counts.idxmax()  # Find the country with the most data

        # Create a pie chart for the selected countries with the label
        fig, ax = plt.subplots()
        data = data_counts.values
        labels = data_counts.index
        explode = [0.1 if country == max_data_country else 0 for country in labels]  # Explode the country with the most data
        ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, explode=explode)
        ax.axis('equal')
        ax.legend(loc='best', frameon=True)  # Explicitly set the legend location
        st.pyplot(fig)

    for country in selected_countries:
        st.write(f"### {country}")

        country_data = df[df['Country'] == country]
        window_size = 3  # Define the window size here
        country_data = df[df['Country'] == country]

        if "Line Chart" in chart_types or "Bar Chart" in chart_types:
            st.write(f"#### Line and Bar Charts 📈 ")
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3))
            x = range(len(country_data))
            pop_ad_mod_sev_smoothed = np.convolve(country_data['pop_ad_mod_sev'], np.ones(window_size) / window_size, mode='same')
            pop_ad_sev_smoothed = np.convolve(country_data['pop_ad_sev'], np.ones(window_size) / window_size, mode='same')
            ax1.plot(x[:len(country_data)], pop_ad_mod_sev_smoothed, label=f'{country} - pop_ad_mod_sev', color='b')
            ax2.bar(x[:len(country_data)], pop_ad_mod_sev_smoothed, label=f'{country} - pop_ad_mod_sev', color='b')
            ax1.plot(x[:len(country_data)], pop_ad_sev_smoothed, label=f'{country} - pop_ad_sev', linestyle='-', color='r')
            ax2.bar(x[:len(country_data)], pop_ad_sev_smoothed, label=f'{country} - pop_ad_sev', color='r', alpha=0.5)
            ax1.set_xlabel('Data Point Index')
            ax2.set_xlabel('Data Point Index')
            ax1.set_ylabel('Values')
            ax2.set_ylabel('Values')
            ax1.tick_params(axis='x', rotation=45)
            ax2.tick_params(axis='x', rotation=45)
            ax1.legend(loc='best', frameon=True)  # Explicitly set the legend location
            ax2.legend(loc='best', frameon=True)  # Explicitly set the legend location
            st.pyplot(fig)
            country_data = df[df['Country'] == country].head(20)

            with st.expander(f"Data for {country}", expanded=False):
                st.table(country_data)

    # Button to display website information
    if st.button("📃"):
        st.write(
            "Этот веб-сайт - инструмент анализа данных, созданный с использованием Streamlit. Он позволяет загрузить файл Excel, выбирать страны и визуализировать данные с помощью различных типов графиков, включая линейные графики, столбчатые диаграммы и круговые диаграммы.")
        st.write(
            "Вы также можете исследовать данные в таблице Excel, отображенной выше. Линейные и столбчатые графики включают сглаженные данные для выбранных стран.")
