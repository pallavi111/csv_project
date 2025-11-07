from django.db import models

STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('PROCESSING', 'Processing'),
    ('COMPLETED', 'Completed'),
    ('FAILED', 'Failed'),
]

class CSVUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_records = models.IntegerField(default=0)
    duplicate_count = models.IntegerField(default=0)
    processing_time = models.FloatField(default=0.0)  # in seconds

    def __str__(self):
        return f"{self.file.name} - {self.status}"

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    age = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    upload = models.ForeignKey(CSVUpload, on_delete=models.CASCADE, related_name='people')
    is_duplicate = models.BooleanField(default=False)  # new field

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
