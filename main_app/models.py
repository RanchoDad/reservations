from django.db import models

class Reservation(models.Model):
    date = models.DateField()
    time = models.TimeField()
    openings = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f"Reservation on {self.date} at {self.time}"

