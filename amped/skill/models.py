from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    sub_skills = models.ManyToManyField('self', related_name='parent_skill', blank=True)

    def __str__(self):
        return f'[{self.id}] {self.name}'
