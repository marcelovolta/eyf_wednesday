# Clase 02

En esta clase promulgan el uso de Python con DuckDB con SQL para manejar los datos en lugar de Pandas, o Polars.
Para esto instalan DuckDB con `pip install duckdb` 
También instalan JupySQL con `pip install jupysql`  Esta última les permite usar SQL contra bases DuckDB y otras directamente en los notebooks de Jupyter. 
Utiliza magics: `%sql` y `%%sql`
Ejemplos de como utilizarlo se encuentran en [Joa_z501_Feature_Engineering_en_SQL](https://github.com/marcelovolta/dmeyf2025/blob/main/src/monday/z501_Feature_Engineering_en_SQL.ipynb)
Esto es muy directo para hacer feature engineering directamente en SQL en el contexto de un notebook de Python. 
Ojo que DuckDB tiene funciones propias de ventana y otras que no existen en SQL y sirven muy bien para feature Engineering. Miralas en [DuckDB SQL Documentation](https://duckdb.org/docs/stable/sql/introduction)

En esta clase se ve: 
- Manejo de los logs con la clase `Logger` de la biblioteca `logging` de Python en lugar de manejo de archivos
- Uso de `try... except` y algunos criterios generales de cuando aplicarlo (función `cargar_datos` del script `data_loader.py`)
- Retorno de más de un tipo especificado en la definición de una función (función `cargar_datos` del script `data_loader.py`)
- Uso del archivo `__init__.py`: Se pone este archivo para señalar que, más que un directorio, es un paquete que contiene módulos importables. En la clase señalaron que se pone vacío, pero se puede poner código que facilite la importación, y aún pueden ponerse importaciones de otras bibliotecas. Por ejemplo, en el código que dio Joaquín, el archivo main está en la raíz, mientras que el directorio src tiene los módulos importables. Uno de estos módulos es `data_loader.py`, entonces en main aparece esta línea: `from src.data_loader import cargar_datos` Pero, si en `__init__.py` agrego: `from .data_loader import cargar_datos` , desde main puedo reemplazar `from src.data_loader import cargar_datos` por `from src import cargar_datos`. Es decir, me independizo de la estructura interna de `src`; Sólo debo recordar que la función se llama `cargar_datos()`. Btw, voy a cambiar los nombres en Español por nombres en Inglés para que este código sirva allende los mares. 
- Generación de lags con Duck DB usando SQL sobre memory donde los datos están cargados por Pandas dataframe. Es posible usar DuckDB para filtrar, transformar y crear features usando SQL después de cargar los datos con Pandas, con Polars o directamente con DuckDB. Para decidir cuál usar, miré [este artículo](https://www.codecentric.de/en/knowledge-hub/blog/duckdb-vs-dataframe-libraries) donde comparan la performance de los tres y se nota que Pandas es el de peor performance de los tres (alto tiempo de proceso, alto uso de memoria), mientras que Polars y DuckDB van muy cercanos uno del otro. Para poder comparar dejo los tres métodos de carga de los datos, y, en todos los casos, proceso los features con SQL usando DuckDB. El método `load_csv()` de Polar da un error con los datos: 
```
2026-02-17 18:29:28 - ERROR - src.data_loader - 23 - Error when trying to load data: could not parse `1161306.32` as dtype `i64` at column 'mprestamos_prendarios' (column number 36)

The current offset in the file is 53932 bytes.

You might want to try:
- increasing `infer_schema_length` (e.g. `infer_schema_length=10000`),
- specifying correct dtype with the `schema_overrides` argument
- setting `ignore_errors` to `True`,
- adding `1161306.32` to the `null_values` list.

Original error: ```invalid primitive value found during CSV parsing```
Traceback (most recent call last):
```
 Por eso cargo los datos con Pandas que no da error y después uso DuckDB para feature engineering.
 Por lo que leí en [este error en Stack Overflow](https://es.stackoverflow.com/questions/610759/error-el-leer-un-csv-con-polars), Polars usa las 100 primeras filas para inferir el tipo de dato; lo que debe estar sucediendo es que en las 100 primeras este calor debe ser entero (i64) pero más adelante se encuentra con un decimal y no lo puede parsear. Habría que sentarse con el dataset y armar una buena especificación de tipos por columna con dtype. Aquí es donde se hace evidente que la lentitud de Pandas paga dividendos en simplicidad: Pandas no tiene problemas en cargar este dataset. De todos modos, cuando uno analiza un dataset hay que conocer primero los tipos de columna con los que va a trabajar, así que quizá primero un análisis exploratorio con Pandas, luego el procesamiento con Polars para cargar más rápido. 
 La otra opción es hacer todo con DuckDB. En [este artículo](https://www.codemag.com/Article/2305071/Using-DuckDB-for-Data-Analytics)se muestra como cargar un CSV usando DuckDB y pasándolo a un Pandas Dataframe directamente sin cargarlo en Pandas primero. La forma alternativa es usar DuckDB con una sentencia `SELECT` donde el `FROM` es directamente el archivo, como se ve en la [documentación de DuckDB](https://duckdb.org/docs/stable/data/csv/overview)
La posibilidad de convertir un query en un pandas dataframe se explica muy sucintamente en la documentación de DuckDB: https://duckdb.org/docs/stable/guides/python/export_pandas 
Con este approach, la carga de datos de competencia02, competencia03, concatenación y head() + tail() lleva 32 segundos. Con Pandas lleva 23 segundos. Es decir, casi no hay diferencia, pero en este caso es mejor con Pandas sólo y después DuckDB para los queries.

Escribí una implementación diferente de lags y delta lags, en una misma función puse ambas, con la posibilidad de especificar si quiero los delta lags o no.
Probé que el código corre para el dataset de competencia_3. Si pongo el de competencia_2 termina cerrándose el proceso por el uso de memoria. 
Necesito usar pruebas para verificar que el código corre bien y calcula lo que tiene que calcular. 
Pero antes de meterme con eso, quiero ver cómo lo solucionan en la clase. 
