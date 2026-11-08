# AXEZENT GitHub HTTPS showcase (not the sales store)

The existing main website is a storefront backed by the AXEZENT Python streaming service. GitHub Pages cannot run this backend, and GitHub Pages rules prohibit primarily commercial storefronts.

This repository contains a separate, **noncommercial artist showcase** for GitHub Pages in `pages-showcase/`. It reuses the site's visual style and lists the 50 featured catalog selections without prices, order forms, payment links, account login, or downloadable music.

## Enable the login-free public HTTPS showcase

1. Open https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/settings/pages while signed into the repo owner account.
2. Under **Build and deployment → Source**, choose **GitHub Actions** and save.
3. Open the repository **Actions** tab. Select **Deploy AXEZENT artist showcase to GitHub Pages**, then click **Run workflow** on the main branch. (A push after enabling Pages can also trigger deployment.)
4. Confirm the workflow succeeds and click **Visit site** from the Pages settings. The expected default URL is https://shawncalvinsnelling.github.io/AXEZENT-Beats-for-Sale/ — do not advertise it until the site is confirmed live.
5. Check in a logged-out browser and on a phone. There should be no GitHub or ChatGPT sign-in prompt.

The workflow publishes only a sanitized site artifact; no `server/`, `.env`, `previews/`, payment handles, contact information, or private masters are included.

The full AXEZENT Beats for Sale site remains in `index.html` plus `assets/` and `server/`. That store needs a separate public HTTPS host which supports the streaming backend and contractual/manual order flow.

Do not change the repository's primary README link to the expected `github.io` URL until the Pages website is verified available.
