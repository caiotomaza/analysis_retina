# 👁️ Retina Analysis Project

Um projeto de análise de imagens de retina desenvolvido em Python para fornecer diagnósticos rápidos e automatizados a partir de imagens de fundo de olho.


## 📋 Sobre o Projeto

Este projeto utiliza técnicas de processamento de imagem e machine learning para analisar imagens de retina e identificar possíveis anomalias ou condições oculares. O sistema é capaz de processar imagens de retina e gerar relatórios preliminares automaticamente.


## ✨ Funcionalidades

- Pré-processamento de imagens de retina;
- Detecção de características anatômicas (disco óptico, vasos sanguíneos);
- Identificação de anomalias como exsudatos, hemorragias e microaneurismas;
- Classificação de condições retinianas;
- Geração de relatórios automáticos;
- Interface simples para upload e análise de imagens.


## 🛠️ Tecnologias Utilizadas

- Python
- TensorFlow/Keras - Redes neurais e deep learning
- scikit-image - Análise e manipulação de imagens
- NumPy & Pandas - Processamento numérico e dados
- Matplotlib & Seaborn - Visualização
- Jupyter Notebook - Experimentação e desenvolvimento

## ⚙️ Como rodar?

```bash
python3 -m venv venv

source venv/bin/activate

. .\venv\Scripts\Activate.ps1

python.exe -m pip install --upgrade pip

pip install ipykernel jupyter

pip install -r requirements.txt
```