# Zero Trust Ghost Deployment

This directory contains a one-click deployment script to provision a Ghost blog on a Hetzner VPS without exposing SSH to the public internet.

## Architecture & Tooling
* **Target:** Hetzner VPS (Ubuntu/Debian)
* **Blog Platform:** Ghost (Dockerized)
* **Tunnel Provider:** Cloudflare Tunnels (`cloudflared`)

### Why Cloudflare Tunnels?
To fulfill the requirement of "no public SSH access", this script implements a Zero Trust architecture. 
1. **No Open Ports:** `ufw` blocks external traffic on Port 22, allowing only `127.0.0.1`.
2. **Web Traffic:** Cloudflare routes public web traffic securely to the internal Ghost container (port 2368).
3. **SSH Access:** Administrators SSH using the `cloudflared` client on their local machine, tunneling securely to the VPS localhost.

## How to use
1. In Cloudflare Zero Trust, create a Tunnel and map `blog.yourdomain.com` to `http://localhost:2368` and `ssh.yourdomain.com` to `ssh://localhost:22`.
2. Run on the VPS: `TUNNEL_TOKEN="your_token_here" sudo -E ./deploy-ghost.sh`