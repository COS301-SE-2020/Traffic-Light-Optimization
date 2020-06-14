from django.contrib import admin

# Register your models here.
from .models import Intersection
from .models import Road
from .models import Artefact


admin.site.register(Intersection)
admin.site.register(Road)
admin.site.register(Artefact)