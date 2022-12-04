from django.db import models

from users.models import CustomUser


class Tags(models.Model):
    name = models.CharField(max_length=150)
    color = models.CharField(max_length=100, default="#D9DDDC", null=True)
    user = models.ForeignKey(
        CustomUser, related_name="tags", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
