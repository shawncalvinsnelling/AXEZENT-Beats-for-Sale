# AXEZENT — Self-hosted website (no Netlify, no website builder)

The store's pages are entirely owned as source code in this GitHub repository.

**GitHub is not the public shop.** To receive visitors on a domain, you must host the code on a real, Internet-connected computer with reliable uptime, HTTPS, a domain/DNS setup, and suitable network access. You may use your **own physical machine** (subject to ISP/router restrictions) or a rented machine that you manage yourself. No third-party website-building platform is required. PayPal/Cash App, Internet access, and domain registration are still external services.

## See the website on your Windows computer today

1. Download the code: on GitHub click **Code > Download ZIP**, then extract it.
2. Install Python 3 (check **Add Python to PATH**).
3. Open a terminal inside the extracted folder and run:
   ```powershell
   py -m http.server 8080 --bind 127.0.0.1
   ```
4. Open **http://127.0.0.1:8080/** in your browser. Your HTML, catalog, styling and search all work.
5. Note: Play works only for tracks whose **tagged MP3 previews have actually been uploaded** into `previews/` and whose catalog status/URL were verified. Without those files, the Play buttons correctly remain unavailable.

This local development preview is **not a public website**. It doesn't accept orders or offer secure paid downloads.

## Host it on your own server — production sketch

Use an always-on Linux server you control. Give it a public IPv4/IPv6 address, arrange DNS and forwarding, and permit inbound ports 80 and 443 where your firewall and ISP allow them.

1. Buy or use a domain under your control and set DNS A/AAAA records pointing to your own server's public address.
2. Install a maintained web server with automatic HTTPS (for example **Caddy**, which you run locally on your machine). This is self-hosting, not a managed website builder.
3. Clone this repository on the server and copy only the static public files to `/srv/axezent/`.
4. Example web server configuration lives in `Caddyfile.example`. Replace the example hostname with your actual domain, then test/reload your server config.
5. Set up protected automatic deployment (pull reviewed changes from `main`) and automatic security updates. Use a non-root service account. Maintain backups.
6. Test with a phone on mobile data, confirm HTTPS, browse/search, and verify preview audio plays. **Do not enable full-master downloads from the static site.**

For noncommercial preview of the site alone, local `http.server` is sufficient; for a paid public store a production web server and careful security review are needed.

## $100 exclusive transfer: manual-first procedure

The website displays payment identifiers and contact information **because the owner requested public display**. It does not confirm transactions.

1. Buyer emails a particular catalog ID (such as `AXZ-169`) to the seller.
2. Seller confirms that track is finished, legitimately controlled, not previously assigned exclusively, and available. Check any coauthor/sample/AI-authorship issues before making a promise.
3. Seller and buyer approve a **signed, written contract identifying the exact master and composition rights** and any limits. The template in `docs/EXCLUSIVE_BEAT_TRANSFER_DRAFT.md` is a drafting aid, not legal advice.
4. Seller gives buyer a **unique invoice/order ID** and the confirmed business payment instructions. PayPal purchases should be goods/services, not friends/family. Cash App must use an account/mode eligible for business earnings.
5. Seller **checks inside PayPal or Cash App** that the correct payment arrived. Do not trust screenshots or a payment total alone.
6. Seller sends the permitted lossless audio and signed paperwork through a private channel and marks the beat `sold` in their private order ledger. Stop offering an exclusive transfer to new buyers.
7. Keep appropriate sales records for taxes and benefit reporting. Do not publish buyer details or the payment ledger on GitHub.

**No $100 payment automatically transfers copyright.** A written, signed transfer is required, and the seller can transfer only rights they own. Copyright status of wholly AI-generated elements may be limited under US law.

## GitHub website button

When you have a **real, functioning HTTPS domain**, place the URL into GitHub repository **About → Website** and the top README 'Visit Store' button. Do not use an invented domain or a placeholder as if it were live.

## Current status

- 200 catalog titles, first 50 privately rendered and under review.
- The first 50 tagged MP3s still need to be published separately before the Play buttons can work on any hosted website.
- The payment-contact section is informational; **no automatic checkout, private download service, sales tracking backend or secure customer portal exists yet**.

## Public-contact privacy note

Anything in this public repository (phone number, email address, payment tag) can be indexed, copied and contacted by strangers and automated spam systems. Consider a dedicated business contact address/number if you want to minimize exposure.
