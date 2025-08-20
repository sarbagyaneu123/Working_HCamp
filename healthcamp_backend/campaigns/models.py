from django.db import models


class Campaign(models.Model):
    TYPE_CHOICES = (
        ("vaccination", "Vaccination"),
        ("checkup", "Health Checkup"),
        ("awareness", "Awareness"),
        ("other", "Other"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    date = models.DateField()
    helpline_number = models.CharField(max_length=30, blank=True)
    maps_url = models.URLField(blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    image_url = models.URLField(blank=True)
    vaccines = models.ManyToManyField("Vaccine", related_name="campaigns", blank=True)
    medicines = models.ManyToManyField("Medicine", related_name="campaigns", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self) -> str:
        return self.title


class Vaccine(models.Model):
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=120, blank=True)
    age_group = models.CharField(max_length=120, blank=True)
    timing = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=120, blank=True)
    age_group = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    availability = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
