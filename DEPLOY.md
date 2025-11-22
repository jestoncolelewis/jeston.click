# Railway Deployment Guide

This guide walks through deploying the jeston.click portfolio to Railway.

## Prerequisites

- Railway account ([railway.app](https://railway.app))
- GitHub repository connected to Railway
- Domain name (jeston.click)

## Deployment Steps

### 1. Create Railway Project

1. Log in to [Railway](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `jeston.click` repository
5. Railway will auto-detect the Python application

### 2. Add PostgreSQL Database

1. In your Railway project, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically provision a PostgreSQL database
4. The `DATABASE_URL` environment variable is auto-configured

### 3. Configure Environment Variables

Railway automatically sets:
- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - Application port

No additional environment variables are needed.

### 4. Deploy the API Service

1. Railway will automatically deploy from the main branch
2. The app uses the configuration in `railway.toml` and `Procfile`
3. Initial deployment takes ~2-3 minutes
4. Check logs for any errors

### 5. Initialize Database

After the first deployment, the database schema is automatically created on app startup via `init_db()` in `app.py`.

To migrate existing page view count from AWS DynamoDB:
1. Note the current count from your DynamoDB table
2. Run the following in Railway's database shell or via `psql`:
   ```sql
   UPDATE page_views SET view_num = <YOUR_COUNT> WHERE pk = 0;
   ```

### 6. Update Frontend URL

1. Get your Railway app URL (e.g., `https://your-app.up.railway.app`)
2. Update `www/script.js` line 6:
   ```javascript
   const url = 'https://your-app.up.railway.app/page-count'
   ```
3. Commit and push the change

### 7. Deploy Static Site (Optional - Railway or External)

**Option A: Deploy static site to Railway**
1. Create a new service in the same project
2. Use Nixpacks static site configuration
3. Point root to `/www` directory

**Option B: Use external static hosting (Netlify, Vercel, Cloudflare Pages)**
1. Deploy the `www` folder to your preferred platform
2. Ensure CORS is configured properly in `api/app.py`

### 8. Configure Custom Domain

1. In Railway project settings, go to your service
2. Click "Settings" → "Domains"
3. Add your custom domain: `api.jeston.click` (or subdomain of choice)
4. Add CNAME record in your DNS:
   ```
   CNAME api <your-app>.up.railway.app
   ```
5. Update `www/script.js` with your custom domain
6. Update CORS origins in `api/app.py` if needed

### 9. Configure Main Domain

Point your main domain (jeston.click) to wherever you're hosting the static site:
- If using Railway for static site: Add domain in Railway settings
- If using external host: Follow their domain configuration guide

## Health Checks

Railway automatically monitors the `/health` endpoint defined in the app.

Test it:
```bash
curl https://your-app.up.railway.app/health
```

## API Endpoints

- `GET /page-count` - Increment and return page view count
- `GET /health` - Health check endpoint

## Monitoring

- View logs in Railway dashboard
- Monitor database connections
- Check deployment status

## Cost Estimate

Railway free tier includes:
- $5 of free credit per month
- ~500 hours of usage

Expected costs (minimal traffic):
- API Service: ~$3-5/month
- PostgreSQL: ~$3-5/month
- **Total: ~$6-10/month** (well within free tier for low traffic)

Much cheaper than AWS for this use case!

## Rollback

Railway keeps deployment history. To rollback:
1. Go to "Deployments" in Railway dashboard
2. Find a previous successful deployment
3. Click "Redeploy"

## Troubleshooting

**Database connection errors:**
- Verify `DATABASE_URL` is set in Railway environment
- Check PostgreSQL service is running

**API not responding:**
- Check logs for Python errors
- Verify port binding to `$PORT` environment variable
- Ensure Procfile uses correct app path

**CORS errors:**
- Update `CORS(app, origins=[...])` in `api/app.py`
- Add your domain to the allowed origins list

## Migration from AWS

The old AWS infrastructure used:
- DynamoDB table: `jestondotclick-page-views`
- Lambda function: `jestonclick-page-count-31ee36e`
- API Gateway endpoint

To preserve page view count, export from DynamoDB before shutting down AWS resources.
