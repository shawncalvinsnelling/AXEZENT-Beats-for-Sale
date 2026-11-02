# Activate all 50 audio Play buttons

The storefront currently has **200 titles** and **50 review-mix entries**, but the actual tagged MP3 audio is not committed yet. GitHub's `index.html` viewer displays source code; it does **not** run the website.

## Upload the 50 public, tagged previews

1. Download and extract `AXEZENT_GitHub_Upload_50_Tagged_MP3s.zip` supplied privately in the ChatGPT conversation. The ZIP contains exactly 50 files named `AXZ-###-tagged.mp3`. **Never upload the private full-resolution WAV masters or untagged MP3s.**
2. Visit the [previews folder](../previews/) in this repository.
3. Select **Add file → Upload files**.
4. Drag all **50 extracted MP3 files** onto the upload page. Upload the files, **not the ZIP**; GitHub won't play a zipped recording.
5. Commit to `main`. GitHub permits up to 100 files in one web upload and each preview is under 2 MB. If your browser struggles with a single large upload, do ten files at a time.
6. The [Publish approved tagged audio previews](../.github/workflows/publish-previews.yml) workflow verifies that each file is MP3 at ≤128 kbps, has sufficient duration, and matches the expected catalog ID. It then switches `previewUrl` and `status` for matching tracks.
7. Once the workflow check passes, **a deployed website** connected to GitHub will show **Play Full Preview** for each uploaded beat.

## Open the actual website

A GitHub code-file page is not a deployed website. To make the storefront public:
- Sign into [Netlify](https://app.netlify.com/start).
- Import the GitHub repository `shawncalvinsnelling/AXEZENT-Beats-for-Sale`, with **no build command** and publish directory `.`.
- Visit the assigned `.netlify.app` site address. Copy that address into this repository's **About → Website** field, so the GitHub page has a one-click **Visit Website** link.

## Why Buy and Download are locked

A publicly streamable MP3 can always be captured, saved or recorded by a determined listener. We can lock **full-quality masters**, not guarantee that previews cannot be copied. The $100 license, purchases, and private downloads remain disabled until payment confirmation and a clear contract are implemented.

## Troubleshooting

- **Play disabled after upload:** Open GitHub **Actions**, find `Release approved tagged audio previews`, check for failure, and verify the filename is exactly `previews/AXZ-###-tagged.mp3`.
- **Play button stays disabled despite successful action:** Refresh the live Netlify site; confirm Netlify is connected to `main` and has deployed the latest commit.
- **Clicking index.html shows code:** Navigate to the separate Netlify URL, not the file page.
- **No audio sounds:** Check device volume, MP3 playback permissions, and browser console/network logs. A playable track must have a real, accessible `previewUrl`.
