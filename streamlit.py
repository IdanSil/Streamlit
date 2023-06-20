import streamlit as st
import pandas as pd
import pydeck as pdk
import folium
from streamlit_folium import st_folium, folium_static

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://static.basicinvite.com/media/bi/33263/multicolored-hearts-wallpaper-2x.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )


df = pd.read_csv('Firsts - st.csv')

def page1():
  add_bg_from_url()
  st.title("Learlir & Dandan")
  st.header(':heart: 2 Amazing Years Together :heart:')
  st.image('https://i.ibb.co/7rBQv9V/camel-removebg-preview.png', width=500)
  st.subheader('Our Story, by ChatGPT')
  relationship_summary = "In the summer of 2021, your eyes met for the first time at IDC, and it wasn't long before you shared your first kiss and official date at the Municipal Bar. Your bond deepened over shared laughter on your second date at Yam Bar, and during the third date, a pizza night at Lear's old apartment, your connection became undeniable. A thrilling movie night and a first sleepover paved the way to a stronger relationship. Amid these beautiful moments, you expressed your love for each other, an emotion beautifully captured during a documented ride together. Before embarking on a long-distance journey of five months, you took a memorable trip to Mitzpe Ramon, creating cherished memories to hold on to during your time apart. During the long-distance period, while you were studying in the US and Lear was in Israel, Lear visited you in Madrid, symbolizing your dedication to each other. Upon reuniting, you began a thrilling chapter of adventures, traveling to Rome and Greece, moving in together, and even adopting a 'doggy daughter'. Over the span of these two years, your love story unfolded, marked by shared adventures, new beginnings, and enduring love that transcends distance."
  st.write(relationship_summary)

def page2():
  add_bg_from_url()
  st.title("Learlir & Dandan")
  st.header('Our Story')
  # Display events as cards
  for index, row in df.iterrows():
      st.subheader(row['event'])
      st.write('Date: ', row['date'])
      st.write('Location: ', row['place'])
      st.image(row['image_link'],width=1000)
      st.write(row['notes'])
      st.markdown("---")  # Line separator

def page3():
  add_bg_from_url()
  m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()], 
                 zoom_start=3, control_scale=True)

  #Loop through each row in the dataframe
  for i,row in df.iterrows():
      #Setup the content of the popup
      iframe = folium.IFrame('What happend here?' + str(row["event"]))
      
      #Initialise the popup using the iframe
      popup = folium.Popup(iframe, min_width=300, max_width=300)
      
      #Add each row to the map
      folium.Marker(location=[row['latitude'],row['longitude']],
                    popup = popup, c=row['event']).add_to(m)

  folium_static(m, width=1000)

pages = {
    "Home": page1,
    "Timeline": page2,
    "Map": page3
}

# Render the page navigation in the sidebar
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Display the selected page with the content
pages[selection]()
