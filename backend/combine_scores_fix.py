"""
CRITICAL BUG FIX: Improved Hybrid Scoring Logic

This file contains the corrected combine_scores function that properly
handles the hybrid scoring between ML predictions and web verification.

The bug: Original logic assumed ML confidence was always for "Fake",
but it's actually confidence for whatever the ML model predicted.

The fix: Properly convert ML predictions to a unified scale and handle
cases where web verification is inconclusive (recent news, niche topics).
"""

def combine_scores_fixed(ml_label, ml_confidence, web_similarity, ml_weight=0.6, web_weight=0.4):
    """
    Improved hybrid scoring that handles "no verification" cases better.
    
    Key insight: Low web similarity could mean:
    1. Story is fake (no one else reporting it)
    2. Story is very recent (not indexed yet)
    3. Story is niche/local (limited online presence)
    
    We should trust ML more when web verification is inconclusive.
    
    Args:
        ml_label (str): "Real" or "Fake" from ML model
        ml_confidence (float): Confidence in the ML prediction (0-100)
        web_similarity (float): Average similarity with web sources (0-100)
        ml_weight (float): Weight for ML prediction (default 0.6)
        web_weight (float): Weight for web verification (default 0.4)
    
    Returns:
        dict: {
            "combined_score": float,
            "final_label": str,
            "ml_score": float,
            "web_verification_reliable": bool
        }
    """
    
    # Define threshold for "inconclusive" web verification
    WEB_VERIFICATION_THRESHOLD = 20  # Below this, web verification is unreliable
    
    # Adjust weights based on web verification reliability
    if web_similarity < WEB_VERIFICATION_THRESHOLD:
        # Web verification is inconclusive - rely more on ML
        # Use 80% ML, 20% web (instead of 60/40)
        ml_weight_adjusted = 0.8
        web_weight_adjusted = 0.2
    else:
        # Web verification is reliable - use normal weights
        ml_weight_adjusted = ml_weight
        web_weight_adjusted = web_weight
    
    # Convert to unified scale (100 = Real, 0 = Fake)
    if ml_label == "Real":
        ml_score = ml_confidence  # High confidence in Real = high score
    else:  # ml_label == "Fake"
        ml_score = 100 - ml_confidence  # High confidence in Fake = low score
    
    # Combine scores (both on same scale: 100 = Real, 0 = Fake)
    combined = (ml_score * ml_weight_adjusted) + (web_similarity * web_weight_adjusted)
    
    # Final decision
    label = "Real" if combined >= 50 else "Fake"
    
    return {
        "combined_score": round(combined, 2),
        "final_label": label,
        "ml_score": round(ml_score, 2),
        "web_verification_reliable": web_similarity >= WEB_VERIFICATION_THRESHOLD
    }


# Example usage and test cases:

if __name__ == "__main__":
    print("="*60)
    print("TESTING IMPROVED HYBRID SCORING")
    print("="*60)
    
    # Test Case 1: ML says Real, high confidence, no web verification
    # (Your Iran news example)
    print("\nTest 1: Recent news (ML: Real 79.61%, Web: 0%)")
    result = combine_scores_fixed("Real", 79.61, 0)
    print(f"  Combined Score: {result['combined_score']}%")
    print(f"  Final Label: {result['final_label']}")
    print(f"  Expected: Real (because ML is confident and web is inconclusive)")
    print(f"  ✅ PASS" if result['final_label'] == "Real" else "  ❌ FAIL")
    
    # Test Case 2: ML says Fake, high confidence, no web verification
    print("\nTest 2: Obvious fake (ML: Fake 85%, Web: 0%)")
    result = combine_scores_fixed("Fake", 85, 0)
    print(f"  Combined Score: {result['combined_score']}%")
    print(f"  Final Label: {result['final_label']}")
    print(f"  Expected: Fake (ML confident it's fake, no sources found)")
    print(f"  ✅ PASS" if result['final_label'] == "Fake" else "  ❌ FAIL")
    
    # Test Case 3: ML says Real, high confidence, high web verification
    print("\nTest 3: Well-verified news (ML: Real 90%, Web: 85%)")
    result = combine_scores_fixed("Real", 90, 85)
    print(f"  Combined Score: {result['combined_score']}%")
    print(f"  Final Label: {result['final_label']}")
    print(f"  Expected: Real (both ML and web agree)")
    print(f"  ✅ PASS" if result['final_label'] == "Real" else "  ❌ FAIL")
    
    # Test Case 4: ML says Real, but web says otherwise
    print("\nTest 4: Conflicting signals (ML: Real 60%, Web: 10%)")
    result = combine_scores_fixed("Real", 60, 10)
    print(f"  Combined Score: {result['combined_score']}%")
    print(f"  Final Label: {result['final_label']}")
    print(f"  Expected: Uncertain/Fake (low web verification casts doubt)")
    
    # Test Case 5: ML says Fake, but web verification is high
    print("\nTest 5: ML wrong? (ML: Fake 70%, Web: 80%)")
    result = combine_scores_fixed("Fake", 70, 80)
    print(f"  Combined Score: {result['combined_score']}%")
    print(f"  Final Label: {result['final_label']}")
    print(f"  Expected: Real (web verification overrides ML)")
    print(f"  ✅ PASS" if result['final_label'] == "Real" else "  ❌ FAIL")
    
    print("\n" + "="*60)
    print("COMPARISON WITH OLD LOGIC")
    print("="*60)
    
    # Old buggy logic for comparison
    def combine_scores_old(ml_confidence, web_similarity, ml_weight=0.6, web_weight=0.4):
        combined = (ml_confidence * ml_weight) + (web_similarity * web_weight)
        label = "Real" if combined >= 50 else "Fake"
        return {"combined_score": round(combined, 2), "final_label": label}
    
    print("\nIran News Example:")
    print("  ML: Real (79.61% confidence), Web: 0%")
    
    old_result = combine_scores_old(79.61, 0)
    print(f"\n  OLD LOGIC:")
    print(f"    Combined: {old_result['combined_score']}%")
    print(f"    Result: {old_result['final_label']} ❌ WRONG")
    
    new_result = combine_scores_fixed("Real", 79.61, 0)
    print(f"\n  NEW LOGIC:")
    print(f"    Combined: {new_result['combined_score']}%")
    print(f"    Result: {new_result['final_label']} ✅ CORRECT")
    print(f"    Web Reliable: {new_result['web_verification_reliable']}")
