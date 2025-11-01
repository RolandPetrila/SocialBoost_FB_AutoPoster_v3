import streamlit as st
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def render():
    st.header("📅 Programare Postări")

    schedule_path = PROJECT_ROOT / "Config" / "schedule.json"

    # Load current schedule
    if schedule_path.exists():
        try:
            with open(schedule_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            jobs = data.get('jobs', [])
        except Exception:
            jobs = []
            data = {'jobs': []}
    else:
        jobs = []
        data = {'jobs': []}

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Joburi Programate")
        if jobs:
            for idx, job in enumerate(jobs):
                with st.expander(f"Job #{idx+1}: {job.get('type', 'unknown')} - {job.get('task', 'N/A')}"):
                    st.write(f"**Type**: {job.get('type', 'N/A')}")
                    st.write(f"**Task**: {job.get('task', 'N/A')}")
                    st.write(f"**Enabled**: {'✅ Yes' if job.get('enabled') else '❌ No'}")
                    if job.get('type') == 'daily':
                        st.write(f"**Time**: {job.get('time', 'N/A')}")
                    elif job.get('type') == 'weekly':
                        st.write(f"**Day**: {job.get('day', 'N/A')}")
                        st.write(f"**Time**: {job.get('time', 'N/A')}")
                    elif job.get('type') == 'interval':
                        st.write(f"**Interval**: {job.get('every_minutes', 0)} minutes")
                    elif job.get('type') == 'once':
                        st.write(f"**Run at**: {job.get('run_at_datetime', 'N/A')}")
                    st.write(f"**Last Run**: {job.get('last_run', 'Never')}")
                    if st.button("🗑️ Delete", key=f"delete_{idx}"):
                        jobs.pop(idx)
                        data['jobs'] = jobs
                        with open(schedule_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2)
                        st.success("Job deleted!")
                        st.rerun()
        else:
            st.info("No scheduled jobs yet.")

    with col2:
        st.subheader("Adaugă Job Nou")
        with st.form("add_job_form"):
            job_type = st.selectbox("Tip Job", ["daily", "weekly", "interval", "once"])
            day = None
            time_str = None
            minutes = None
            datetime_str = None

            if job_type == "daily":
                time_input = st.time_input("Ora")
                time_str = time_input.strftime("%H:%M")
            elif job_type == "weekly":
                day = st.selectbox("Ziua", [
                    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
                ])
                time_input = st.time_input("Ora")
                time_str = time_input.strftime("%H:%M")
            elif job_type == "interval":
                minutes = st.number_input("Interval (minute)", min_value=1, value=60)
            elif job_type == "once":
                date_input = st.date_input("Data")
                time_input = st.time_input("Ora")
                datetime_str = f"{date_input}T{time_input.strftime('%H:%M')}:00"

            task = st.text_input("Task (fișier .py)", value="auto_post.py")
            enabled = st.checkbox("Activat", value=True)
            submitted = st.form_submit_button("➕ Adaugă Job")

            if submitted:
                new_job = {
                    'type': job_type,
                    'task': task,
                    'enabled': enabled,
                    'last_run': None
                }
                if job_type == "daily":
                    new_job['time'] = time_str
                elif job_type == "weekly":
                    new_job['day'] = day
                    new_job['time'] = time_str
                elif job_type == "interval":
                    new_job['every_minutes'] = minutes
                elif job_type == "once":
                    new_job['run_at_datetime'] = datetime_str
                    new_job['executed'] = False

                jobs.append(new_job)
                data['jobs'] = jobs
                with open(schedule_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                st.success("Job adăugat cu succes!")
                st.rerun()
