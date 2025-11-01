import streamlit as st
from pathlib import Path
import json
from PIL import Image
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def render():
    st.header("📁 Gestionare Assets")

    col1, col2 = st.columns([2, 1])

    images_dir = PROJECT_ROOT / "Assets" / "Images"
    videos_dir = PROJECT_ROOT / "Assets" / "Videos"
    images_dir.mkdir(parents=True, exist_ok=True)
    videos_dir.mkdir(parents=True, exist_ok=True)

    with col1:
        st.subheader("Fișiere Disponibile")
        image_files = list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png")) + list(images_dir.glob("*.jpeg"))
        video_files = list(videos_dir.glob("*.mp4")) + list(videos_dir.glob("*.mov"))

        st.write(f"📸 **Images**: {len(image_files)} files")
        st.write(f"🎥 **Videos**: {len(video_files)} files")

        selected_files = []
        if image_files:
            st.markdown("### Images")
            for img_file in image_files:
                if st.checkbox(f"📷 {img_file.name}", key=f"img_{img_file.name}"):
                    selected_files.append(str(img_file))
        if video_files:
            st.markdown("### Videos")
            for vid_file in video_files:
                if st.checkbox(f"🎬 {vid_file.name}", key=f"vid_{vid_file.name}"):
                    selected_files.append(str(vid_file))

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💾 Save Selection", use_container_width=True):
                selected_images = [f for f in selected_files if any(f.endswith(ext) for ext in ['.jpg', '.png', '.jpeg'])]
                selected_videos = [f for f in selected_files if any(f.endswith(ext) for ext in ['.mp4', '.mov'])]
                data = {"images": selected_images, "videos": selected_videos}
                json_path = PROJECT_ROOT / "selected_assets.json"
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                st.success(f"Saved {len(selected_images)} images and {len(selected_videos)} videos!")
        with col_b:
            if st.button("📤 Post Selected", use_container_width=True):
                script_path = PROJECT_ROOT / "Automatizare_Completa" / "auto_post.py"
                result = subprocess.run(
                    [sys.executable, str(script_path), "--selected-only"],
                    capture_output=True,
                    text=True,
                    cwd=str(PROJECT_ROOT),
                )
                if result.returncode == 0:
                    st.success("✅ Selected assets posted!")
                else:
                    st.error(f"❌ Posting failed: {result.stderr}")

    with col2:
        st.subheader("Preview")
        selected_images = [f for f in st.session_state.keys() if str(f).startswith('img_')]
        # Attempt preview of first checked image from checkboxes
        preview_path = None
        for img_file in image_files:
            key = f"img_{img_file.name}"
            if st.session_state.get(key):
                preview_path = img_file
                break
        if preview_path:
            try:
                img = Image.open(preview_path)
                st.image(img, caption=preview_path.name, use_column_width=True)
            except Exception:
                st.error("Cannot preview image")
        else:
            st.info("Select an image to preview")

        st.markdown("---")
        st.subheader("Upload New Assets")
        uploaded_files = st.file_uploader(
            "Upload images/videos",
            accept_multiple_files=True,
            type=['jpg', 'jpeg', 'png', 'mp4', 'mov']
        )
        if uploaded_files:
            saved = 0
            for uploaded_file in uploaded_files:
                save_dir = images_dir if uploaded_file.type.startswith('image') else videos_dir
                save_path = save_dir / uploaded_file.name
                try:
                    with open(save_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    saved += 1
                except Exception as e:
                    st.error(f"Failed to save {uploaded_file.name}: {e}")
            st.success(f"Uploaded {saved} files!")
            st.rerun()
