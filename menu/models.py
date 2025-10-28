from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menu_items')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    availability = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class TodaySpecial(models.Model):
    name = models.CharField(max_length=100, default='Special Menu')
    items = models.ManyToManyField(MenuItem)
    created_at = models.DateTimeField(auto_now_add=True)


class ScheduledSpecial(models.Model):
    special = models.ForeignKey(TodaySpecial, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.special.name} ({self.start_date} to {self.end_date})"