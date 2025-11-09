import pulp as pl


def allocate_resources(employees, projects, value, max_hours, project_demand):
    """
    Solve a linear programming resource allocation problem.

    Parameters:
        employees (list): List of employee names.
        projects (list): List of project names.
        value (dict): Dictionary mapping (employee, project) to value per hour.
        max_hours (dict): Dictionary mapping employee to maximum available hours.
        project_demand (dict): Dictionary mapping project to required hours.

    Returns:
        tuple: (allocation, total_value, status)
        allocation is a dictionary mapping (employee, project) to allocated hours.
        total_value is the optimal objective value.
        status is the solver status string.
    """
    # Create LP problem
    model = pl.LpProblem("Employee_Project_Allocation", pl.LpMaximize)

    # Decision variables: hours employee i spends on project j
    x = pl.LpVariable.dicts(
        "hours",
        (employees, projects),
        lowBound=0,
        cat="Continuous"
    )

    # Objective: maximize total value
    model += pl.lpSum(value[(i, j)] * x[i][j] for i in employees for j in projects)

    # Employee capacity constraints
    for i in employees:
        model += pl.lpSum(x[i][j] for j in projects) <= max_hours[i], f"Cap_{i}"

    # Project demand constraints
    for j in projects:
        model += pl.lpSum(x[i][j] for i in employees) >= project_demand[j], f"Demand_{j}"

    # Solve the LP
    status = model.solve(pl.PULP_CBC_CMD(msg=False))

    # Extract results
    allocation = {(i, j): x[i][j].varValue for i in employees for j in projects}
    total_value = pl.value(model.objective)
    status_str = pl.LpStatus[status]

    return allocation, total_value, status_str
