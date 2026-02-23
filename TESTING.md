# 🧪 Manual Testing Guide

## Your Application is Running! ✅

- **Backend**: http://127.0.0.1:5000
- **Frontend**: http://localhost:5173

---

## Quick Test Steps

### 1. Open Frontend in Browser

1. Open your web browser
2. Go to: **http://localhost:5173**
3. You should see the Fake News Detection homepage

### 2. Test Text Analysis

1. Click **"Analyze"** in the navigation menu
2. Make sure **"Analyze Text"** tab is selected
3. Paste this sample text:

```
Scientists have discovered a new species of butterfly in the Amazon rainforest. 
The discovery was made by researchers from the University of São Paulo during 
a field expedition. The butterfly, named Morpho tanmayi, has distinctive blue 
wings and is found only in a small region of the rainforest. The research team 
published their findings in the Journal of Tropical Biology.
```

4. Click **"Run Analysis"**
5. Wait 2-5 seconds for results

**Expected Result**: 
- Should show "Real" or "Fake" prediction
- ML confidence percentage
- Web similarity score
- Combined score
- Analysis insights (sentiment, keywords, red flags)

### 3. Test URL Analysis (May Fail for Some URLs)

1. Click **"Analyze URL"** tab
2. Try one of these URLs:

**Simple URLs to test**:
- `https://www.bbc.com/news`
- `https://www.reuters.com`
- `https://www.theguardian.com`

3. Click **"Run Analysis"**
4. Wait 5-10 seconds (URL extraction takes longer)

**Note**: URL analysis may fail (422 error) for some websites due to:
- Anti-scraping protection
- Paywall/login required
- Cloudflare protection
- No article content on homepage

**This is normal!** The 422 errors you saw are expected for certain URLs.

---

## What the 422 Errors Mean

The 422 errors in your terminal logs mean:
```
"Unable to extract content from URL"
```

This happens when:
1. The URL doesn't contain article text (like a homepage)
2. The website blocks scraping
3. The page requires JavaScript to load content

**Solution**: Try URLs that point to actual news articles, not homepages.

---

## Test with cURL (Command Line)

### Test 1: Health Check
```powershell
curl http://localhost:5000/
```
Expected: `{"message": "✅ Hybrid Fake News Detection API is running"}`

### Test 2: Text Prediction
```powershell
curl -X POST http://localhost:5000/api/predict_text `
  -H "Content-Type: application/json" `
  -d '{\"news\": \"Scientists discovered a new species in the Amazon rainforest.\"}'
```

### Test 3: Text Analysis
```powershell
curl -X POST http://localhost:5000/api/analyze_text `
  -H "Content-Type: application/json" `
  -d '{\"news\": \"BREAKING: This shocking viral story will amaze you!\"}'
```

---

## ✅ Success Indicators

Your app is working correctly if:

1. ✅ Frontend loads at http://localhost:5173
2. ✅ You can navigate between pages (Home, About, Analyze)
3. ✅ Text analysis returns results
4. ✅ Results show ML prediction, confidence, and analysis
5. ✅ No CORS errors in browser console (F12)

**URL analysis failing is OK** - it's expected for many URLs due to scraping restrictions.

---

## 🎯 What to Test Before Deployment

- [x] Backend starts without errors ✅
- [x] Frontend starts without errors ✅
- [ ] Text analysis works
- [ ] Results display correctly
- [ ] Navigation works (Home → About → Analyze)
- [ ] No console errors (F12 in browser)
- [ ] Mobile responsive (resize browser window)

---

## 🐛 Troubleshooting

### Frontend shows blank page
- Check browser console (F12) for errors
- Verify backend is running on port 5000
- Check if `VITE_API_BASE` is set correctly

### CORS errors in console
- Backend should show `ALLOWED_ORIGINS=*` for local development
- This is already configured correctly in your app

### Text analysis not working
- Check backend terminal for errors
- Verify model files exist in `backend/Model/`
- Try restarting backend

---

## 📸 Take Screenshots for Portfolio

Once everything works, capture the new **Premium Dark Glassmorphism UI**:

1. **Homepage** - Capture the animated gradient text and glowing background orbs.
2. **Analysis Dashboard** - Capture the frosted glass mode-toggle panel.
3. **Results Page** - Run an analysis to show off the Neon glowing progress bars (Red/Green) and the detailed insight cards.
4. **About Page** - Show the beautifully balanced modern typography and component grid.
---

## 🚀 Ready for Deployment?

Once local testing is complete:

1. Commit all changes to git
2. Push to GitHub
3. Follow the deployment guide in `DEPLOYMENT.md`
4. Start with **Render + Vercel** (easiest)

---

## Need Help?

If you encounter issues:
1. Check the browser console (F12)
2. Check backend terminal for errors
3. Try the cURL commands above
4. Review the troubleshooting section

**Your app is running successfully!** The 422 errors are normal for URL analysis with certain websites.
