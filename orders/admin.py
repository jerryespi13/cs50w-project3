from django.contrib import admin
import orders.models as model
from.models import User

# Register your models here.
admin.site.register(User)
admin.site.register(model.Pizza)
admin.site.register(model.TamañoPizza)
admin.site.register(model.TipoPizza)