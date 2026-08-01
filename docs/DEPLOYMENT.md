# Deployment Manual

This guide provides step-by-step instructions to manually deploy the multi-agent application across Vercel (Frontend) and Render (Backend). The application relies on external LLM services (Gemini API) and doesn't require a traditional relational database, but the environment variables must be configured properly.

## 1. Backend Deployment (Render)

We will use Render to host the FastAPI backend. It is configured to run automatically using the included `render.yaml` file (Infrastructure as Code) or can be deployed manually.

### Option A: Blueprint (Recommended)
Render Blueprints allow you to deploy services from the `render.yaml` file automatically.
1. Sign up/Log in to [Render](https://render.com).
2. Go to the Dashboard and click **New > Blueprint**.
3. Connect your GitHub repository.
4. Render will automatically detect `render.yaml`.
5. Enter the required environment variable `GEMINI_API_KEY` when prompted.
6. Click **Apply**. The backend will be built and deployed.

### Option B: Manual Web Service Setup
1. On the Render Dashboard, click **New > Web Service**.
2. Connect your GitHub repository.
3. Configure the following:
   - **Name**: `multi-agent-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api:api --host 0.0.0.0 --port $PORT`
4. Expand **Advanced** and set the environment variables:
   - `PYTHON_VERSION`: `3.11.0`
   - `GEMINI_API_KEY`: Your Gemini API Key from Google AI Studio.
5. Click **Create Web Service**. 
6. Once deployed, copy your Render URL (e.g., `https://multi-agent-backend.onrender.com`).

---

## 2. Frontend Deployment (Vercel)

We will use Vercel to host the React/Vite frontend. Vercel automatically configures Vite projects perfectly.

### Step-by-Step Vercel Setup
1. Sign up/Log in to [Vercel](https://vercel.com).
2. Click **Add New > Project**.
3. Connect your GitHub account and import the repository.
4. Expand the **Build and Output Settings** (if it isn't auto-detected, but normally it is):
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend` (Crucial step, Vercel needs to know the app is in this folder).
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Expand **Environment Variables** and add your backend's API URL:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://multi-agent-backend.onrender.com` (Use the Render URL you copied in the previous step).
6. Click **Deploy**. Vercel will build and assign you a live URL.

---

## 3. Database / Services configuration

This specific project is an AI Agent workflow utilizing LangGraph and AutoGen, heavily leveraging LLMs. By default, it does **not** rely on a persistent relational database like PostgreSQL or MySQL.

However, if you choose to expand this project to save user chats, histories, or generated articles, follow the standard database integration practices from our Master Playbook:
1. Spin up a **PostgreSQL** instance via Neon, Supabase, or Render's built-in managed Postgres.
2. Store the `DATABASE_URL` in the environment variables of your Render backend.
3. Use a library like `SQLAlchemy` or `Prisma Client Python` to manage your migrations and queries.
4. Make sure to restart the deployment after applying new database environment variables.

### External LLM Keys
The application's core logic requires access to Gemini. The API keys must be securely injected via the environment variable `GEMINI_API_KEY` on the backend (Render). The frontend (Vercel) does not need and should never expose this key in the browser.
