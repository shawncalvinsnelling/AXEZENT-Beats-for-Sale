# Releasing AXEZENT beats one at a time

## Current milestone

200 titles across 50 states are in `data/catalog.json`. Every track is `planned`, with no audio sold or published yet. This is **not** a 200-beat recording release.

## Track production checklist

1. Select the next `AXZ-NNN` catalog entry. Use the stable ID for file names and order references.
2. Compose an original instrumental. Keep MIDI, session files, stems, and source audio in a private production workspace.
3. Record/arrange an optional **original** hook demo; keep a no-hook version for buyers.
4. Confirm all collaborators' permissions and that any sampled sounds are properly licensed for the proposed usage, especially exclusive transfers.
5. Listen-test the arrangement, kick and bass, tonal balance and vocal space on headphones, speakers and a phone.
6. Export a **24-bit WAV master**, **320 kbps MP3 preview**, and optionally 24-bit separated stems (no MP4 needed for studio buyers).
7. Ensure preview audio is watermarked/tagged and protected from full-quality reuse. Store only the preview in `previews/AXZ-NNN-tagged.mp3`; keep masters and stems in **private object storage**.
8. To show a public preview, set catalog `status` to `preview_ready` and `previewUrl` to `previews/AXZ-NNN-tagged.mp3`. It is not for sale yet.
9. Run catalog checks and manually test preview playback on phone and desktop.
10. Publish **Buy** and **Download** functionality only after secure server-side payment verification, written license terms, customer support/refunds, and protected download URLs are tested.

## Sales / Cash App

A buyer sending $100 directly to a personal handle does **not** securely prove which track was bought, whether they own rights, or whether a particular payment succeeded.

For an initial manual workflow, use an eligible business payment account and unique **order reference** per purchase. The seller must personally confirm the actual transaction inside the payment account; never rely on screenshots, matching amounts, or unsupported claims. Delivery remains manual until a secure payment-verification backend is available.

For automatic fulfilment, integrate an eligible payment processor using signed server-to-server confirmation/webhooks. The customer receives the full WAV **only after** that verification. Public static HTML cannot secure paid downloads by itself.

## Rights

Proposed default: **$100 nonexclusive commercial license**. It does not transfer full copyright ownership. Formalize exactly what uses are included, sample clearance, credit requirements, royalty splits (if any), refund policy and exclusivity before accepting any money. An exclusive ownership transfer requires a separate signed assignment and removing that beat from sale.

## Owner data and analytics

Site searches and preview clicks need consent-aware server event collection; payments and download starts need authenticated, durable backend records. There are **no live customer analytics yet**, and no sales count should be invented. Do not place customer details or payment account identifiers in public GitHub.

## Deployment

This repository is a **static frontend**, not a hosted ecommerce backend. For a public website, connect it to an appropriate static web host (e.g. Vercel), then a secure backend with a managed database and private audio storage. GitHub Pages is not the recommended home for a commercial ecommerce storefront.

## Priority first track

**AXZ-169 — Diamond in the Dirt**, Houston, Texas; proposed 84 BPM and F minor. Track ID from the public catalog is preserved. Complete original composition, review and mastering before any public MP3 goes live.
