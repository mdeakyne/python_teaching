#!/bin/bash
#
# Test GitHub Pages Deployment
# Tests that the Jupyter Book deployed correctly to GitHub Pages
#

set -e

BASE_URL="https://mdeakyne.github.io/python_teaching"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================"
echo "Testing GitHub Pages Deployment"
echo "Base URL: $BASE_URL"
echo "================================================"
echo ""

# Test function
test_url() {
    local name="$1"
    local url="$2"
    local search_term="$3"

    printf "%-40s" "$name"

    # Check HTTP status
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)

    if [ "$status" = "200" ]; then
        # If search term provided, verify content
        if [ -n "$search_term" ]; then
            if curl -s "$url" 2>/dev/null | grep -q "$search_term"; then
                echo -e "${GREEN}✓ PASS${NC} (200 OK, content verified)"
                return 0
            else
                echo -e "${YELLOW}⚠ WARN${NC} (200 OK, but missing: $search_term)"
                return 1
            fi
        else
            echo -e "${GREEN}✓ PASS${NC} (200 OK)"
            return 0
        fi
    elif [ "$status" = "000" ]; then
        echo -e "${YELLOW}⚠ WAIT${NC} (Site not reachable yet - deployment may still be in progress)"
        return 1
    else
        echo -e "${RED}✗ FAIL${NC} (HTTP $status)"
        return 1
    fi
}

# Track results
passed=0
failed=0
total=0

# Test 1: Homepage
((total++))
if test_url "1. Homepage" "$BASE_URL/" "Pandas & Dash"; then
    ((passed++))
else
    ((failed++))
fi

# Test 2: Day 1 Lesson
((total++))
if test_url "2. Day 1 Lesson" "$BASE_URL/day-01/lesson.html" "Environment Setup"; then
    ((passed++))
else
    ((failed++))
fi

# Test 3: Day 1 Exercise
((total++))
if test_url "3. Day 1 Exercise" "$BASE_URL/day-01/exercise.html" ""; then
    ((passed++))
else
    ((failed++))
fi

# Test 4: Day 10 (Mid-point)
((total++))
if test_url "4. Day 10 Lesson" "$BASE_URL/day-10/lesson.html" "Plotly"; then
    ((passed++))
else
    ((failed++))
fi

# Test 5: Day 21 (Final)
((total++))
if test_url "5. Day 21 Capstone" "$BASE_URL/day-21/lesson.html" "Capstone"; then
    ((passed++))
else
    ((failed++))
fi

# Test 6: Search functionality
((total++))
if test_url "6. Search Page" "$BASE_URL/search.html" ""; then
    ((passed++))
else
    ((failed++))
fi

# Test 7: TOC/Navigation
((total++))
if test_url "7. Table of Contents" "$BASE_URL/" "day-01"; then
    ((passed++))
else
    ((failed++))
fi

echo ""
echo "================================================"
echo "Test Results"
echo "================================================"
echo -e "Total:  $total tests"
echo -e "${GREEN}Passed: $passed${NC}"
if [ $failed -gt 0 ]; then
    echo -e "${RED}Failed: $failed${NC}"
else
    echo -e "Failed: $failed"
fi
echo ""

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    echo "Your bootcamp is live at:"
    echo "  $BASE_URL"
    echo ""
    exit 0
elif [ $passed -eq 0 ]; then
    echo -e "${YELLOW}⚠ Site may not be deployed yet${NC}"
    echo ""
    echo "Check deployment status:"
    echo "  https://github.com/mdeakyne/python_teaching/actions"
    echo ""
    echo "Deployments typically take 2-3 minutes."
    echo "Run this script again in a few minutes."
    exit 2
else
    echo -e "${YELLOW}⚠ Some tests failed${NC}"
    echo ""
    echo "Site is partially deployed. Check the failed URLs manually."
    exit 1
fi
