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

### 🪟 Windows

```bash
# Etapa 0: Corrige problema de política de execução do PowerShell para permitir a ativação (temporário)
Set-ExecutionPolicy RemoteSigned -Scope Process

# Etapa 1: Cria o ambiente virtual chamado .venv usando especificamente o Python 3.11
# O comando "py -3.11" garante que o interpretador 3.11 seja usado
py -3.11 -m venv .venv

# Etapa 2: Ativa o ambiente virtual para que os comandos 'pip' instalem APENAS nele
.\.venv\Scripts\Activate.ps1
# *** Verifique se o seu prompt mudou para (.venv) PS C:\... ***

# Etapa 3: Atualiza o pip dentro do ambiente (Comum para todos os sistemas)
python -m pip install --upgrade pip

# Etapa 4: Instala/Atualiza as ferramentas de construção
pip install --upgrade setuptools wheel

# Etapa 5: Instala os pacotes desejados
pip install ipykernel jupyter
```

### 🪟 Linux/macOS

```bash
# 1. Cria o ambiente virtual chamado .venv usando especificamente o Python 3.11
# Este comando assume que 'python3.11' está disponível no seu PATH
python3.11 -m venv .venv

# 2. Ativa o ambiente virtual (usa 'source' no Linux/macOS)
source .venv/bin/activate
# *** Verifique se o seu prompt mudou para (.venv) ***

# 3. Atualiza o pip dentro do ambiente
python -m pip install --upgrade pip

# 4. Instala/Atualiza as ferramentas de construção
pip install --upgrade setuptools wheel

# 5. Instala os pacotes desejados
pip install ipykernel jupyter
```

### 💀 Como desativas o ambiente virtual no terminal?

```bash
deactivate
```