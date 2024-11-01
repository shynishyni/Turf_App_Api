from django.db import models
from django.utils import timezone

class UserDetailsTable(models.Model):
   
    user_id = models.CharField(max_length=200, unique=True, editable=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.CharField(max_length=10, null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    address = models.CharField(max_length=300, null=True, blank=True, default=None)
    latitude = models.FloatField(null=True, blank=True, default=None)
    longitude = models.FloatField(null=True, blank=True, default=None)
    city = models.CharField(max_length=200, null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.user_id:
            year = timezone.now().year
            last_user_id = UserDetailsTable.objects.filter(user_id__startswith=str(year)).order_by('-user_id').first()
            if last_user_id:
                last_id_num = int(last_user_id.user_id[len(str(year)):])
                new_id_num = last_id_num + 1
            else:
                new_id_num = 1
            self.user_id = f"{year}{new_id_num:03d}"
    
        super().save(*args, **kwargs)

class TurfDetails(models.Model):
    TURF_TYPE_CHOICES = [
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor'),
    ]

    SURFACE_TYPE_CHOICES = [
        ('artificial', 'Artificial Grass'),
        ('natural', 'Natural Grass'),
        ('concrete', 'Concrete'),
    ]

    class Status(models.IntegerChoices):
        VERIFIED = 1, 'Verified'
        BLOCKED = 2, 'Blocked'
        PENDING = 3, 'Pending'

    turf_name = models.CharField(max_length=100)
    turf_address = models.TextField()
    turf_city = models.CharField(max_length=50)
    turf_state = models.CharField(max_length=50)
    turf_zip_code = models.CharField(max_length=10)
    turf_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    turf_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    turf_type = models.CharField(max_length=10, choices=TURF_TYPE_CHOICES)
    surface_type = models.CharField(max_length=20, choices=SURFACE_TYPE_CHOICES)
    size = models.CharField(max_length=20, help_text="E.g., 5-a-side, 7-a-side, 11-a-side")
    capacity = models.PositiveIntegerField(help_text="Maximum players allowed")
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)    
    opening_time = models.TimeField( blank=True, null=True)
    closing_time = models.TimeField( blank=True, null=True)
    closed_days = models.CharField(max_length=50, help_text="Days turf is closed, e.g., Sunday") 
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    peak_hour_rate = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    owner_name = models.CharField(max_length=200)
    turf_contact_phone = models.CharField(max_length=10)
    turf_contact_email = models.EmailField()
    images = models.JSONField(default=list)
    # image1 = models.ImageField(upload_to='turf_images/', default='turf_images/download_1.jpeg', blank=True, null=True)
    # image2 = models.ImageField(upload_to='turf_images/', default='turf_images/download_1.jpeg', blank=True, null=True)
    # image3 = models.ImageField(upload_to='turf_images/', default='turf_images/download_1.jpeg', blank=True, null=True)
    # image4 = models.ImageField(upload_to='turf_images/', default='turf_images/download_1.jpeg', blank=True, null=True)
    # image5 = models.ImageField(upload_to='turf_images/', default='turf_images/download_1.jpeg', blank=True, null=True)

    def __str__(self):
        return self.turf_name  # Updated __str__ method to use turf_name

# class TurfImage(models.Model):
#     turf = models.ForeignKey(TurfDetails, related_name='images', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='turf_images/')

#     def __str__(self):
#         return f"Image for {self.turf.turf_name}"


class TurfBookingDeatils(models.Model):
    user_id = models.CharField(max_length=200, unique=True, editable=False)
    turf_name = models.CharField(max_length=100)
    starting_time = models.TimeField( blank=False, null=False)
    ending_time = models.TimeField( blank=False, null=False)
    date= models.DateField(blank=False, null=False)
    total_ammount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name