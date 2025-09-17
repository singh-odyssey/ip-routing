# Deploying IP Routing Bot to Render

This guide explains how to deploy your IP routing bot project to Render for free.

## Prerequisites

1. A GitHub account with your project repository
2. A Render account (sign up at https://render.com)
3. Your project should be pushed to GitHub

## Step-by-Step Deployment Instructions

### 1. Prepare Your Repository

Make sure your project has these files (already created):
- `requirements.txt` - Python dependencies
- `render.yaml` - Render service configuration
- `Procfile` - Alternative deployment configuration
- `.gitignore` - Files to exclude from deployment

### 2. Push to GitHub

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 3. Deploy on Render

1. **Go to Render Dashboard**
   - Visit https://render.com and sign in
   - Click "New +" button in the top right

2. **Create a Web Service**
   - Select "Web Service"
   - Choose "Build and deploy from a Git repository"
   - Click "Connect" next to your GitHub account

3. **Connect Your Repository**
   - Find and select your `ip-routing` repository
   - Click "Connect"

4. **Configure the Service**
   - **Name**: `ip-routing-bot` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your target audience
   - **Branch**: `main` (or your default branch)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python web_ui.py`

5. **Set Environment Variables** (if needed)
   - In the service settings, you can add environment variables
   - `PORT` is automatically set by Render
   - `FLASK_ENV` is set to `production` in render.yaml

6. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app
   - This process takes 5-10 minutes

### 4. Access Your Deployed App

Once deployment is complete:
- Your app will be available at: `https://your-service-name.onrender.com`
- The URL will be shown in your Render dashboard

## Important Notes

### Free Tier Limitations
- **Sleep Mode**: Free services sleep after 15 minutes of inactivity
- **Build Time**: Limited build minutes per month
- **Memory**: 512MB RAM limit
- **No Persistent Disk**: Files don't persist between deployments

### Bot Functionality Considerations
1. **Selenium/WebDriver**: May not work reliably on free tier due to memory constraints
2. **Background Tasks**: Free services sleep, so continuous bot tasks may be interrupted
3. **IP Rotation**: External proxy services may be needed for production

### Recommended Approach
For your bot to work effectively on the free tier:

1. **Web UI Only**: Deploy just the web interface for manual bot control
2. **On-Demand Execution**: Run bots only when triggered through the web UI
3. **Short Sessions**: Keep bot sessions brief to avoid memory issues

### Alternative for Continuous Bot Operation
If you need 24/7 bot operation, consider:
- Render's paid plans ($7/month) for persistent services
- Railway (also has free tier with better bot support)
- Self-hosted VPS solutions

## Testing Your Deployment

1. Visit your deployed URL
2. Test the web interface
3. Try running a short bot session
4. Monitor logs in Render dashboard for any issues

## Troubleshooting

### Common Issues:
1. **Build Failures**: Check requirements.txt for incompatible packages
2. **Memory Errors**: Reduce concurrent operations or use paid tier
3. **Selenium Issues**: Consider headless mode or alternative automation

### Viewing Logs:
- Go to your service in Render dashboard
- Click "Logs" tab to see real-time application logs
- Use logs to debug deployment and runtime issues

## Making Updates

To update your deployed app:
1. Make changes to your code
2. Push to GitHub: `git push origin main`
3. Render automatically rebuilds and redeploys

Your IP routing bot is now deployed and accessible worldwide through Render!