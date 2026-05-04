from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "mssql+pyodbc://MSI/Northwind"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

# Leer tablas
clientes  = pd.read_sql("SELECT CustomerID, CompanyName, Country FROM Customers", engine)
ordenes   = pd.read_sql("SELECT OrderID, CustomerID, OrderDate, Freight FROM Orders", engine)
detalle   = pd.read_sql("SELECT OrderID, ProductID, UnitPrice, Quantity FROM [Order Details]", engine)

# Merge 1: ordenes + clientes
resultado = pd.merge(ordenes, clientes, on='CustomerID', how='left')

# Merge 2: resultado + detalle
resultado = pd.merge(resultado, detalle, on='OrderID', how='left')

# Columna calculada: total por línea
resultado['total'] = resultado['UnitPrice'] * resultado['Quantity']

# Análisis: ventas totales por país
ventas_pais = resultado.groupby('Country')['total'].sum().reset_index()
ventas_pais = ventas_pais.sort_values('total', ascending=False)

print(ventas_pais.head(10))

# Guardar resultado
ventas_pais.to_csv('ventas_por_pais.csv', index=False)
