from django.contrib import admin
import orders.models as model
from.models import User

# Register your models here.
#admin.site.register(model.Tamaño)
admin.site.register(User)
admin.site.register(model.Pizza)
admin.site.register(model.Topping)
admin.site.register(model.Sub)
admin.site.register(model.Extra)
admin.site.register(model.DinnerPlate)
admin.site.register(model.Salads)
admin.site.register(model.Pasta)
admin.site.register(model.Orden)
admin.site.register(model.OrdenProducto)
admin.site.register(model.Tamaño)