# Crawler para detectar errores 4XX en un dominio

## Objetivo

Este proyecto consiste en un crawler desarrollado en Python y Selenium que explora un dominio completo, detecta URLs con códigos de error HTTP 4XX y genera un informe en formato CSV.

## Cómo funciona

- Navega recursivamente por todas las páginas dentro del dominio.
- Comprueba el código HTTP de cada URL encontrada.
- Registra todas las URLs que devuelven errores 4XX junto con la página de origen.
- Genera un informe CSV con los resultados.

## Uso

1. Instalar dependencias:
2. Ejecutar el script:
3. El informe se guardará como `errors_4xx.csv`.

## Decisiones técnicas

- Uso de Selenium para ejecutar JavaScript y obtener enlaces dinámicos.
- Uso de `requests.head` para comprobar código HTTP de manera eficiente.
- Recursión para exploración profunda con control de URLs visitadas.
- Generación de CSV para facilitar análisis posterior.

## Limitaciones y mejoras futuras

- No se controla profundidad máxima (puede añadirse).
- No maneja autenticaciones ni captchas.
- Se podría optimizar para paralelizar peticiones.

## Autor

Biel Prous Espinosa

