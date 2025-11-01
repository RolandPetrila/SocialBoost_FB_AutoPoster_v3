import streamlit as st
from pathlib import Path
import subprocess
import sys
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def render():
    st.header("✍️ Generare Text")

    st.markdown("Generați conținut folosind OpenAI pe baza unui prompt sau pentru fișiere selectate.")

    with st.form("gen_form"):
        prompt = st.text_area("Prompt", value="Creează un post scurt despre importanța tehnologiei în viața de zi cu zi.")
        selected_assets = st.text_input("Fișiere țintă (opțional, separate prin virgulă)", value="")
        submitted = st.form_submit_button("🪄 Generează")
        if submitted:
            with st.spinner("Generare conținut..."):
                script_path = PROJECT_ROOT / "Automatizare_Completa" / "auto_generate.py"
                args = [sys.executable, str(script_path)]
                if prompt.strip():
                    args += ["--prompt", prompt.strip()]
                if selected_assets.strip():
                    assets = [a.strip() for a in selected_assets.split(',') if a.strip()]
                    args += ["--assets", *assets]
                result = subprocess.run(args, capture_output=True, text=True, cwd=str(PROJECT_ROOT))
                if result.returncode == 0:
                    st.success("✅ Generare completă")
                    st.code(result.stdout[-5000:], language='text')
                else:
                    st.error("❌ Generare eșuată")
                    st.code(result.stderr, language='text')
