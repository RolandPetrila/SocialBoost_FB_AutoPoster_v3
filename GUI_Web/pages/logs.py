import streamlit as st
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def tail(path: Path, n: int = 200) -> str:
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        return ''.join(lines[-n:])
    except Exception as e:
        return f"<error reading {path.name}: {e}>"


def render():
    st.header("📝 Logs")

    logs_dir = PROJECT_ROOT / "Logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_files = list(logs_dir.glob("*.log"))
    if not log_files:
        st.info("No logs found. Run operations to generate logs.")
        return

    for log_file in log_files:
        st.subheader(log_file.name)
        st.code(tail(log_file, 300), language='log')
