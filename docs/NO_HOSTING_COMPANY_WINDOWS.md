# AXEZENT first-party hosting: no commercial hosting provider

Our GitHub repository is the entrance to BEATS & INSTRUMENTALS FOR SALE.
The intended live website displays 50 titles, each with its own Listen button.
The local Python API streams the private MP3 previews and does not publish WAV masters.

## Step 1: Start on the owner's Windows computer

Keep the repository on the Windows computer. Beside it (NOT inside it),
create a sibling folder named AXEZENT_PRIVATE_TAGGED_PREVIEWS. Put the 50
tagged review MP3s in it, named AXZ-169-tagged.mp3 and so forth.

Double-click deploy/START_AXEZENT_ON_MY_WINDOWS_PC.bat.

The program first checks that 50/50 MP3 files are ready. Then it serves
the music website at http://127.0.0.1:8080/ on the SAME COMPUTER.
The API status is http://127.0.0.1:8080/api/ready.

Do not put the 50 private audio files in the public GitHub repository.
Do not open the Windows Python test server to the public Internet
without a protective local HTTPS reverse proxy.

## Step 2: Give the website a real address from a computer we control

GitHub code cannot configure the home router or make a local Windows PC
publicly reachable. The owner must be able to receive incoming Internet
connections, configure router/firewall rules, and operate an always-on PC
or server. Check whether the ISP supplies an inbound public IP rather
than carrier-grade NAT.

For Linux owners, deploy/launch-on-own-server.sh, compose.yaml and
deploy/Caddyfile provide the HTTPS local-server configuration using Caddy.
That requires real DNS, ports 80 and 443, and private MP3 files.
For Windows owners, a local TLS reverse proxy still needs to be configured
once the domain and networking are known.

Public HTTPS usually involves a domain registrar, DNS, and trusted
certificate authority, but NO separate commercial WEB HOST is required.

## Step 3: Activate the GitHub website button

Only after a real public HTTPS site is running and 50/50 streams work,
open GitHub Actions -> Activate one-click AXEZENT player link.
Enter the actual HTTPS site address. The launch check verifies the
popup player, API readiness and all 50 preview streams before publishing
the one-click website link on GitHub.

These files are preliminary review mixes; rendering code changes do not
replace existing MP3s or imply that professional audio review is complete.
Streaming audio can still be captured even when the player has no
Download button.
