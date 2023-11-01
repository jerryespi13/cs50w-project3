from django.contrib import admin
import orders.models as model
from.models import User

# Register your models here.
#admin.site.register(model.Tamaño)
admin.site.register(User)
admin.site.register(model.Pizza)
admin.site.register(model.TipoPizza)
admin.site.register(model.Sub)
admin.site.register(model.Extra)
admin.site.register(model.DinnerPlate)
admin.site.register(model.Salads)