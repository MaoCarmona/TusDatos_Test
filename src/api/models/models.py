from pydantic import BaseModel
from typing import List, Optional

class Detalle(BaseModel):
    id_judicatura: int
    nombre_judicatura: str
    ciudad: str
    lst_incidente_judicatura: List[str]

class IncidenteJudicatura(BaseModel):
    id_incidente_judicatura: int
    id_movimiento_juicio_incidente: int
    id_judicatura_destino: int
    fecha_crea: str
    incidente: str
    lst_litigante_actor: List[str]
    lst_litigante_demandado: List[str]

class Litigante(BaseModel):
    tipo_litigante: str
    nombres_litigante: str
    representado_por: Optional[str]
    id_litigante: int

class Actuacion(BaseModel):
    codigo: str
    id_judicatura: int
    id_juicio: int
    fecha: str
    tipo: str
    actividad: str
    visible: bool
    origen: str
    id_movimiento_juicio_incidente: int
    ie_tabla_referencia: str
    ie_documento_adjunto: str
    escape_out: Optional[str]
    uuid: Optional[str]
    alias: Optional[str]
    nombre_archivo: Optional[str]
    tipo_ingreso: Optional[str]
    id_tabla_referencia: Optional[int]

class Proceso(BaseModel):
    id: int
    id_juicio: int
    estado_actual: str
    id_materia: int
    id_provincia: int
    id_canton: int
    id_judicatura: int
    nombre_delito: str
    fecha_ingreso: str
    nombre: str
    cedula: str
    id_estado_juicio: int
    nombre_materia: str
    nombre_estado_juicio: str
    nombre_judicatura: str
    nombre_tipo_resolucion: str
    nombre_tipo_accion: str
    fecha_providencia: str
    nombre_providencia: str
    nombre_provincia: str
    ie_documento_adjunto: str
    documento: Optional[str]
    type: Optional[str]
    detalles: Optional[List[Detalle]]
    actuaciones: Optional[List[Actuacion]]
