import streamlit as st
import pandas as pd
import pydeck as pdk
import folium
from streamlit_folium import st_folium, folium_static

IMAGE_WIDTH = 300
BG_LINK = 'https://cdn.shopify.com/s/files/1/0020/6123/8339/products/6622379835438_720x.jpg'
LOGO_LINK = 'https://i.ibb.co/7rBQv9V/camel-removebg-preview.png'
FIRST_PAGE_LINK = 'https://i.etsystatic.com/icm/44e445/558970353/icm_fullxfull.558970353_nt195fa87j4gswwwkcgw.jpg'
    
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url({BG_LINK});
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url({LOGO_LINK});
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "Anniversary";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["public_gsheets_url"])


def page1():
    add_logo()
    add_bg_from_url()
    st.title("Learlir & Dandan")
    st.header(':heart: 2 Amazing Years Together :heart:')
    st.image(FIRST_PAGE_LINK, width=IMAGE_WIDTH)
    st.subheader('Our Story, by ChatGPT')
    relationship_summary = "In the summer of 2021, your eyes met for the first time at IDC, and it wasn't long before you shared your first kiss and official date at the Municipal Bar. Your bond deepened over shared laughter on your second date at Yam Bar, and during the third date, a pizza night at Lear's old apartment, your connection became undeniable. A thrilling movie night and a first sleepover paved the way to a stronger relationship. Amid these beautiful moments, you expressed your love for each other, an emotion beautifully captured during a documented ride together. Before embarking on a long-distance relationship phase of five months, you took a memorable trip to Mitzpe Ramon, creating cherished memories to hold on to during your time apart. During the long-distance period, Lear visited Idan in Madrid, symbolizing your dedication to each other. Upon reuniting, you began a thrilling chapter of adventures, traveling to Rome and Greece, moving in together, and even adopting a 'doggy daughter' named 'Lulu'. Over the span of these two years, your love story unfolded, marked by shared adventures, new beginnings, and enduring love that transcends distance."
    st.write(relationship_summary)

def page2():
    add_logo()
    add_bg_from_url()
    st.title("Learlir & Dandan")
    st.header('Our Story')

    # Add Year and Month Filters
    selected_year = st.selectbox("Filter by Year", ['', '2021', '2022', '2023'])
    selected_month = st.selectbox("Filter by Month", ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

    # Filter DataFrame based on selected filters
    filtered_df = df.copy()
    if selected_year:
        filtered_df = filtered_df[filtered_df['date'].str.contains(selected_year)]
    if selected_month:
        filtered_df = filtered_df[pd.to_datetime(filtered_df['date']).dt.strftime("%B") == selected_month]

    # Display filtered events as cards
    for index, row in filtered_df.iterrows():
        if row['missing'] == "no":
            st.subheader(row['event'])
            st.write('Date: ', pd.to_datetime(row['date']).strftime("%B %d, %Y"))
            st.write('Location: ', row['place'])
            st.image(row['image_link'], width=IMAGE_WIDTH)
            st.write(row['notes'])
            st.markdown("---")  # Line separator

def page3():
    add_logo()
    add_bg_from_url()
    m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()], 
                 zoom_start=3, control_scale=True, width=IMAGE_WIDTH)

  #Loop through each row in the dataframe
    for i,row in df.iterrows():
        #Setup the content of the popup
        iframe = folium.IFrame('What happend here? \n' + str(row["event"]) + '\n Where was it? \n' +str(row["place"]))
        
        #Initialise the popup using the iframe
        popup = folium.Popup(iframe, min_width=300, max_width=300)
        
        #Add each row to the map
        folium.Marker(location=[row['latitude'],row['longitude']],
                    popup = popup, c=row['event']).add_to(m)

    folium_static(m, width=IMAGE_WIDTH)

def page4():
    add_bg_from_url()
    st.title("Learlir & Dandan")
    st.header('Another Beautiful Year Together')

    message = "Happy anniversary, Lear! As we reflect on our journey over the past two years, I am overwhelmed with gratitude and love. The memories we have created together, from our first meeting at IDC to our adventures in Rome and Greece, have been nothing short of magical. Your presence in my life fills each day with joy and warmth. I am excited for the countless adventures and beautiful moments that lie ahead. Cheers to another year of love, growth, and shared happiness. I love you, always and forever."

    st.write(message)

pages = {
    "Home": page1,
    "Timeline": page2,
    "Map": page3
    "Invitation": page4
}

# Render the page navigation in the sidebar
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Display the selected page with the content
pages[selection]()
