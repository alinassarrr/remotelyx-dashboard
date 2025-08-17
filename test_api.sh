#!/bin/bash

# RemotelyX Dashboard API Testing Script
# This script tests all major API endpoints using curl

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# API Base URL
BASE_URL="http://localhost:8000"

# Global variables
ACCESS_TOKEN=""
USER_ID=""
JOB_ID=""

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_header() {
    echo -e "\n${BLUE}================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================${NC}"
}

# Function to check if server is running
check_server() {
    print_header "🔍 CHECKING SERVER STATUS"
    
    response=$(curl -s -w "%{http_code}" -o /dev/null "$BASE_URL/health")
    
    if [ "$response" -eq 200 ]; then
        print_success "Server is running on $BASE_URL"
        return 0
    else
        print_error "Server is not running on $BASE_URL"
        print_info "Please start the backend server first:"
        print_info "cd server && ./run_dev.sh"
        exit 1
    fi
}

# Function to test health endpoint
test_health() {
    print_header "🏥 TESTING HEALTH ENDPOINT"
    
    response=$(curl -s "$BASE_URL/health")
    status_code=$(curl -s -w "%{http_code}" -o /dev/null "$BASE_URL/health")
    
    if [ "$status_code" -eq 200 ]; then
        print_success "Health check passed"
        print_info "Response: $response"
    else
        print_error "Health check failed (Status: $status_code)"
    fi
}

# Function to register a test user
test_register() {
    print_header "👤 TESTING USER REGISTRATION"
    
    # Generate unique email for testing
    timestamp=$(date +%s)
    test_email="test$timestamp@remotelyx.com"
    
    response=$(curl -s -X POST "$BASE_URL/api/v1/auth/register" \
        -H "Content-Type: application/json" \
        -d "{
            \"email\": \"$test_email\",
            \"password\": \"SecurePassword123!\",
            \"full_name\": \"Test User $timestamp\",
            \"phone\": \"+1234567890\"
        }")
    
    status_code=$(curl -s -w "%{http_code}" -o /dev/null -X POST "$BASE_URL/api/v1/auth/register" \
        -H "Content-Type: application/json" \
        -d "{
            \"email\": \"$test_email\",
            \"password\": \"SecurePassword123!\",
            \"full_name\": \"Test User $timestamp\",
            \"phone\": \"+1234567890\"
        }")
    
    if [ "$status_code" -eq 201 ]; then
        print_success "User registration successful"
        USER_ID=$(echo "$response" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
        print_info "User ID: $USER_ID"
        print_info "Test Email: $test_email"
        
        # Store email for login
        TEST_EMAIL="$test_email"
    else
        print_error "User registration failed (Status: $status_code)"
        print_info "Response: $response"
    fi
}

# Function to login user
test_login() {
    print_header "🔐 TESTING USER LOGIN"
    
    if [ -z "$TEST_EMAIL" ]; then
        print_error "No test email available. Registration may have failed."
        return 1
    fi
    
    response=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=$TEST_EMAIL&password=SecurePassword123!")
    
    status_code=$(curl -s -w "%{http_code}" -o /dev/null -X POST "$BASE_URL/api/v1/auth/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=$TEST_EMAIL&password=SecurePassword123!")
    
    if [ "$status_code" -eq 200 ]; then
        print_success "User login successful"
        ACCESS_TOKEN=$(echo "$response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
        print_info "Access token obtained (length: ${#ACCESS_TOKEN})"
    else
        print_error "User login failed (Status: $status_code)"
        print_info "Response: $response"
    fi
}

# Function to test getting current user
test_get_user() {
    print_header "👨‍💻 TESTING GET CURRENT USER"
    
    if [ -z "$ACCESS_TOKEN" ]; then
        print_error "No access token available. Login may have failed."
        return 1
    fi
    
    response=$(curl -s -X GET "$BASE_URL/api/v1/auth/me" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    status_code=$(curl -s -w "%{http_code}" -o /dev/null -X GET "$BASE_URL/api/v1/auth/me" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    if [ "$status_code" -eq 200 ]; then
        print_success "Get current user successful"
        print_info "User data: $response"
    else
        print_error "Get current user failed (Status: $status_code)"
        print_info "Response: $response"
    fi
}

# Function to create a test job
test_create_job() {
    print_header "💼 TESTING JOB CREATION"
    
    if [ -z "$ACCESS_TOKEN" ]; then
        print_error "No access token available. Login may have failed."
        return 1
    fi
    
    response=$(curl -s -X POST "$BASE_URL/api/v1/jobs" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "title": "Senior Full-Stack Developer",
            "company": "TechCorp Inc.",
            "location": "Remote",
            "job_type": "FULL_TIME",
            "remote_type": "FULLY_REMOTE",
            "salary_min": 80000,
            "salary_max": 120000,
            "description": "We are looking for an experienced full-stack developer to join our team.",
            "requirements": ["React", "Node.js", "TypeScript", "MongoDB"],
            "url": "https://techcorp.com/careers/senior-fullstack",
            "status": "APPLIED"
        }')
    
    status_code=$(curl -s -w "%{http_code}" -o /dev/null -X POST "$BASE_URL/api/v1/jobs" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "title": "Senior Full-Stack Developer",
            "company": "TechCorp Inc.",
            "location": "Remote",
            "job_type": "FULL_TIME",
            "remote_type": "FULLY_REMOTE",
            "salary_min": 80000,
            "salary_max": 120000,
            "description": "We are looking for an experienced full-stack developer to join our team.",
            "requirements": ["React", "Node.js", "TypeScript", "MongoDB"],
            "url": "https://techcorp.com/careers/senior-fullstack",
            "status": "APPLIED"
        }')
    
    if [ "$status_code" -eq 201 ]; then
        print_success "Job creation successful"
        JOB_ID=$(echo "$response" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
        print_info "Job ID: $JOB_ID"
    else
        print_error "Job creation failed (Status: $status_code)"
        print_info "Response: $response"
    fi
}

# Function to get all jobs
test_get_jobs() {
    print_header "📋 TESTING GET ALL JOBS"
    
    if [ -z "$ACCESS_TOKEN" ]; then
        print_error "No access token available. Login may have failed."
        return 1
    fi
    
    response=$(curl -s -X GET "$BASE_URL/api/v1/jobs?skip=0&limit=10" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    status_code=$(curl -s -w "%{http_code}" -o /dev/null -X GET "$BASE_URL/api/v1/jobs?skip=0&limit=10" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    if [ "$status_code" -eq 200 ]; then
        print_success "Get all jobs successful"
        job_count=$(echo "$response" | grep -o '"id"' | wc -l)
        print_info "Found $job_count jobs"
    else
        print_error "Get all jobs failed (Status: $status_code)"
        print_info "Response: $response"
    fi
}

# Function to get job by ID
test_get_job_by_id() {
    print_header "🔍 TESTING GET JOB BY ID"
    
    if [ -z "$ACCESS_TOKEN" ] || [ -z "$JOB_ID" ]; then
        print_error "No access token or job ID available."
        return 1
    fi
    
    response=$(curl -s -X GET "$BASE_URL/api/v1/jobs/$JOB_ID" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    status_code=$(curl -s -w "%{http_code}" -o /dev/null -X GET "$BASE_URL/api/v1/jobs/$JOB_ID" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    if [ "$status_code" -eq 200 ]; then
        print_success "Get job by ID successful"
        print_info "Job details retrieved"
    else
        print_error "Get job by ID failed (Status: $status_code)"
        print_info "Response: $response"
    fi
}

# Function to update job
test_update_job() {
    print_header "✏️ TESTING JOB UPDATE"
    
    if [ -z "$ACCESS_TOKEN" ] || [ -z "$JOB_ID" ]; then
        print_error "No access token or job ID available."
        return 1
    fi
    
    response=$(curl -s -X PUT "$BASE_URL/api/v1/jobs/$JOB_ID" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"status": "INTERVIEW"}')
    
    status_code=$(curl -s -w "%{http_code}" -o /dev/null -X PUT "$BASE_URL/api/v1/jobs/$JOB_ID" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"status": "INTERVIEW"}')
    
    if [ "$status_code" -eq 200 ]; then
        print_success "Job update successful"
        print_info "Job status updated to INTERVIEW"
    else
        print_error "Job update failed (Status: $status_code)"
        print_info "Response: $response"
    fi
}

# Function to test search jobs
test_search_jobs() {
    print_header "🔎 TESTING JOB SEARCH"
    
    if [ -z "$ACCESS_TOKEN" ]; then
        print_error "No access token available. Login may have failed."
        return 1
    fi
    
    response=$(curl -s -X GET "$BASE_URL/api/v1/jobs/search?q=developer&company=TechCorp" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    status_code=$(curl -s -w "%{http_code}" -o /dev/null -X GET "$BASE_URL/api/v1/jobs/search?q=developer&company=TechCorp" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    if [ "$status_code" -eq 200 ]; then
        print_success "Job search successful"
        search_count=$(echo "$response" | grep -o '"id"' | wc -l)
        print_info "Found $search_count matching jobs"
    else
        print_error "Job search failed (Status: $status_code)"
        print_info "Response: $response"
    fi
}

# Function to test analytics
test_analytics() {
    print_header "📊 TESTING ANALYTICS ENDPOINTS"
    
    if [ -z "$ACCESS_TOKEN" ]; then
        print_error "No access token available. Login may have failed."
        return 1
    fi
    
    # Test dashboard analytics
    print_info "Testing dashboard analytics..."
    response=$(curl -s -X GET "$BASE_URL/api/v1/analytics/dashboard" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    status_code=$(curl -s -w "%{http_code}" -o /dev/null -X GET "$BASE_URL/api/v1/analytics/dashboard" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    if [ "$status_code" -eq 200 ]; then
        print_success "Dashboard analytics successful"
    else
        print_error "Dashboard analytics failed (Status: $status_code)"
    fi
    
    # Test timeline analytics
    print_info "Testing timeline analytics..."
    response=$(curl -s -X GET "$BASE_URL/api/v1/analytics/timeline?period=30" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    status_code=$(curl -s -w "%{http_code}" -o /dev/null -X GET "$BASE_URL/api/v1/analytics/timeline?period=30" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    if [ "$status_code" -eq 200 ]; then
        print_success "Timeline analytics successful"
    else
        print_error "Timeline analytics failed (Status: $status_code)"
    fi
    
    # Test skills analytics
    print_info "Testing skills analytics..."
    response=$(curl -s -X GET "$BASE_URL/api/v1/analytics/skills" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    status_code=$(curl -s -w "%{http_code}" -o /dev/null -X GET "$BASE_URL/api/v1/analytics/skills" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    
    if [ "$status_code" -eq 200 ]; then
        print_success "Skills analytics successful"
    else
        print_error "Skills analytics failed (Status: $status_code)"
    fi
}

# Function to test unauthorized access
test_unauthorized() {
    print_header "🚫 TESTING UNAUTHORIZED ACCESS"
    
    response=$(curl -s -w "%{http_code}" -o /dev/null -X GET "$BASE_URL/api/v1/jobs")
    
    if [ "$response" -eq 401 ]; then
        print_success "Unauthorized access properly blocked"
    else
        print_error "Unauthorized access not properly blocked (Status: $response)"
    fi
}

# Function to clean up test data
cleanup() {
    print_header "🧹 CLEANING UP TEST DATA"
    
    if [ -n "$ACCESS_TOKEN" ] && [ -n "$JOB_ID" ]; then
        print_info "Deleting test job..."
        status_code=$(curl -s -w "%{http_code}" -o /dev/null -X DELETE "$BASE_URL/api/v1/jobs/$JOB_ID" \
            -H "Authorization: Bearer $ACCESS_TOKEN")
        
        if [ "$status_code" -eq 200 ]; then
            print_success "Test job deleted successfully"
        else
            print_warning "Could not delete test job (Status: $status_code)"
        fi
    fi
    
    print_info "Note: Test user account remains in database for reference"
}

# Function to print test summary
print_summary() {
    print_header "📋 TEST SUMMARY"
    print_info "API testing completed for RemotelyX Dashboard"
    print_info "Base URL: $BASE_URL"
    print_info "Test User: $TEST_EMAIL"
    print_info "Check the output above for any failed tests"
}

# Main function to run all tests
main() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║               RemotelyX Dashboard API Tester              ║"
    echo "║                     Testing Suite                         ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Run all tests in sequence
    check_server
    test_health
    test_unauthorized
    test_register
    test_login
    test_get_user
    test_create_job
    test_get_jobs
    test_get_job_by_id
    test_update_job
    test_search_jobs
    test_analytics
    cleanup
    print_summary
    
    echo -e "\n${GREEN}🎉 All tests completed! Check results above.${NC}"
}

# Handle script interruption
trap cleanup EXIT

# Check if curl is installed
if ! command -v curl &> /dev/null; then
    print_error "curl is required but not installed. Please install curl first."
    exit 1
fi

# Run main function
main "$@" 