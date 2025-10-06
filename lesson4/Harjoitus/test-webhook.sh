#!/bin/bash
# Test script for IoT pipeline webhook endpoint

SERVER_URL=${1:-http://localhost:3000}

echo "Testing IoT webhook at: $SERVER_URL/webhook"
echo "=========================================="
echo ""

# Test 1: Send normal reading
echo "Test 1: Sending normal temperature reading (22°C)..."
curl -X POST "$SERVER_URL/webhook" \
  -H "Content-Type: application/json" \
  -d '{"temp": 22.5, "hum": 65.2, "source": "test-script"}' \
  -w "\nStatus: %{http_code}\n\n"

sleep 2

# Test 2: Send high temperature (should trigger alert if configured)
echo "Test 2: Sending HIGH temperature reading (35°C - should trigger alert)..."
curl -X POST "$SERVER_URL/webhook" \
  -H "Content-Type: application/json" \
  -d '{"temp": 35.0, "hum": 45.0, "source": "test-script"}' \
  -w "\nStatus: %{http_code}\n\n"

sleep 2

# Test 3: Send low temperature
echo "Test 3: Sending LOW temperature reading (5°C - should trigger alert)..."
curl -X POST "$SERVER_URL/webhook" \
  -H "Content-Type: application/json" \
  -d '{"temp": 5.0, "hum": 80.0, "source": "test-script"}' \
  -w "\nStatus: %{http_code}\n\n"

sleep 2

# Test 4: Get current data
echo "Test 4: Fetching current readings from /data..."
curl -X GET "$SERVER_URL/data" | jq '.readings | length'
echo ""

# Test 5: Register a webhook
echo "Test 5: Registering a test webhook..."
curl -X POST "$SERVER_URL/webhooks/register" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://webhook.site/test", "name": "Test Webhook"}' \
  -w "\nStatus: %{http_code}\n\n"

sleep 1

# Test 6: List registered webhooks
echo "Test 6: Listing registered webhooks..."
curl -X GET "$SERVER_URL/webhooks" | jq
echo ""

echo "=========================================="
echo "All tests completed!"
echo "Open dashboard at: $SERVER_URL"
