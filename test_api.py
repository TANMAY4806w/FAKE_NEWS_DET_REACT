"""
Test script for Fake News Detection API
Run this to test your backend endpoints
"""

import requests
import json

API_BASE = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    try:
        response = requests.get(f"{API_BASE}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_text_prediction():
    """Test text prediction endpoint"""
    print("\n" + "="*60)
    print("TEST 2: Text Prediction")
    print("="*60)
    
    test_text = """
    Scientists have discovered a new species of butterfly in the Amazon rainforest. 
    The discovery was made by researchers from the University of São Paulo during 
    a field expedition. The butterfly, named Morpho tanmayi, has distinctive blue 
    wings and is found only in a small region of the rainforest.
    """
    
    try:
        response = requests.post(
            f"{API_BASE}/api/predict_text",
            json={"news": test_text},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Prediction Results:")
            print(f"   ML Label: {result.get('ml_label')}")
            print(f"   ML Confidence: {result.get('ml_confidence')}%")
            print(f"   Web Similarity: {result.get('web_similarity')}%")
            print(f"   Combined Score: {result.get('combined_score')}%")
            print(f"   Final Label: {result.get('final_label')}")
            print(f"   Sources Found: {len(result.get('sources', []))}")
            
            if result.get('analysis'):
                print(f"\n   Analysis:")
                print(f"   - Sentiment: {result['analysis'].get('sentiment')}")
                print(f"   - Red Flags: {len(result['analysis'].get('red_flags', []))}")
            
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_url_prediction():
    """Test URL prediction endpoint"""
    print("\n" + "="*60)
    print("TEST 3: URL Prediction")
    print("="*60)
    
    # Using a simple, accessible news URL
    test_url = "https://www.bbc.com/news"
    
    try:
        response = requests.post(
            f"{API_BASE}/api/predict_url",
            json={"url": test_url},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ URL Analysis Results:")
            print(f"   Headline: {result.get('headline', 'N/A')[:100]}...")
            print(f"   ML Label: {result.get('ml_label')}")
            print(f"   ML Confidence: {result.get('ml_confidence')}%")
            print(f"   Final Label: {result.get('final_label')}")
            return True
        elif response.status_code == 422:
            error = response.json()
            print(f"⚠️  URL extraction failed: {error.get('error')}")
            print(f"   This is expected for some URLs due to scraping restrictions")
            return False
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_analyze_text():
    """Test analyze text endpoint"""
    print("\n" + "="*60)
    print("TEST 4: Text Analysis (Keywords & Sentiment)")
    print("="*60)
    
    test_text = "BREAKING: Shocking discovery! This amazing viral story will blow your mind!"
    
    try:
        response = requests.post(
            f"{API_BASE}/api/analyze_text",
            json={"news": test_text},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Analysis Results:")
            print(f"   Sentiment: {result.get('sentiment')}")
            print(f"   Suspicious Keywords: {result.get('suspicious_keywords')}")
            print(f"   Trust Keywords: {result.get('trust_keywords')}")
            print(f"   Red Flags: {result.get('red_flags')}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧠 FAKE NEWS DETECTION API - TEST SUITE")
    print("="*60)
    print(f"Testing API at: {API_BASE}")
    
    results = {
        "Health Check": test_health_check(),
        "Text Prediction": test_text_prediction(),
        "URL Prediction": test_url_prediction(),
        "Text Analysis": test_analyze_text()
    }
    
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed! Your API is working correctly!")
    elif total_passed >= 3:
        print("\n✅ Core functionality working! URL extraction may fail for some sites.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
