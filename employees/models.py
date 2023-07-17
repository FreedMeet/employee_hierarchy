from django.db import models

class Employee(models.Model):
    POSITIONS = [
        'Executor',
        'Senior Executor',
        'Coordinator',
        'Project Manager',
        'Department Head',
        'Director',
        'CEO',
    ]

    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, choices=[(pos, pos) for pos in POSITIONS])
    hire_date = models.DateField()
    email = models.EmailField()
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')

    def __str__(self):
        return self.full_name