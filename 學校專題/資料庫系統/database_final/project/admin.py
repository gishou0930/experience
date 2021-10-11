from django.contrib import admin

# Register your models here.
from .models import User
from .models import State
from .models import Products
from .models import ProductKind
from .models import Pay
from .models import Buy
admin.site.register(User)
admin.site.register(State)
admin.site.register(Products)
admin.site.register(ProductKind)
admin.site.register(Pay)
admin.site.register(Buy)