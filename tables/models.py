from django.db import models
from datetime import timedelta

class Table(models.Model):
    number = models.CharField(max_length=10)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.number}"


class Booking(models.Model):
    date = models.DateField()
    time = models.TimeField()  # booking start time
    end_time = models.TimeField(blank=True, null=True)  # auto-calculated end time
    tables = models.ManyToManyField(Table)  # multiple tables ek booking me
    customer_name = models.CharField(max_length=100)
    total_persons = models.IntegerField()
    contact_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.time and not self.end_time:
            # add 1 hour to start time
            from datetime import datetime, timedelta
            dt = datetime.combine(self.date, self.time)
            dt_end = dt + timedelta(hours=1.5)
            self.end_time = dt_end.time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} - {self.date} {self.time}"


