import streamlit as st
import requests
import json
import io

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
                            st.metric("Genre", metadata.get("genre", "Unknown"))
                        
                        # Download button with actual CSV content
                        st.write("### 📥 Download Your Spreadsheet")
                        st.write(data["data"]["summary"])
                        
                        # Get CSV content from response
                        csv_content = data["data"]["csvContent"]
                        filename = data["data"]["filename"]
                        
                        # Create download button
                        st.download_button(
                            label="📄 Download CSV File",
                            data=csv_content,
                            file_name=filename,
                            mime="text/csv",
                            type="primary"
                        )
                        
                        # Show preview of first few rows
                        st.write("### 👀 Preview (First 5 Rows)")
                        lines = csv_content.split('\n')
                        preview = '\n'.join(lines[:6])  # Header + 5 rows
                        st.code(preview, language="csv")
                        
                    else:
                        st.error("❌ Failed to extract metadata")
                        
                else:
                    st.error(f"❌ Request failed with status {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Network error: {str(e)}")
            except json.JSONDecodeError:
                st.error("❌ Invalid response format")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a Spotify artist URL")
