# 🔄 Updating Vercel Deployment

## Quick Update Steps

1. **Commit and push your changes**:
   ```bash
   git add .
   git commit -m "Add content management UI and fix error handling"
   git push
   ```

2. **Vercel will automatically redeploy** when you push to your main branch.

3. **If automatic deployment doesn't work**, manually trigger:
   - Go to your Vercel dashboard
   - Click on your project
   - Go to "Deployments" tab
   - Click "Redeploy" on the latest deployment

## Environment Variables

Make sure these are set in Vercel:

1. Go to Project Settings → Environment Variables
2. Add/Update:
   - `REACT_APP_API_URL` - Your backend API URL (e.g., `https://your-backend.railway.app/api`)
   - `OPENAI_API_KEY` - Your OpenAI API key (for backend)

## Frontend Build

The frontend should build automatically. If it doesn't:

1. Check build logs in Vercel dashboard
2. Ensure `package.json` has correct build script: `"build": "react-scripts build"`
3. Check that all dependencies are in `package.json`

## Backend (if using Vercel serverless)

If you're using Vercel serverless functions:
- Make sure `api/index.py` exists
- Check that `requirements-vercel.txt` has all dependencies
- Verify environment variables are set

## Troubleshooting

### Changes not showing?
1. Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
2. Check Vercel deployment logs
3. Verify the build completed successfully
4. Check that environment variables are correct

### Still having issues?
- Check Vercel build logs for errors
- Verify all files are committed and pushed
- Make sure `vercel.json` is configured correctly

