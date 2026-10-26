# 02 · Equipo

[← Volver al README](../README.md)

Equipo mínimo del [Plan de acción MVP](biblia/05-plan-de-accion-mvp.md). Detalle completo y mensaje original en [Freelancers México](biblia/06-freelancers-mexico.md).

## Roles

| Rol | Quién | Qué hace | Costo en el modelo |
|---|---|---|---|
| Director creativo / Product Owner | Ricardo López Reyero | Usa la biblia de diseño como fuente de verdad; aprueba layout, escala y cada zona | 8,000 USD/mes |
| Environment Artist (freelance, Unreal) | Por contratar | Construye la isla con asset packs: topografía, vegetación, playas, caminos, edificios, luz de día/atardecer/noche; deja terminadas 1 habitación, 1 villa y el restaurante | 5,000 USD/mes |
| Technical Artist / Game Developer (freelance) | Por contratar | Configura el proyecto UE5, movimiento y cámara, interacciones (puertas, luces, sentarse), UI del menú y hora del día, NPC simples, optimización | 6,000 USD/mes |
| Soporte / operación | Más adelante | Atención a usuarios y operación del mundo | 6,000 USD/mes |

Los costos son los supuestos del [modelo financiero](03-modelo-financiero.md); no son ofertas.

## Candidatos sugeridos (Upwork · «Unreal Engine Developers in Mexico»)

| Perfil | Nombre | Ciudad | Para |
|---|---|---|---|
| Environment / 3D Artist | Antonio C. | Querétaro | Isla, resort, vegetación, luz |
| Technical Artist / Game Developer | Luis L. | Zapopan | Interacciones y lógica en Unreal |

Antes de contratar: revisar calificaciones, portafolio y reseñas. Se pueden cambiar por otros freelancers mexicanos que encajen mejor.

## Cómo contactarlos

1. Mandar el mensaje modelo (abajo) por Upwork, adaptado a cada rol.
2. Adjuntar el PDF del plan de acción ([`fuentes/pdf/Plan_de_Accion_Isla_3D_MVP.pdf`](../fuentes/pdf/Plan_de_Accion_Isla_3D_MVP.pdf)) y 2–3 imágenes de [`referencias/renders/`](../referencias/renders/).
3. Llamada corta: tiempos, presupuesto y acceso a este repo.

### Mensaje modelo

> Hola [Nombre],
>
> Soy fundador de un proyecto de resort/isla virtual en Unreal Engine 5. Ya tengo un documento muy detallado con la topografía, edificios, habitaciones, villas, amenities y un menú gastronómico premium, y ahora quiero crear un MVP jugable de la isla.
>
> Busco a alguien con tu perfil para:
>
> – [Environment Artist] Montar la isla con asset packs (resort tropical, hotel, villas, marina), ajustar iluminación y vegetación, y dejar 1 habitación, 1 villa y 1 restaurante muy bien resueltos.
>
> – [Technical Artist / Dev] Programar el movimiento del jugador, interacciones básicas (abrir puertas, luces, UI de menú, etc.) y optimizar la escena en Unreal.
>
> ¿Te interesaría tener una llamada corta para contarte más del proyecto, tiempos y presupuesto?
>
> Gracias,
> Ricardo

## Cómo trabajan con este repo

- La **biblia** (`docs/biblia/`) no se edita: si algo cambia, se escribe un documento nuevo con versión.
- Los **datos** (`data/*.json`) son lo que el juego lee: menú del restaurante, flora a sembrar, fauna, tiendas.
- El proyecto de Unreal vive en `unreal/IslaEncantada/` con **Git LFS** ([04-unreal.md](04-unreal.md)).
- Cada entrega de fase deja capturas en `referencias/avances/AAAA-MM-DD/`.

<!-- RLR · Ricardo López Reyero · rev 181218 -->
