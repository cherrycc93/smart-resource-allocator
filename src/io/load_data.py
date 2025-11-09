import pandas as pd


def load_employee_data(file_path):
    """
    Load employee data from a CSV file.

    The CSV should have columns: employee,max_hours
    Returns a list of employee names and a dict mapping each employee to their max hours.
    """
    df = pd.read_csv(file_path)
    employees = df['employee'].tolist()
    max_hours = dict(zip(df['employee'], df['max_hours']))
    return employees, max_hours


def load_project_data(file_path):
    """
    Load project data from a CSV file.

    The CSV should have columns: project,required_hours,value
    Returns a list of project names, a dict mapping each project to its demand (required hours),
    and a dict mapping each project to its value contribution per hour.
    """
    df = pd.read_csv(file_path)
    projects = df['project'].tolist()
    project_demand = dict(zip(df['project'], df['required_hours']))
    project_value = dict(zip(df['project'], df['value']))
    return projects, project_demand, project_value
