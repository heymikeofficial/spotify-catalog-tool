import streamlit as st
import requests
import json

st.title("🎵 Spotify Artist Catalog Metadata Extractor")
st.write("Extract complete metadata for any Spotify artist's catalog")

# Input field for Spotify artist URL
artist_url = st.text_input(
    "Spotify Artist URL", 
    placeholder="https://open.spotify.com/artist/4dpARuHxo51G3z768sgnrY",
    help="Paste the Spotify artist profile URL here"
)

if st.button("Extract Metadata", type="primary"):
    if artist_url:
        with st.spinner("Extracting metadata... This may take a few minutes for large catalogs."):
            try:
                # Send POST request to your Pipedream webhook
                response = requests.post(
                    "https://eoqvwg2k8fqpyc9.m.pipedream.net",
                    json={"artist_url": artist_url},
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("success"):
                        st.success("✅ Metadata extracted successfully!")
                        
                        # Display summary
                        metadata = data["data"]["metadata"]
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Artist", metadata["artistName"])
                        with col2:
                            st.metric("Total Tracks", metadata["totalTracks"])
                        with col3:
                            st.metric("Genre", metadata["genre"])
                        
                        # Download button
                        st.write("### 📥 Download Your Spreadsheet")
                        st.write(data["data"]["summary"])
                        
                        # Note: The downloadUrl contains the file path, you'll need to 
                        # implement file serving or use a different approach for downloads
                        st.info("💡 Your CSV file has been generated. Contact support for download access.")
                        
                    else:
                        st.error("❌ Failed to extract metadata")
                        
                else:
                    st.error(f"❌ Request failed with status {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Network error: {str(e)}")
            except json.JSONDecodeError:
                st.error("❌ Invalid response format")
    else:
        st.warning("⚠️ Please enter a Spotify artist URL")

# Example URLs
st.write("### 🎯 Example Artist URLs")
st.code("https://open.spotify.com/artist/4dpARuHxo51G3z768sgnrY  # Adele")
st.code("https://open.spotify.com/artist/1Xyo4u8uXC1ZmMpatF05PJ  # The Weeknd")
st.code("https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02  # Taylor Swift")
