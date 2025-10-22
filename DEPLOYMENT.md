# Deploying to GitHub Pages

This guide will help you deploy your 21-Day Pandas & Dash Bootcamp to GitHub Pages for free hosting.

## Quick Deploy (Automatic with GitHub Actions)

### Step 1: Push to GitHub

```bash
# Push your latest changes (already done!)
git push origin main
```

### Step 2: Enable GitHub Pages

1. Go to your GitHub repository: https://github.com/mdeakyne/python_teaching
2. Click **Settings** (top right)
3. Click **Pages** (left sidebar under "Code and automation")
4. Under **Source**, select:
   - Source: **GitHub Actions**

That's it! GitHub Actions will automatically build and deploy.

### Step 3: Wait for Deployment

The first deployment takes 2-3 minutes. You can watch progress:

1. Go to **Actions** tab in your repository
2. Click on "Deploy Jupyter Book to GitHub Pages" workflow
3. Watch the build and deploy steps

### Step 4: Access Your Site

Once deployed, your bootcamp will be live at:

**https://mdeakyne.github.io/python_teaching/**

---

## How It Works

The GitHub Actions workflow (`.github/workflows/deploy.yml`) automatically:

1. ✅ Checks out your code on every push to `main`
2. ✅ Sets up Python 3.11 and installs `uv`
3. ✅ Installs Jupyter Book
4. ✅ Builds the static site from `docs/`
5. ✅ Deploys to GitHub Pages

### Manual Trigger

You can also manually trigger deployment:

1. Go to **Actions** tab
2. Click "Deploy Jupyter Book to GitHub Pages"
3. Click **Run workflow** → **Run workflow**

---

## Local Preview Before Deploying

To preview exactly what will be deployed:

```bash
# Build locally
uv run jupyter-book build docs

# Open in browser
open docs/_build/html/index.html

# Or serve with live reload
cd docs/_build/html
python -m http.server 8000
# Visit http://localhost:8000
```

---

## Troubleshooting

### Deploy Fails with "Not Found (404)"

**Error message:**
```
Error: Creating Pages deployment failed
Error: HttpError: Not Found
```

**Cause:** GitHub Pages hasn't been enabled in repository settings yet.

**Fix:**
1. Go to **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. Re-run the failed workflow (or push a new commit)

This must be done BEFORE the first deployment. After enabling Pages once, all future deployments will work automatically.

### Build Fails

**Check the Actions log:**
1. Go to **Actions** tab
2. Click the failed workflow run
3. Expand the failed step to see error details

**Common issues:**
- Missing dependencies → Add to workflow's `pip install` step
- Build errors → Run `jupyter-book build docs` locally to debug
- File paths → Ensure all links in markdown use relative paths

### Pages Not Showing

**Verify Pages settings:**
1. Go to **Settings** → **Pages**
2. Confirm **Source** is set to "GitHub Actions"
3. Check that deployment completed (green checkmark in Actions)

**Force rebuild:**
```bash
# Make a trivial change
echo "" >> docs/index.md

# Commit and push
git add docs/index.md
git commit -m "Trigger rebuild"
git push origin main
```

### Custom Domain (Optional)

To use a custom domain like `bootcamp.yoursite.com`:

1. **Settings** → **Pages** → **Custom domain**
2. Enter your domain
3. Add a `CNAME` record in your DNS settings:
   ```
   CNAME bootcamp.yoursite.com -> mdeakyne.github.io
   ```
4. Wait for DNS propagation (5-30 minutes)
5. Enable "Enforce HTTPS" in Pages settings

---

## Updating Content

Every time you push changes to `main`, the site rebuilds automatically:

```bash
# Edit content
vim docs/day-01/lesson.md

# Commit and push
git add docs/
git commit -m "Update Day 1 lesson"
git push origin main

# Site updates automatically in 2-3 minutes
```

---

## Advanced: Branch Deployments

Deploy from a specific branch:

```bash
# Create a dev branch
git checkout -b dev

# Make changes
# ... edit files ...

# Deploy from dev branch
git push origin dev
```

Then update workflow to deploy from `dev`:

```yaml
on:
  push:
    branches:
      - main
      - dev  # Add this line
```

---

## Testing Your Deployment

### Automated Test Script

Run the included test script to verify your deployment:

```bash
./test_deployment.sh
```

This will test:
- ✅ Homepage loads (200 OK)
- ✅ Day 1 lesson accessible
- ✅ Day 10 lesson accessible (mid-point check)
- ✅ Day 21 capstone accessible
- ✅ Search functionality works
- ✅ Navigation/TOC present

**If site isn't deployed yet:**
The script will show warnings and exit with a helpful message. Wait 2-3 minutes and run again.

**Example output:**
```
1. Homepage                              ✓ PASS (200 OK, content verified)
2. Day 1 Lesson                          ✓ PASS (200 OK, content verified)
...
✓ All tests passed!
Your bootcamp is live at: https://mdeakyne.github.io/python_teaching/
```

### Manual Testing

Visit these URLs to verify:
- Homepage: https://mdeakyne.github.io/python_teaching/
- Day 1: https://mdeakyne.github.io/python_teaching/day-01/lesson.html
- Day 21: https://mdeakyne.github.io/python_teaching/day-21/lesson.html

---

## Monitoring

### View Deployment History

**Actions** tab shows all deployments with:
- ✅ Success/failure status
- ⏱️ Build time
- 📊 Deployment logs

### Analytics (Optional)

Add Google Analytics to track visitors:

1. Get GA tracking ID
2. Add to `docs/_config.yml`:
   ```yaml
   html:
     google_analytics_id: "G-XXXXXXXXXX"
   ```
3. Commit and push

---

## Alternative Deployment Methods

### Manual GitHub Pages (Without Actions)

If you prefer manual control:

```bash
# Install ghp-import
uv pip install ghp-import

# Build the book
uv run jupyter-book build docs

# Deploy to gh-pages branch
ghp-import -n -p -f docs/_build/html

# Enable GitHub Pages from gh-pages branch in Settings
```

### Netlify

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start)

1. Connect your GitHub repo
2. Set build command: `jupyter-book build docs`
3. Set publish directory: `docs/_build/html`
4. Deploy!

### Read the Docs

1. Import project at readthedocs.org
2. Connect GitHub repository
3. RTD auto-detects Jupyter Book configuration
4. Deploy!

---

## Cost

**GitHub Pages is completely FREE for public repositories!**

Includes:
- ✅ Unlimited bandwidth
- ✅ Automatic SSL/HTTPS
- ✅ Custom domains
- ✅ Fast CDN delivery

---

## Next Steps

Once deployed:

1. ✅ Share the URL: https://mdeakyne.github.io/python_teaching/
2. ✅ Add URL to repository description
3. ✅ Tweet/share on LinkedIn
4. ✅ Add to your portfolio

**Your bootcamp is now live and ready for students!** 🎉
