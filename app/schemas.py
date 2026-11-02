from pydantic import BaseModel

class DatiSensori(BaseModel):
    temperatura : float
    vibrazioni : float