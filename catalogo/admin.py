from django.contrib import admin

from .models import Editorial, Libro


@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ("nombre", "pais", "ciudad", "email")
    list_filter = ("pais", "ciudad")
    search_fields = ("nombre", "pais", "ciudad", "email")


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "autor",
        "isbn",
        "precio_formateado",
        "fecha_publicacion",
        "editorial",
    )
    list_filter = ("editorial", "fecha_publicacion")
    search_fields = ("titulo", "autor", "isbn", "editorial__nombre")

    @admin.display(description="Precio")
    def precio_formateado(self, obj):
        return f"${obj.precio:,.0f}".replace(",", ".")
