# AXEZENT GitHub HTTPS music showcase — public listening excerpts

The live public website is:
https://shawncalvinsnelling.github.io/AXEZENT-Beats-for-Sale/

This is a noncommercial artist showcase using the original AXEZENT website's visual design and 50 featured catalog entries. GitHub Pages does not support the Python private streaming backend, customer transactions, or a full paid store. The full rights-transfer storefront needs separate hosting.

## How audio now works

The GitHub Actions workflow `.github/workflows/deploy-artist-showcase.yml` creates **50 PUBLIC 30-second excerpts** at deployment from the existing reproducible, synthesized AXEZENT **review-mix renderer** in `scripts/render_previews.py`.

Five parallel synthesis jobs each render ten full draft mixes in ephemeral GitHub Actions runner storage, then `scripts/build_public_listening_excerpts.py` extracts only 30 seconds of each into a separate low-bitrate MP3 for public listening. The workflow uploads **only the short samples**, not full review mixes, WAV masters, or stems. The deployment job verifies exactly 50 clips and generates the public `data/public-preview-manifest.json` for the static player.

These generated clips are not asserted to be the same recordings available in the private ChatGPT prototype. They are synthetic review drafts and are not automatically approved for $100 exclusive sale. For release-quality audio, replace the source/rendering pipeline with owner-approved recordings and a rights review.

**Important:** Any audio a public browser can play can be recorded or copied, regardless of whether the webpage shows a Download button. The 30-second limit reduces exposure; it does not enforce digital-rights protection.

## Deploy

1. Open https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/settings/pages
2. Under **Build and deployment → Source**, select **GitHub Actions**.
3. Open https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/actions/workflows/deploy-artist-showcase.yml and click **Run workflow** on `main` (or change an included source file).
4. Wait for `render-public-excerpts` (five jobs) and `deploy` to succeed, including the validation steps.
5. Open https://shawncalvinsnelling.github.io/AXEZENT-Beats-for-Sale/ and hard-refresh with Ctrl+F5. Play a beat, then Pause, Seek, Repeat, Stop and Exit. Test on a phone.
6. If Play fails, inspect the latest GitHub Actions job logs and look for the 50 sample manifest check. Check if `previews/AXZ-169-sample.mp3` resolves with an HTTPS 200 response.

The existing production storefront remains in `index.html` plus `assets/` and `server/`. Do not publish private masters to Pages or accept unverified exclusive rights payments through a static site.
