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
