from pydantic import BaseModel

class Assist(BaseModel):   
    thread_id:str
    name:str