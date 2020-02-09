from django.contrib.auth import get_user_model
from django.db import models


class Project(models.Model):
    author = models.ForeignKey(get_user_model(), related_name="projects", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateField(auto_now_add=True, db_index=True)
    updated_at = models.DateField(auto_now=True, db_index=True)

    def __str__(self):
        return f'[{self.id}] {self.author.first_name} {self.author.last_name} - {self.name}'


class Posting(models.Model):
    author = models.ForeignKey(get_user_model(), related_name="postings", on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    budget = models.FloatField()
    required_skills = models.ManyToManyField("skill.Skill")

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    length = models.IntegerField(blank=True, null=True)
    range = models.IntegerField(blank=True, null=True)
    location_longitude = models.FloatField(blank=True, null=True)
    location_latitude = models.FloatField(blank=True, null=True)

    project = models.ForeignKey(Project, related_name="postings", on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateField(auto_now_add=True, db_index=True)
    updated_at = models.DateField(auto_now=True, db_index=True)

    def __str__(self):
        return f'[{self.id}] {self.author.first_name} {self.author.last_name} - {self.title}'
