import streamlit as st
import pandas as pd
from src.models.linear_allocator import allocate_resources
from src.io.load_data import load_employee_data, load_project_data

st.title("Smart Resource Allocator")

uploaded_employees = st.file_uploader("Upload Employees CSV", type=["csv"])
uploaded_projects = st.file_uploader("Upload Projects CSV", type=["csv"])

if uploaded_employees is not None and uploaded_projects is not None:
    if st.button("Run Optimization"):
        employees_df = pd.read_csv(uploaded_employees)
        projects_df = pd.read_csv(uploaded_projects)
        employees = employees_df['employee'].tolist()
        max_hours = dict(zip(employees_df['employee'], employees_df['max_hours']))
        projects = projects_df['project'].tolist()
        project_demand = dict(zip(projects_df['project'], projects_df['required_hours']))
        project_value = dict(zip(projects_df['project'], projects_df['value']))
        value = {(i, j): project_value[j] for i in employees for j in projects}
        allocation, total_value = allocate_resources(employees, projects, value, max_hours, project_demand)
        st.write(f"Optimal total value: {total_value}")
        data = []
        for (i, j), hours in allocation.items():
            if hours > 1e-6:
                data.append({"employee": i, "project": j, "hours": hours})
        results_df = pd.DataFrame(data)
        st.dataframe(results_df)
        # charts
        if not results_df.empty:
            hours_per_employee = results_df.groupby('employee')['hours'].sum()
            st.bar_chart(hours_per_employee)
            hours_per_project = results_df.groupby('project')['hours'].sum()
            st.bar_chart(hours_per_project)
