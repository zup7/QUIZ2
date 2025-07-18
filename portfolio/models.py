from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    project_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name

    class Meta:
        ordering = ['-created_at']


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio_title = models.CharField(max_length=200)
    portfolio_description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} - Portfolio"

    def get_absolute_url(self):
        return reverse('portfolio:detail', kwargs={'username': self.user.username})

    class Meta:
        ordering = ['-id']
