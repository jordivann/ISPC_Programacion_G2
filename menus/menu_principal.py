from menus.menu_pacientes import menu_pacientes
from menus.menu_medicos import menu_medicos
from menus.menu_empleados import menu_empleados
from menus.menu_turno import menu_turnos

def menu_principal():
    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Pacientes")
        print("2. Medicos")
        print("3. Empleados")
        print("4. Turnos")
        print("0. Salir")
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            menu_pacientes()
        elif opcion == "2":
            menu_medicos()
        elif opcion == "3":
            menu_empleados()
        elif opcion == "4":
            menu_turnos()
        elif opcion == "0":
            break
        else:
            print("Opcion invalida. Por favor, intente nuevamente.")