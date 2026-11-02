# One upload to enable 50 GitHub listening links

Your GitHub repo: https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale

**Do not upload full WAV masters or private ZIPs.** Upload only the five tagged preview bundles.

## Audio upload

1. Download these five separate ZIP files from the current ChatGPT conversation (one bundle of 10 tagged 96-kbps MP3s per ZIP):
   - `axezent-previews-01.zip`
   - `axezent-previews-02.zip`
   - `axezent-previews-03.zip`
   - `axezent-previews-04.zip`
   - `axezent-previews-05.zip`
2. Go to https://github.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/tree/main/incoming
3. Choose **Add file → Upload files** and upload all **five ZIPs** together. You do **not** need to extract them.
4. Commit directly to the **main** branch.
5. Go to **Actions → Import tagged AXEZENT preview audio** and confirm it succeeded.
6. Go back to the repository main page. The 50 `⏳ Preview upload pending` table cells should become **▶ Listen to tagged MP3** links.
7. Each Listen link opens the direct MP3 file, which a supported browser may play (or download). GitHub itself cannot guarantee a built-in Loop control in its README.
8. The full HTML player, `index.html`, supports **▶ Play** and **🔁 Repeat On/Off** once these preview files are present. The HTML source file does not render as an interactive website in the GitHub code viewer.

The GitHub automation checks the contents, verifies MP3 bitrate and playable duration via `ffprobe`, publishes only the preview recordings, and updates the main catalog and links. It fails closed if the files aren't correct.

## What remains disabled

Paid full-quality downloads, automatic PayPal/Cash App confirmation, and exclusive copyright transfer are **not** switched on by audio upload. The $100 email links are purchase inquiries only. Buyers must receive a confirmed offer and signed agreement before making a payment.

## Important hosting limitation

GitHub's repository page is a Markdown project homepage, not a full interactive website, and GitHub Pages is not permitted to be used as a free commercial e-commerce storefront. A true website with native embedded Play/Repeat/Checkout controls must be hosted separately (own self-managed server is fine).
