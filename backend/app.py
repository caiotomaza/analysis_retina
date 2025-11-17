from __future__ import annotations

import io
import os
from typing import List, Tuple

import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image

try:
    RESAMPLE_FILTER = Image.Resampling.LANCZOS
except Exception:
    RESAMPLE_FILTER = getattr(Image, 'LANCZOS', Image.BICUBIC)

try:
    import tensorflow as tf
    from tensorflow import keras
except Exception as e:
    raise RuntimeError("TensorFlow não está instalado ou não pode ser importado. Instale dependências do backend.")


APP_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(APP_DIR, '..', 'modelo_cnn_otimizado.h5')
LABELS_PATH = os.path.join(APP_DIR, '..', 'labels_example.txt')

app = FastAPI(title="Retina Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionItem(BaseModel):
    label: str
    probability: float


def load_model(path: str) -> keras.Model:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Modelo não encontrado em: {path}")
    model = keras.models.load_model(path, compile=False)
    return model


def get_input_shape(model: keras.Model) -> Tuple[int, int, int]:
    shape = None
    try:
        shape = model.input_shape
    except Exception:
        try:
            shape = model.inputs[0].shape
        except Exception:
            pass

    if not shape:
        raise RuntimeError("Não foi possível inferir o shape de entrada do modelo.")

    if len(shape) == 4:
        _, h, w, c = shape
    elif len(shape) == 3:
        h, w, c = shape
    else:
        raise RuntimeError(f"Formato inesperado de input_shape: {shape}")

    if h is None or w is None:
        h = h or 224
        w = w or 224

    c = int(c) if c is not None else 3
    return int(h), int(w), int(c)


def preprocess_image_file(file_bytes: bytes, target_size: Tuple[int, int], channels: int) -> np.ndarray:
    img = Image.open(io.BytesIO(file_bytes))

    if channels == 1:
        img = img.convert('L')
    else:
        img = img.convert('RGB')

    forced_size = target_size
    img = img.resize(forced_size, resample=RESAMPLE_FILTER)

    arr = np.asarray(img, dtype=np.float32)
    if channels == 1 and arr.ndim == 2:
        arr = arr[..., np.newaxis]
    elif channels != 1 and arr.ndim == 2:
        arr = np.stack([arr] * channels, axis=-1)

    arr = arr / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr


def safe_softmax(x: np.ndarray) -> np.ndarray:
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def load_labels(path: str, n_classes: int) -> List[str]:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            labels = [line.strip() for line in f if line.strip()]
        if len(labels) != n_classes:
            if len(labels) < n_classes:
                labels += [f'class_{i}' for i in range(len(labels), n_classes)]
            else:
                labels = labels[:n_classes]
        return labels
    return [f'class_{i}' for i in range(n_classes)]


@app.on_event("startup")
def startup_event():
    global model, input_h, input_w, input_c, labels
    try:
        model = load_model(MODEL_PATH)
    except Exception as e:
        model = None
        print(f"Aviso: não foi possível carregar o modelo na inicialização: {e}")
        return

    input_h, input_w, input_c = get_input_shape(model)
    try:
        out_shape = model.output_shape
        if isinstance(out_shape, tuple):
            n_classes = int(out_shape[-1])
        else:
            n_classes = int(out_shape[0][-1])
    except Exception:
        n_classes = 45

    labels = load_labels(LABELS_PATH, n_classes)
    print(f"Modelo carregado: {MODEL_PATH} | entrada: {input_h}x{input_w}x{input_c} | classes: {n_classes}")


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict")
async def predict(file: UploadFile = File(...), topk: int = Query(5, ge=1, le=100)):
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo não disponível no servidor")

    contents = await file.read()
    try:
        img_arr = preprocess_image_file(contents, (input_h, input_w), input_c)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar imagem: {e}")

    preds = model.predict(img_arr)
    if preds.ndim > 1:
        preds = preds[0]

    s = float(np.sum(preds))
    if not (0.9 <= s <= 1.1):
        probs = safe_softmax(preds)
    else:
        probs = preds / s

    n = probs.shape[0]
    lbls = labels if 'labels' in globals() else load_labels(LABELS_PATH, n)

    idx = np.argsort(probs)[::-1]
    topk = min(topk, n)
    resp_top = []
    for i in idx[:topk]:
        resp_top.append(PredictionItem(label=lbls[i], probability=float(probs[i])))

    full = [PredictionItem(label=lbls[i], probability=float(probs[i])) for i in range(n)]

    return {"top": resp_top, "all": full}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)