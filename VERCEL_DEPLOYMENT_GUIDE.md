# Vercel Deployment Guide for Sudoku App

This guide explains how to deploy the Sudoku Generator & Solver application to Vercel.

## Prerequisites

- A GitHub account
- A Vercel account (you can sign up at [vercel.com](https://vercel.com) using your GitHub account)

## Deployment Steps

### 1. Push to GitHub (Already Done)

Your code has been pushed to GitHub with all the necessary Vercel configuration files:
- `vercel.json` - Configures build settings and routing
- `api/server.py` - Main Flask application
- `api/index.py` - Serverless function entry point

### 2. Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) and log in with your GitHub account
2. Click on "Add New..." > "Project"
3. Select your GitHub repository
4. Vercel should automatically detect that this is a Python project
5. Configure your project:
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: Leave empty (or `python -m pip install -r requirements.txt`)
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`
6. Click "Deploy"

### 3. Environment Variables

If needed, you can add environment variables in the Vercel project settings.

### 4. Custom Domain (Optional)

Once deployed, you can add a custom domain in the Vercel project settings.

## Troubleshooting

If your deployment fails:

1. Check the Vercel deployment logs for specific errors
2. Verify the Python version is 3.9 in the Vercel settings
3. Make sure all dependencies are in `requirements.txt`
4. Ensure `vercel.json` is properly configured
5. Try a manual deployment using the Vercel CLI:
   ```
   npm install -g vercel
   vercel login
   vercel --prod
   ```

## Updating Your Deployment

After making changes to your code:

1. Push changes to GitHub
2. Vercel will automatically rebuild and deploy your application

## Local Development

To run the app locally:

```bash
python api/server.py
```

Or if using the Vercel CLI:

```bash
vercel dev
```

## Production URL

After deployment, your application will be available at:
- https://sudoku-[your-username].vercel.app (default)
- Or the custom domain you've configured

You can always check deployment status in your Vercel dashboard. 