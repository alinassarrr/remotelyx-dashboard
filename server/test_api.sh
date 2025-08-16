#!/bin/bash

# RemotelyX API Testing Script

echo "🧪 RemotelyX API Testing"
echo "========================="

# Check if server is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Server is not running. Start it first with: ./run_dev.sh"
    exit 1
fi

echo "✅ Server is running"
echo ""

# Test basic endpoints
echo "🔍 Testing basic endpoints..."
echo "   Health check: $(curl -s http://localhost:8000/health | jq -r '.status' 2>/dev/null || echo 'Failed')"
echo "   Root endpoint: $(curl -s http://localhost:8000/ | jq -r '.message' 2>/dev/null || echo 'Failed')"
echo ""

# Test authentication
echo "🔐 Testing authentication..."
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@remotelyx.com", "password": "admin123"}')

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    echo "✅ Login successful"
    TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token' 2>/dev/null || echo '')
    if [ -n "$TOKEN" ]; then
        echo "   JWT Token obtained"
        
        # Test protected endpoints
        echo ""
        echo "🔒 Testing protected endpoints..."
        
        # Test /me endpoint
        ME_RESPONSE=$(curl -s -X GET "http://localhost:8000/api/v1/auth/me" \
          -H "Authorization: Bearer $TOKEN")
        if echo "$ME_RESPONSE" | grep -q "email"; then
            echo "✅ /auth/me endpoint working"
        else
            echo "❌ /auth/me endpoint failed"
        fi
        
        # Test jobs endpoint
        JOBS_RESPONSE=$(curl -s -X GET "http://localhost:8000/api/v1/jobs" \
          -H "Authorization: Bearer $TOKEN")
        if echo "$JOBS_RESPONSE" | grep -q "title"; then
            echo "✅ /jobs endpoint working"
        else
            echo "❌ /jobs endpoint failed"
        fi
        
        # Test analytics endpoint
        ANALYTICS_RESPONSE=$(curl -s -X GET "http://localhost:8000/api/v1/analytics" \
          -H "Authorization: Bearer $TOKEN")
        if echo "$ANALYTICS_RESPONSE" | grep -q "kpis"; then
            echo "✅ /analytics endpoint working"
        else
            echo "❌ /analytics endpoint failed"
        fi
        
    else
        echo "❌ Could not extract JWT token"
    fi
else
    echo "❌ Login failed"
    echo "   Response: $LOGIN_RESPONSE"
fi

echo ""
echo "🎯 API Testing Complete!"
echo ""
echo "📚 For interactive testing, visit:"
echo "   - Swagger UI: http://localhost:8000/docs"
echo "   - ReDoc: http://localhost:8000/redoc"
echo ""
echo "🔑 Default admin credentials:"
echo "   - Email: admin@remotelyx.com"
echo "   - Password: admin123" 