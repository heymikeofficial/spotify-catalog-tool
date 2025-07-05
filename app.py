import streamlit as st
import requests
import json

st.title("Spotify Artist Catalog Metadata Tool")
st.write("Get complete metadata for an artist's entire catalog")

# Input for Spotify artist URL
artist_url = st.text_input("Enter Spotify Artist URL:", 
                          placeholder="https://open.spotify.com/artist/...")

def call_pipedream_agent(artist_url):
    webhook_url = "https://eoxae8bluv1cjyy.m.pipedream.net"
    
    data = {
        "artist_url": artist_url
    }
    
    try:
        response = requests.post(webhook_url, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if st.button("Get Artist Catalog Metadata"):
    if artist_url:
        st.write("Processing... this may take a minute")
        result = call_pipedream_agent(artist_url)
        st.write("Result:", result)
    else:
        st.error("Please enter a Spotify artist URL first")
