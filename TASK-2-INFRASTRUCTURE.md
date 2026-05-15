# Task 2: Zero-Trust Ghost Deployment on Hetzner

**Objective:** One-click deployment script for Ghost on a Hetzner VPS with NO public inbound ports (no public SSH, no public HTTP/S). All access is handled via outbound tunnels.

**Architecture:**
1. **Web Traffic:** Cloudflare Tunnels (`cloudflared`) runs as a Docker sidecar to Ghost. It creates an outbound tunnel to Cloudflare's edge. Port 80/443 are blocked on the VPS.
2. **Admin SSH:** Tailscale creates a secure WireGuard mesh. SSH is bound *only* to the Tailscale interface (`tailscale0`). Public port 22 is dropped.

### The One-Click Script (`deploy_ghost.sh`)

```bash
#!/bin/bash
set -e

echo "Starting Zero-Trust Ghost Deployment..."

# 1. Ask for credentials (Cloudflare Tunnel Token)
read -p "Enter your Cloudflare Tunnel Token: " CF_TOKEN

# 2. Update and Install Dependencies
sudo apt-get update && sudo apt-get install -y ufw curl docker.io docker-compose

# 3. Install Tailscale for Private SSH Access
curl -fsSL [https://tailscale.com/install.sh](https://tailscale.com/install.sh) | sh
sudo tailscale up --ssh # Enables Tailscale SSH

# 4. Lockdown Firewall (No Public Inbound)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow in on tailscale0 # ONLY allow inbound from Tailscale mesh
sudo ufw --force enable

# 5. Create Docker Compose for Ghost + Cloudflare Tunnel
mkdir -p /opt/ghost && cd /opt/ghost
cat <<EOF > docker-compose.yml
version: '3.8'
services:
  ghost:
    image: ghost:latest
    restart: always
    environment:
      # Change to your actual domain
      url: [https://my-blog-domain.com](https://my-blog-domain.com)
    volumes:
      - ghost_data:/var/lib/ghost/content

  cloudflared:
    image: cloudflare/cloudflared:latest
    restart: always
    command: tunnel run
    environment:
      - TUNNEL_TOKEN=\${CF_TOKEN}
    depends_on:
      - ghost

volumes:
  ghost_data:
EOF

# 6. Inject the token and start the services
echo "CF_TOKEN=$CF_TOKEN" > .env
sudo docker-compose up -d

echo "Deployment Complete."
echo "Public SSH is BLOCKED. Connect via Tailscale."
echo "Ghost is running and routed through Cloudflare Edge."