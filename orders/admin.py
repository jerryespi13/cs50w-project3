from django.contrib import admin
import orders.models as model
from.models import User

class OrdenProductoInline(admin.TabularInline):
    model = model.OrdenProducto
    extra = 0

class OrdenAdmin(admin.ModelAdmin):
    inlines = [OrdenProductoInline]
    list_display=('id', 'fecha', 'estado', 'usuario', 'total')
    list_editable=('estado',)

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
admin.site.register(model.Orden, OrdenAdmin)
admin.site.register(model.OrdenProducto)
admin.site.register(model.Tamaño)