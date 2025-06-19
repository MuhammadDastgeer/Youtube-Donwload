import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Video Downloader", layout="centered")
st.title("📥 YouTube Video Downloader")

url = st.text_input("🔗 Enter YouTube video URL:")

def get_video_info(url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

def sizeof_fmt(num, suffix="B"):
    for unit in ['','K','M','G']:
        if abs(num) < 1024.0:
            return f"{num:.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} T{suffix}"

if url:
    try:
        info = get_video_info(url)

        st.image(info['thumbnail'], width=400)
        st.subheader(f"🎬 {info['title']}")

        # Filter formats with both video and audio
        formats = [
            f for f in info['formats']
            if f.get('vcodec') != 'none' and f.get('acodec') != 'none'
        ]

        # Prepare format options for dropdown
        format_options = []
        format_map = {}
        for f in formats:
            resolution = f.get('format_note') or f.get('height') or 'Unknown'
            filesize = f.get('filesize') or f.get('filesize_approx') or 0
            label = f"{resolution} - {sizeof_fmt(filesize)}"
            format_options.append(label)
            format_map[label] = f

        st.markdown("### 🎯 Select Quality")
        selected_label = st.selectbox("Choose resolution:", format_options)

        if st.button("⬇️ Download Selected"):
            selected_format = format_map[selected_label]
            resolution = selected_format.get('format_note') or selected_format.get('height') or 'video'
            filename = f"{info['title'].replace(' ', '_')}_{resolution}.mp4"

            with st.spinner("Downloading..."):
                ydl_opts = {
                    'format': selected_format['format_id'],
                    'outtmpl': filename,
                    'quiet': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

            with open(filename, "rb") as f:
                st.download_button(
                    label=f"📥 Save to your PC: {selected_label}",
                    data=f,
                    file_name=filename,
                    mime="video/mp4"
                )

            os.remove(filename)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
