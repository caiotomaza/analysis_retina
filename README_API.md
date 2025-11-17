# API para integração com React

Este README descreve como rodar a API que serve o modelo `modelo_cnn_otimizado.h5` e como chamá-la a partir de um app React.

1) Instalar dependências (recomendo venv):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

2) Rodar a API (desenvolvimento):

```bash
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

Endpoint principal
- POST /predict
  - Form data: `file` (arquivo de imagem)
  - Query param opcional: `topk` (inteiro)
  - Retorna JSON com `top` (lista das top-k previsões) e `all` (todas as classes com probabilidades)

Exemplo de chamada fetch do React (client-side):

```js
async function predictImage(file) {
  const form = new FormData();
  form.append('file', file);

  const resp = await fetch('http://localhost:8000/predict?topk=5', {
    method: 'POST',
    body: form,
  });
  if (!resp.ok) throw new Error(await resp.text());
  const data = await resp.json();
  return data; // { top: [...], all: [...] }
}
```

Notas
- Ajuste a política de CORS no `backend/app.py` antes de ir para produção.
- Verifique se `modelo_cnn_otimizado.h5` está na raiz do projeto (mesmo nível de `backend/`).
- Substitua `labels_example.txt` por um arquivo com os nomes reais das 46 classes.

Redimensionamento automático
- Este backend aceita imagens em alta resolução (por exemplo PNG de 2144x1424) e
  irá redimensioná-las automaticamente para 224x224 antes da inferência, que é o
  tamanho exigido pelo modelo CNN criado no notebook. Não é necessário redimensionar
  no cliente React — o backend já faz isso.

Se quiser, posso gerar um componente React simples que envia a imagem e exibe o resultado (um exemplo pronto para copiar/colar).
