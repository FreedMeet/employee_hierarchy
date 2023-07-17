from django_seed import Seed
from employees.models import Employee
import random

def generate_fake_employee_data(total_records=40000):
    positions = [
        'Executor',
        'Senior Executor',
        'Coordinator',
        'Project Manager',
        'Department Head',
        'Director',
        'CEO',
    ]

    seeder = Seed.seeder()
    seeder.add_entity(Employee, total_records, {
        'full_name': lambda x: seeder.faker.name(),
        'position': lambda x: random.choice(positions),
        'hire_date': lambda x: seeder.faker.date_this_decade(),
        'email': lambda x: seeder.faker.email(),
        'supervisor': lambda x: None,
    })

    inserted_pks = seeder.execute()
    employees = Employee.objects.in_bulk(inserted_pks[Employee])

    for employee in employees.values():
        if employee.position != 'CEO':
            higher_position = positions[positions.index(employee.position) + 1]
            supervisors = Employee.objects.filter(position=higher_position)
            if supervisors.exists():
                employee.supervisor = random.choice(supervisors)
            else:
                employee.supervisor = None
            employee.save()
            print(f"Created employee: {employee.full_name}")

generate_fake_employee_data()