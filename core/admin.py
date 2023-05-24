from django.contrib import admin

# Register your models here.
from .models import Challenge, Solve, CustomUser
admin.site.site_header = "CTF Platform Admin"
admin.site.register(CustomUser)
admin.site.register(Challenge)
admin.site.register(Solve)

