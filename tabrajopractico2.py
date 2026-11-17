import json, os
from pathlib import Path

class StockInvalidoError(Exception):
        pass

class DispositivoEcológico:
    codigo: str
    nombre: str
    __stock: int

    def __init__(self, codigo: str, nombre: str, stock: int):
        self.codigo = codigo
        self.nombre = nombre
        self.stock = stock  
    
    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, valor):
        try:
            self.__stock = int(valor)
            if self.__stock < 0:
                raise StockInvalidoError("El stock debe ser mayor o igual a 0")
        except ValueError:
            raise StockInvalidoError("El valor asignado en STOCK debe ser numérico entero") 
        except TypeError:
            raise StockInvalidoError("El valor asignado a STOCK no puede ser nulo")
        
    def ficha_tecnica(self, imprimir: bool = False) -> str:
        ficha = f"codigo: {self.codigo} | nombre: {self.nombre} | stock: {self.stock}"
        if imprimir: print(ficha)
        return ficha 

    def to_dict(self) -> dict: 
        return {"codigo": self.codigo, "nombre": self.nombre, "stock": self.stock}
        
class PanelSolar(DispositivoEcológico):
    potencia_w: float
    eficiencia: float

    def __init__(self, codigo: str, nombre: str, stock: int, potencia_w: float, eficiencia: float):
        super().__init__(codigo, nombre, stock)
        self.potencia_w = potencia_w
        self.eficiencia = eficiencia

    def ficha_tecnica(self, imprimir: bool = False) -> str:
        ficha = super().ficha_tecnica()
        ficha += f" | potencia w: {self.potencia_w}W | eficiencia: {self.eficiencia}%"
        if imprimir: print(ficha)
        return ficha 

    def to_dict(self) -> dict:
        resultado = super().to_dict()        
        resultado["potencia_w"] = self.potencia_w
        resultado["eficiencia"] = self.eficiencia
        return resultado

class GestorInventario:
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos: list[DispositivoEcológico | PanelSolar], ruta_archivo: str = "catalogo_ecotech.json") -> bool: 
        
        ruta = Path(ruta_archivo)
        if ruta.parent != Path(''):
            ruta.parent.mkdir(parents=True, exist_ok=True)
            
        with open(ruta, "w") as archivo:
            lista_dispositivos_serializados = [elemento.to_dict() for elemento in lista_dispositivos]
            json.dump(lista_dispositivos_serializados, archivo, indent=4)
        print(f"\n[+] Catálogo exportado exitosamente a '{ruta_archivo}'.")
        return True

dispositivo_1 = DispositivoEcológico("DISP-1", "Inversor Solar Base", 15)        
dispositivo_2 = DispositivoEcológico("DISP-2", "Batería de Litio", 8)

panel_1 = PanelSolar("PAN-01", "Panel Solar  Monocromo ", 25, 450.0, 21.5)        
panel_2 = PanelSolar("PAN-02", "Panel Complejo Multidireccional", 12, 380.0, 18.0)
panel_3 = PanelSolar("PAN-03", "Panel Bifacial ", 30, 550.0, 23.2)

# Prueba de StockInvalidoError, valor negativo
try:
    dispositivo_erroneo_1 = DispositivoEcológico("ERR-1", "Dispositivo Erróneo", -10)            
except StockInvalidoError as e: 
    print(f"Excepción capturada al instanciar un Dispositivo Ecológico con stock negativo: {e}")    

# Prueba 2: Captura de StockInvalidoError,valor nulo (None)
try:
    panel_1.stock = None            
except StockInvalidoError as e: 
    print(f"Excepción capturada al modificar un Dispositivo Ecológico con stock nulo: {e}") 

print("\n-Diccionarios individuales-")
print(dispositivo_1.to_dict())
print(panel_1.to_dict())
 
lista_dispositivos: list[DispositivoEcológico | PanelSolar] = [
    dispositivo_1,
    dispositivo_2,
    panel_1,
    panel_2,
    panel_3
]

print("\n--- Fichas Técnicas Comerciales ---")
for dispositivo in lista_dispositivos:
    dispositivo.ficha_tecnica(True)

GestorInventario.guardar_catalogo_json(lista_dispositivos, "catalogo_ecotech.json")