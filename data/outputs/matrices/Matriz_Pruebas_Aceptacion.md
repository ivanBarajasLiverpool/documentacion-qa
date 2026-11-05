# Matriz de Pruebas de Aceptación (MPA) — Módulo de Facturación Electrónica v2.4

## Contexto Funcional y Documentación de Referencia
> Según la documentación funcional (`data/inputs/context_docs/especificacion_facturacion.md`) y la URL del portal de reglas fiscales recopiladas por el subagente `investigador_contexto`:
> - Todo usuario que emita facturas CFDI 4.0 debe contar con el rol **Contabilidad_Emisor** activo.
> - El cliente receptor debe estar dado de alta previamente en el Catálogo de Clientes con su RFC validado.
> - El sistema calcula automáticamente el IVA (16%) al ingresar el importe unitario de una partida.

## Tabla Consolidada de Casos de Prueba

| ID del Caso | Condiciones Previas | N° Paso | Paso a Seguir (Automatizador) | Datos de Prueba | Resultado Esperado |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **MPA-FAC-001**<br>*(Emisión exitosa de factura nacional con cliente existente)* | • Usuario autenticado en el portal con rol `Contabilidad_Emisor`<br>• Cliente "Acme Corp S.A. de C.V." previamente registrado con RFC activo<br>• Folios fiscales disponibles en la serie `A` | 1 | Desplegar el menú lateral izquierdo y hacer clic en la opción "Facturación". | `N/A` | Se carga el panel principal de facturación mostrando el historial de comprobantes y el botón "Nueva Factura". |
| `MPA-FAC-001` | *(Ver paso 1)* | 2 | Hacer clic en el botón "Nueva Factura" ubicado en la esquina superior derecha. | `N/A` | Se abre el formulario de captura de factura con los campos de receptor y conceptos vacíos. |
| `MPA-FAC-001` | *(Ver paso 1)* | 3 | Ingresar el nombre o RFC del cliente en el campo de búsqueda "Cliente Receptor" y seleccionar la coincidencia de la lista desplegable. | `Cliente: "Acme Corp S.A. de C.V." \| RFC: "ACO1405209A1"` | El sistema autocompleta automáticamente la Razón Social, el Régimen Fiscal (`601 - General de Ley`) y el Código Postal (`06600`). |
| `MPA-FAC-001` | *(Ver paso 1)* | 4 | Seleccionar la opción correspondiente en el selector desplegable "Uso de CFDI". | `Uso de CFDI: "G03 - Gastos en general"` | El campo "Uso de CFDI" queda establecido con el valor `G03 - Gastos en general`. |
| `MPA-FAC-001` | *(Ver paso 1)* | 5 | Hacer clic en el botón "+ Agregar Concepto" dentro de la sección de partidas. | `N/A` | Se habilita una nueva fila editable para capturar clave de producto, cantidad, descripción y precio unitario. |
| `MPA-FAC-001` | *(Ver paso 1)* | 6 | Capturar la descripción del servicio, la cantidad y el precio unitario en la fila del concepto y presionar la tecla Tabulador. | `Descripción: "Servicio de Consultoría QA" \| Cantidad: "1" \| Precio Unitario: "15000.00"` | El sistema calcula y muestra en pantalla el Subtotal (`$15,000.00`), el IVA 16% (`$2,400.00`) y el Total (`$17,400.00`). |
| `MPA-FAC-001` | *(Ver paso 1)* | 7 | Hacer clic en el botón primario "Timbrar y Emitir Factura". | `N/A` | Se cierra el formulario y se muestra una notificación de confirmación verde con el folio fiscal UUID generado y los enlaces para descargar XML y PDF. |
