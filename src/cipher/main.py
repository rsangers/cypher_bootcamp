from fastapi import FastAPI
from pydantic import BaseModel

from cipher.constants import ALPHABET
from cipher.solver import solve_cipher
from cipher.utils import Vocabulary

app = FastAPI()


vocab = Vocabulary('./enwiki-2023-04-13.txt')

class Message(BaseModel):
    ciphertext: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/solve/echo")
async def echo(message: Message):
    return {
        "ciphertext": message.ciphertext,
        "plaintext": message.ciphertext,
        "mapping": {x: x for x in ALPHABET}
    }

@app.post("/api/solve/en")
async def echo(message: Message):
    ciphertext = message.ciphertext
    plaintext, mapping = solve_cipher(ciphertext, vocab)
    return {
        "ciphertext": message.ciphertext,
        "plaintext": plaintext,
        "mapping": mapping
    }