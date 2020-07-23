from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Intersection)
admin.site.register(Road)
admin.site.register(Artefact)
admin.site.register(TrafficLight)
admin.site.register(Network)