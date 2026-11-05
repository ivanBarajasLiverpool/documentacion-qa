# Ejemplo Gold Standard de MPA

| ID del Caso | Condiciones Previas | N° Paso | Paso a Seguir (Automatizador) | Datos de Prueba | Resultado Esperado |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **MPA-AUTH-001**<br>*(Inicio de sesión con perfil Administrador)* | • Usuario registrado con estado `Activo`<br>• Rol `Admin_Global` asignado | 1 | Navegar a la pantalla de inicio de sesión del portal. | `N/A` | Se muestra el formulario de autenticación con los campos "Correo Electrónico", "Contraseña" y el botón "Ingresar". |
| `MPA-AUTH-001` | *(Ver paso 1)* | 2 | Ingresar las credenciales válidas en los campos "Correo Electrónico" y "Contraseña". | `Correo: "admin@empresa.com" \| Contraseña: "***"` | Los campos quedan poblados y el botón "Ingresar" se habilita. |
| `MPA-AUTH-001` | *(Ver paso 1)* | 3 | Hacer clic en el botón "Ingresar". | `N/A` | El sistema autentica al usuario y redirige al Dashboard Principal mostrando el menú de Administración. |
