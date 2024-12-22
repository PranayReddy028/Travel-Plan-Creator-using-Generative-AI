import streamlit as st
import google.generativeai as palm
import os
from datetime import datetime, timedelta
import json

# Setting up the Google API key
api_key = "AIzaSyB6oO3clAGEc7ictz3T-CZHHPcFDeo4UvI"
os.environ['GOOGLE_API_KEY'] = api_key

# Assuming palm.configure(api_key=os.getenv("PALM_API_KEY")) is correctly set up
if api_key is None:
    st.error("Error: GOOGLE_API_KEY environment variable is not set.")
else:
    palm.configure(api_key=api_key)

    # Fetching models supporting 'generateText' method
    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]

    if models:
        model = models[0].name
        #st.success(f"Model name: {model}")
    else:
        st.error("No models supporting 'generateText' generation method found.")

# Streamlit app and user input
st.title("TRAVEL ITINERARY GENERATOR")

city = st.text_input("Enter the city you're visiting:")

start_date = st.date_input("Select the start date for your trip:", value=datetime.today())
max_end_date = start_date + timedelta(days=30)
end_date = st.date_input("Select the end date for your trip:",
                         value=start_date + timedelta(days=1),
                         min_value=start_date,
                         max_value=max_end_date)

if st.button("Generate Itinerary"):
    days = (end_date - start_date).days
    prompt = f"You are a travel expert. Give me an itinerary for {city}, for {days} days, starting at 10am and ending at 10pm with a 30-minute buffer between each activity."

    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        max_output_tokens=3000,
    )

    itinerary = completion.result.strip()


    st.subheader("Travel Itinerary:")
    activities = itinerary.split("*")
    for activity in activities:
        if activity.strip():
            st.write(activity.strip())