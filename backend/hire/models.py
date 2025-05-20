from django.contrib.postgres.fields import ArrayField
from django.db import models


class jobs_post(models.Model):
    job_id = models.AutoField(primary_key=True)  # Job ID
    title = models.CharField(max_length=255)  # Title 
    description = models.TextField()  # Description
    location = models.CharField(max_length=255)
    salary_range  = models.CharField(max_length=255) #Salary Range
    company_name = models.CharField(max_length=255) #Company Name
    P_date = models.DateField()     #Posting Date
    E_date = models.DateTimeField()  # Expiration Date
    skills = ArrayField(models.CharField(max_length=255), blank=True, default=list)  # Required Skills
    def __str__(self) -> str:
        return str(self.title)
