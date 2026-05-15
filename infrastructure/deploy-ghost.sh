#!/bin/bash
set -e

# ==============================================================================
# One-Click Ghost Deployment Script (Zero Trust / No Public SSH)
# Target: Hetzner VPS (Ubuntu/Debian)
# ==============================================================================

if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root or with sudo."
  exit 1
fi

if [ -z "$TUNNEL_TOKEN" ]; then
  echo "Error: TUNNEL_TOKEN environment variable is missing."
  echo "Usage: TUNNEL_TOKEN=ey... sudo -E ./deploy-ghost.sh"
  exit 1
fi

echo "🛡️ Configuring UFW Firewall..."
apt-get update && apt-get install -y ufw curl
ufw allow from 127.0.0.1 to any port 22
ufw deny 22/tcp
ufw --force enable

echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh

echo "👻 Configuring Ghost..."
mkdir -p /opt/ghost
cd /opt/ghost

cat << 'EOF' > docker-compose.yml
services:
  ghost:
    image: ghost:latest
    restart: always
    ports:
      - "127.0.0.1:2368:2368"
    environment:
      url: http://localhost:2368
    volumes:
      - ghost_data:/var/lib/ghost/content

volumes:
  ghost_data:
EOF

docker compose up -d

echo "☁️ Installing Cloudflare Tunnel (cloudflared)..."
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
dpkg -i cloudflared.deb
rm cloudflared.deb

cloudflared service install "$TUNNEL_TOKEN"
echo "✅ Deployment Complete! Public SSH blocked. Ghost is locked to localhost via Tunnel."