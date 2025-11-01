import streamlit as st
import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def render():
    st.header("📊 Control Panel")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Project Status")

        # PROJECT_CONTEXT.json
        context_path = PROJECT_ROOT / "PROJECT_CONTEXT.json"
        if context_path.exists():
            try:
                with open(context_path, 'r', encoding='utf-8') as f:
                    context = json.load(f)
                st.metric("Project", context.get('project_name', 'Unknown'))
                st.metric("Stage", context.get('current_stage', 'Unknown'))
                st.metric("Last Commit", str(context.get('last_commit', 'Unknown'))[:7])
            except Exception as e:
                st.warning(f"Cannot read PROJECT_CONTEXT.json: {e}")

        # Health check summary
        health_path = PROJECT_ROOT / "Logs" / "health_check.json"
        if health_path.exists():
            try:
                with open(health_path, 'r', encoding='utf-8', errors='replace') as f:
                    health = json.load(f)
                overall = health.get('overall_health', 'Unknown') or health.get('Overall Health', 'Unknown')
                score = health.get('health_score', health.get('Health Score', 0.0))
                if str(overall).lower().startswith('healthy'):
                    st.success(f"✅ Health: {overall} (Score: {float(score):.2f})")
                else:
                    st.warning(f"⚠️ Health: {overall} (Score: {float(score):.2f})")
            except Exception as e:
                st.info("Run the health check to see details.")

        st.markdown("---")
        st.subheader("Facebook Token")
        if st.button("🔄 Check Token Status", key="check_token"):
            with st.spinner("Checking token..."):
                script_path = PROJECT_ROOT / "Automatizare_Completa" / "auto_post.py"
                result = subprocess.run(
                    [sys.executable, str(script_path), "--message", "Token check"],
                    capture_output=True,
                    text=True,
                    cwd=str(PROJECT_ROOT),
                )
                if result.returncode == 0:
                    st.success("✅ Token is valid and working!")
                else:
                    st.error(f"❌ Token validation failed: {result.stderr}")

        if st.button("🔄 Refresh All Status", key="refresh_status"):
            st.rerun()

    with col2:
        st.subheader("Quick Actions")

        if st.button("🏥 Run Health Check", key="health_check", use_container_width=True):
            with st.spinner("Running health check..."):
                script_path = PROJECT_ROOT / "Automatizare_Completa" / "health_check.py"
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    capture_output=True,
                    text=True,
                    cwd=str(PROJECT_ROOT),
                )
                if result.returncode == 0:
                    st.success("✅ Health check completed!")
                    st.rerun()
                else:
                    st.error(f"❌ Health check failed: {result.stderr}")

        if st.button("💾 Create Backup", key="backup", use_container_width=True):
            with st.spinner("Creating backup..."):
                script_path = PROJECT_ROOT / "backup_manager.py"
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    capture_output=True,
                    text=True,
                    cwd=str(PROJECT_ROOT),
                )
                if result.returncode == 0:
                    st.success("✅ Backup created successfully!")
                else:
                    st.error(f"❌ Backup failed: {result.stderr}")

        st.markdown("---")
        st.subheader("Scheduler Control")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("▶️ Start", key="start_scheduler", use_container_width=True):
                st.info("Scheduler starting... (use CLI to run as background process)")
        with col_b:
            if st.button("⏹️ Stop", key="stop_scheduler", use_container_width=True):
                st.info("Scheduler stopped! (manage processes via CLI)")

    st.markdown("---")
    st.subheader("📝 Recent Logs")

    # Show tail of main logs if present
    log_candidates = [
        PROJECT_ROOT / "Logs" / "system.log",
        PROJECT_ROOT / "Logs" / "scheduler.log",
        PROJECT_ROOT / "Logs" / "health_check.log",
    ]
    any_log = False
    for log_file in log_candidates:
        if log_file.exists():
            any_log = True
            st.caption(str(log_file))
            try:
                with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
                    lines = f.readlines()
                st.code(''.join(lines[-200:]), language='log')
            except Exception as e:
                st.warning(f"Cannot read {log_file.name}: {e}")
    if not any_log:
        st.info("No logs available yet.")
