from django.contrib import admin
import orders.models as model

# Register your models here.
admin.site.register(model.Usuario)
admin.site.register(model.Pizza)
admin.site.register(model.TamañoPizza)
admin.site.register(model.TipoPizza)