import streamlit as st
import requests
import json

st.title("🎵 Spotify Artist Catalog Metadata Extractor")
st.write("Extract complete metadata for any Spotify artist's catalog")

# Input field for Spotify artist URL
artist_url = st.text_input(
    "Spotify Artist URL", 
    placeholder="https://open.spotify.com/artist/3TVXtAsR1Inumwj472S9r4",
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
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    timeout=300  # 5 minute timeout for large catalogs
                )
                
                st.write(f"Response status: {response.status_code}")
                st.write(f"Response headers: {dict(response.headers)}")
                
                if response.status_code == 200:
                    try:
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
                            st.write("Response:", data)
                            
                    except json.JSONDecodeError as e:
                        st.error("❌ Invalid JSON response")
                        st.write("Raw response:", response.text[:1000])
                        
                else:
                    st.error(f"❌ Request failed with status {response.status_code}")
                    st.write("Response text:", response.text[:1000])
                    
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. Large catalogs may take several minutes to process.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Network error: {str(e)}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a Spotify artist URL")
