from django.db import models


class Editorial(models.Model):
    nombre = models.CharField(max_length=120)
    pais = models.CharField(max_length=80)
    ciudad = models.CharField(max_length=80)
    email = models.EmailField()

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Editorial"
        verbose_name_plural = "Editoriales"

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=120)
    isbn = models.CharField(max_length=17, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    fecha_publicacion = models.DateField()
    editorial = models.ForeignKey(
        Editorial,
        on_delete=models.CASCADE,
        related_name="libros",
    )

    class Meta:
        ordering = ["titulo"]
        verbose_name = "Libro"
        verbose_name_plural = "Libros"

    def __str__(self):
        return self.titulo
