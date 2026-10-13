from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.db import migrations


def crear_datos_iniciales(apps, schema_editor):
    Editorial = apps.get_model("catalogo", "Editorial")
    Libro = apps.get_model("catalogo", "Libro")
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    User = apps.get_model("auth", "User")

    editoriales = {}
    datos_editoriales = [
        {
            "nombre": "Editorial Planeta",
            "pais": "España",
            "ciudad": "Barcelona",
            "email": "contacto@planetadelibros.com",
        },
        {
            "nombre": "Penguin Random House",
            "pais": "Chile",
            "ciudad": "Santiago",
            "email": "contacto@penguinrandomhouse.cl",
        },
        {
            "nombre": "Editorial Universitaria",
            "pais": "Chile",
            "ciudad": "Santiago",
            "email": "contacto@universitaria.cl",
        },
    ]
    for datos in datos_editoriales:
        editorial, _ = Editorial.objects.update_or_create(
            nombre=datos["nombre"],
            defaults=datos,
        )
        editoriales[editorial.nombre] = editorial

    datos_libros = [
        {
            "titulo": "Cien años de soledad",
            "autor": "Gabriel García Márquez",
            "isbn": "978-0307474728",
            "precio": Decimal("12990"),
            "fecha_publicacion": "1967-05-30",
            "editorial": "Editorial Planeta",
        },
        {
            "titulo": "El principito",
            "autor": "Antoine de Saint-Exupéry",
            "isbn": "978-0156012195",
            "precio": Decimal("8990"),
            "fecha_publicacion": "1943-04-06",
            "editorial": "Editorial Planeta",
        },
        {
            "titulo": "Sapiens",
            "autor": "Yuval Noah Harari",
            "isbn": "978-0062316097",
            "precio": Decimal("15990"),
            "fecha_publicacion": "2011-01-01",
            "editorial": "Penguin Random House",
        },
        {
            "titulo": "1984",
            "autor": "George Orwell",
            "isbn": "978-0451524935",
            "precio": Decimal("10990"),
            "fecha_publicacion": "1949-06-08",
            "editorial": "Penguin Random House",
        },
        {
            "titulo": "La casa de los espíritus",
            "autor": "Isabel Allende",
            "isbn": "978-1501117015",
            "precio": Decimal("11990"),
            "fecha_publicacion": "1982-01-01",
            "editorial": "Editorial Universitaria",
        },
        {
            "titulo": "Poema de Chile",
            "autor": "Gabriela Mistral",
            "isbn": "978-9561112345",
            "precio": Decimal("9990"),
            "fecha_publicacion": "1967-01-01",
            "editorial": "Editorial Universitaria",
        },
    ]
    for datos in datos_libros:
        datos["editorial"] = editoriales[datos["editorial"]]
        Libro.objects.update_or_create(
            isbn=datos["isbn"],
            defaults=datos,
        )

    permisos = {
        permiso.codename: permiso
        for permiso in Permission.objects.filter(
            content_type__app_label="catalogo",
            content_type__model__in=("editorial", "libro"),
        )
    }

    operador, _ = Group.objects.get_or_create(name="Operador")
    operador.permissions.set(
        [
            permisos[f"{accion}_{modelo}"]
            for modelo in ("editorial", "libro")
            for accion in ("view", "add", "change")
        ]
    )

    auditor, _ = Group.objects.get_or_create(name="Auditor")
    auditor.permissions.set(
        [
            permisos[f"view_{modelo}"]
            for modelo in ("editorial", "libro")
        ]
    )

    jefe, _ = User.objects.get_or_create(username="jefe")
    jefe.is_staff = True
    jefe.is_superuser = True
    jefe.password = make_password("Inacap.2026")
    jefe.save()

    operador_usuario, _ = User.objects.get_or_create(username="operador")
    operador_usuario.password = make_password("Inacap.2026")
    operador_usuario.is_staff = True
    operador_usuario.is_superuser = False
    operador_usuario.save()
    operador_usuario.groups.set([operador])

    auditor_usuario, _ = User.objects.get_or_create(username="auditor")
    auditor_usuario.password = make_password("Inacap.2026")
    auditor_usuario.is_staff = True
    auditor_usuario.is_superuser = False
    auditor_usuario.save()
    auditor_usuario.groups.set([auditor])


def eliminar_datos_iniciales(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Group = apps.get_model("auth", "Group")
    Libro = apps.get_model("catalogo", "Libro")
    Editorial = apps.get_model("catalogo", "Editorial")

    User.objects.filter(username__in=("operador", "auditor")).delete()
    Group.objects.filter(name__in=("Operador", "Auditor")).delete()
    Libro.objects.filter(
        isbn__in=(
            "978-0307474728",
            "978-0156012195",
            "978-0062316097",
            "978-0451524935",
            "978-1501117015",
            "978-9561112345",
        )
    ).delete()
    Editorial.objects.filter(
        nombre__in=(
            "Editorial Planeta",
            "Penguin Random House",
            "Editorial Universitaria",
        )
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("catalogo", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(crear_datos_iniciales, eliminar_datos_iniciales),
    ]
