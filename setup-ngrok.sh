#!/bin/bash

# Setup ngrok for n8n RemotelyX Dashboard

echo "🌐 Setting up ngrok for n8n integration..."
echo "==========================================="

echo ""
echo "📋 Instructions:"
echo "1. Make sure ngrok is installed (https://ngrok.com/)"
echo "2. Run: ngrok http 5679"
echo "3. Copy your ngrok URL (e.g., https://abc123.ngrok.io)"
echo "4. Update docker-compose.yml with your ngrok URL"
echo "5. Restart n8n service"
echo ""

read -p "Enter your ngrok URL (e.g., https://abc123.ngrok.io): " NGROK_URL

if [ -z "$NGROK_URL" ]; then
    echo "❌ No URL provided. Exiting..."
    exit 1
fi

echo ""
echo "🔄 Updating docker-compose.yml with your ngrok URL..."

# Update the docker-compose.yml file
sed -i "s|https://your-ngrok-subdomain.ngrok.io/|${NGROK_URL}/|g" docker-compose.yml

echo "✅ Updated docker-compose.yml"
echo ""

echo "🔄 Restarting n8n service..."
docker-compose restart n8n

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Access URLs:"
echo "   - Local n8n: http://localhost:5679"
echo "   - Public n8n: $NGROK_URL"
echo "   - Credentials: hadihaidar1723@gmail.com / Treble23!"
echo ""
echo "💡 Your webhooks will now work with: $NGROK_URL/webhook/"
echo ""
