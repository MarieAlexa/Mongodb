from pymongo import MongoClient
from bson.objectid import ObjectId

def conectar_db(uri="mongodb://localhost:27017/", db_name="recetas_db"):
    try:
        cliente = MongoClient(uri)
        db = cliente[db_name]
        return db
    except Exception as e:
        print("Error al conectar a la base de datos: " + str(e))
        return None


def agregar_receta(db, nombre, ingredientes, pasos):
    nueva_receta = {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "pasos": pasos
    }
    try:
        db.recetas.insert_one(nueva_receta)
        print("Receta agregada con éxito.")
    except Exception as e:
        print(f"Error al agregar la receta: {e}")


def actualizar_receta(db, nombre, nuevos_ingredientes, nuevos_pasos):
    resultado = db.recetas.update_one(
        {"nombre": nombre},
        {"$set": {"ingredientes": nuevos_ingredientes, "pasos": nuevos_pasos}}
    )
    if resultado.modified_count > 0:
        print("Receta actualizada con éxito.")
    else:
        print("Error: No se encontró una receta con ese nombre.")


def eliminar_receta(db, nombre):
    resultado = db.recetas.delete_one({"nombre": nombre})
    if resultado.deleted_count > 0:
        print("Receta eliminada con éxito.")
    else:
        print("Error: No se encontró una receta con ese nombre.")


def ver_recetas(db):
    recetas = db.recetas.find()
    if recetas.count() > 0:
        print("Listado de recetas:")
        for receta in recetas:
            print(f"- {receta['nombre']}")
    else:
        print("No hay recetas disponibles.")


def buscar_receta(db, nombre):
    receta = db.recetas.find_one({"nombre": nombre})
    if receta:
        print(f"\nIngredientes:\n{receta['ingredientes']}\n")
        print(f"Pasos:\n{receta['pasos']}\n")
    else:
        print("Error: No se encontró una receta con ese nombre.")


def menu(db):
    while True:
        print("\n--- Libro de Recetas ---")
        print("1. Agregar nueva receta")
        print("2. Actualizar receta existente")
        print("3. Eliminar receta existente")
        print("4. Ver listado de recetas")
        print("5. Buscar ingredientes y pasos de receta")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Nombre de la receta: ")
            ingredientes = input("Ingredientes (separados por comas): ")
            pasos = input("Pasos: ")
            agregar_receta(db, nombre, ingredientes, pasos)
        elif opcion == '2':
            nombre = input("Nombre de la receta a actualizar: ")
            nuevos_ingredientes = input("Nuevos ingredientes (separados por comas): ")
            nuevos_pasos = input("Nuevos pasos: ")
            actualizar_receta(db, nombre, nuevos_ingredientes, nuevos_pasos)
        elif opcion == '3':
            nombre = input("Nombre de la receta a eliminar: ")
            eliminar_receta(db, nombre)
        elif opcion == '4':
            ver_recetas(db)
        elif opcion == '5':
            nombre = input("Nombre de la receta a buscar: ")
            buscar_receta(db, nombre)
        elif opcion == '6':
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == '__main__':
    db = conectar_db()
    if db is not None:
        menu(db)

