# 🌟 Foto do Espaço no Meu Aniversário

Site que mostra a **Foto Astronômica do Dia (APOD)** da NASA para a data do seu aniversário. Descubra qual imagem incrível do espaço a NASA publicou no dia em que você nasceu!

![NASA APOD](https://api.nasa.gov/images/logo.png)

## ✨ Sobre o projeto

Este projeto consome a API **Astronomy Picture of the Day** da NASA. O usuário informa sua data de aniversário e o site retorna a foto, o título e a descrição que a NASA publicou naquele dia.

- **Backend:** Python + Flask  
- **Frontend:** HTML, CSS e JavaScript  
- **API:** [NASA APOD API](https://api.nasa.gov/)

---

## 🚀 Como rodar

### Pré-requisitos

- Python 3.8+
- Chave da API NASA (gratuita em [api.nasa.gov](https://api.nasa.gov/))

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/nasa-aniversario.git
cd nasa-aniversario
```

### 2. Configure a chave da API

Crie o arquivo `backend/.env` com sua chave:

```
NASA_API_KEY=sua_chave_aqui
```

### 3. Ambiente virtual e dependências

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4. Inicie o servidor

```powershell
python app.py
```

Acesse no navegador: **http://127.0.0.1:5000**

---

## 📁 Estrutura do projeto

```
Plataformas/
├── backend/
│   ├── app.py          # API Flask + servidor do frontend
│   ├── requirements.txt
│   ├── .env            # NASA_API_KEY (não versionar!)
│   └── venv/           # Ambiente virtual
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── README.md
```

---

## ☁️ Hospedagem gratuita (Render)

1. Acesse [render.com](https://render.com) e crie conta (conecte com GitHub)
2. **New** → **Web Service**
3. Conecte o repositório do GitHub
4. Configure:
   - **Name:** `anivernasa`
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && gunicorn app:app --bind 0.0.0.0:$PORT`
5. Em **Environment** → **Add Environment Variable:**
   - Key: `NASA_API_KEY`
   - Value: (sua chave da NASA)
6. Clique em **Create Web Service**

Seu site ficará em: **https://nasa-site-oh6r.onrender.com/**

---

## 📅 Datas disponíveis

A API APOD da NASA possui registros a partir de **16 de junho de 1995**.

---

## 📄 Licença

Este projeto é de uso educacional. As imagens e textos são de propriedade da NASA.
