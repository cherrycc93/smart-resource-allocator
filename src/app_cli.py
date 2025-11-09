import argparse
from src.io.load_data import load_employee_data, load_project_data
from src.models.linear_allocator import allocate_resources


def main():
    parser = argparse.ArgumentParser(description="Smart Resource Allocator CLI")
    parser.add_argument("--employees", required=True, help="Path to employees CSV")
    parser.add_argument("--projects", required=True, help="Path to projects CSV")
    args = parser.parse_args()

    employees, max_hours = load_employee_data(args.employees)
    projects, project_demand, project_value = load_project_data(args.projects)

    # build value dict: same value per hour for each employee-project pair from project_value
    value = {(i, j): project_value[j] for i in employees for j in projects}

    allocation, total_value = allocate_resources(employees, projects, value, max_hours, project_demand)

    print(f"Optimal total value: {total_value}")
    for (i, j), hours in allocation.items():
        if hours > 1e-6:
            print(f"{i} -> {j}: {hours:.2f}")


if __name__ == "__main__":
    main()
