# 🚀 Quick Deployment Guide

## Choose Your Deployment Method

### Option 1: Render + Vercel (Easiest, Free Tier) ⭐ RECOMMENDED

**Perfect for**: Beginners, portfolios, demos

#### Backend (Render)

1. **Sign up** at https://render.com
2. **New Web Service** → Connect GitHub repo
3. **Settings**:
   - Name: `fakenews-backend`
   - Root Directory: `backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 2 -k gthread -t 60 -b 0.0.0.0:$PORT wsgi:application`
4. **Environment Variables**:
   - `ALLOWED_ORIGINS`: Leave blank for now (will update after frontend)
   - `USE_JINA_FALLBACK`: `1`
   - `PYTHON_VERSION`: `3.11.0`
5. **Create Web Service**
6. **Copy the URL** (e.g., `https://fakenews-backend.onrender.com`)

#### Frontend (Vercel)

1. **Sign up** at https://vercel.com
2. **Import Project** → Select GitHub repo
3. **Settings**:
   - Framework Preset: `Vite`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. **Environment Variables**:
   - `VITE_API_BASE`: Paste your Render backend URL
5. **Deploy**
6. **Copy the URL** (e.g., `https://fakenews.vercel.app`)

#### Final Step: Update CORS

1. Go back to **Render dashboard**
2. Open your backend service
3. **Environment** → Edit `ALLOWED_ORIGINS`
4. Set to your Vercel URL: `https://fakenews.vercel.app`
5. **Save Changes** (will auto-redeploy)

✅ **Done!** Visit your Vercel URL to use the app.

---

### Option 2: Railway (All-in-One)

**Perfect for**: Simple full-stack deployment

1. **Sign up** at https://railway.app
2. **New Project** → Deploy from GitHub repo
3. **Add Backend Service**:
   - Root Directory: `backend`
   - Environment Variables:
     - `ALLOWED_ORIGINS`: (update after frontend)
     - `USE_JINA_FALLBACK`: `1`
   - Copy the generated URL
4. **Add Frontend Service**:
   - Root Directory: `frontend`
   - Environment Variables:
     - `VITE_API_BASE`: (paste backend URL)
   - Copy the generated URL
5. **Update Backend CORS**:
   - Edit `ALLOWED_ORIGINS` with frontend URL

✅ **Done!** Both services auto-deploy on git push.

---

### Option 3: Docker (Self-Hosted VPS)

**Perfect for**: Full control, production deployments

#### Prerequisites
- VPS with Ubuntu 22.04 (DigitalOcean, AWS, Linode, etc.)
- Minimum 2GB RAM
- Docker installed

#### Steps

1. **SSH into your VPS**:
   ```bash
   ssh root@your-server-ip
   ```

2. **Install Docker** (if not installed):
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo apt-get install docker-compose-plugin
   ```

3. **Clone your repo**:
   ```bash
   git clone https://github.com/yourusername/FAKE_NEWS_DET_REACT.git
   cd FAKE_NEWS_DET_REACT
   ```

4. **Update docker-compose.yml**:
   - Edit `VITE_API_BASE` to your server IP or domain
   - Edit `ALLOWED_ORIGINS` to match

5. **Build and run**:
   ```bash
   docker compose up -d --build
   ```

6. **Check status**:
   ```bash
   docker compose ps
   docker compose logs
   ```

7. **Access your app**:
   - Frontend: `http://your-server-ip`
   - Backend: `http://your-server-ip:5000`

#### Optional: Setup Domain + SSL

1. **Point domain to server IP** (in DNS settings)

2. **Install nginx**:
   ```bash
   sudo apt install nginx certbot python3-certbot-nginx
   ```

3. **Create nginx config**:
   ```bash
   sudo nano /etc/nginx/sites-available/fakenews
   ```

   Paste:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:80;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /api {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. **Enable site**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/fakenews /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

5. **Get SSL certificate**:
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

✅ **Done!** Visit `https://your-domain.com`

---

## Testing Your Deployment

### 1. Backend Health Check
```bash
curl https://your-backend-url.com/
```
Expected response:
```json
{"message": "✅ Hybrid Fake News Detection API is running"}
```

### 2. Frontend Test
1. Open your frontend URL in browser
2. Click "Analyze" in navigation
3. Paste test text:
   ```
   Scientists have discovered a new species of butterfly in the Amazon rainforest.
   ```
4. Click "Run Analysis"
5. Verify results appear

### 3. Check Browser Console
- Open Developer Tools (F12)
- Check Console tab for errors
- Look for CORS errors (if any, update ALLOWED_ORIGINS)

---

## Troubleshooting

### "CORS policy" error
**Fix**: Update backend `ALLOWED_ORIGINS` to include your frontend URL

### "Model files not found"
**Fix**: Ensure `.pkl` files are committed to git:
```bash
git add backend/Model/*.pkl
git commit -m "Add model files"
git push
```

### Backend takes 30+ seconds to respond (Render free tier)
**Cause**: Free tier sleeps after 15 minutes of inactivity  
**Fix**: Upgrade to paid plan ($7/month) or use Railway

### Build fails on Render
**Fix**: Add `PYTHON_VERSION=3.11.0` environment variable

### Frontend shows blank page
**Fix**: Check browser console for errors, verify `VITE_API_BASE` is set correctly

---

## Cost Summary

| Platform | Free Tier | Paid Plan | Best For |
|----------|-----------|-----------|----------|
| **Render + Vercel** | ✅ Yes (with sleep) | $7/month | Beginners |
| **Railway** | $5 credit | $5-10/month | Simple setup |
| **Docker VPS** | ❌ No | $5-15/month | Full control |

---

## Next Steps After Deployment

1. ✅ Test all features thoroughly
2. 📊 Add analytics (Google Analytics, Plausible)
3. 🔍 Setup monitoring (UptimeRobot, Better Uptime)
4. 📝 Add your URLs to README
5. 🎥 Create demo video for portfolio
6. 🌐 Share on LinkedIn/Twitter

---

## Need Help?

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Railway Docs**: https://docs.railway.app
- **Docker Docs**: https://docs.docker.com

**Good luck with your deployment! 🚀**
