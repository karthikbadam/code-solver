"""
RNA Strand Folding Score
Difficulty: Medium
Topics: dynamic-programming, string, biology

In RNA biology, nucleotide sequences can fold and form base pairs. Given a string 
representing an RNA sequence containing only characters 'A', 'U', 'G', and 'C', 
calculate the maximum folding score. A folding score is calculated by the number 
of valid base pairs that can be formed under these rules:

1. A can pair with U
2. G can pair with C  
3. Each nucleotide can pair with at most one other nucleotide
4. Base pairs cannot cross (if i-j and k-l are pairs, we cannot have i < k < j < l)

Return the maximum possible folding score.

Examples:
- AUUGC → 2 (A-U at (0,1) and G-C at (3,4))
- GCAU → 1 (either G-C or A-U, not both due to crossing)
- AAUU → 2 (both A's pair with U's without crossing)
"""

def maxRNAFoldingScore(sequence: str) -> int:
    """
    Calculate the maximum RNA folding score for a given sequence.
    
    Args:
        sequence (str): RNA sequence containing only 'A', 'U', 'G', 'C'
    
    Returns:
        int: Maximum possible folding score
    """
    n = len(sequence)
    
    # Initialize DP table with zeros
    # dp[i][j] represents max score for substring from i to j
    dp = [[0] * n for _ in range(n)]
    
    # Helper function to check if two bases can pair
    def can_pair(x: str, y: str) -> bool:
        return (x == 'A' and y == 'U') or \
               (x == 'U' and y == 'A') or \
               (x == 'G' and y == 'C') or \
               (x == 'C' and y == 'G')
    
    # Fill DP table
    # l is the length of substring being considered
    for l in range(2, n + 1):
        # i is the start position of substring
        for i in range(n - l + 1):
            j = i + l - 1  # j is end position of substring
            
            # Case 1: Don't pair position i, move to i+1
            dp[i][j] = dp[i + 1][j]
            
            # Case 2: Pair i with some position k where i < k <= j
            for k in range(i + 1, j + 1):
                if can_pair(sequence[i], sequence[k]):
                    score = 1  # Score for pairing i with k
                    if k < j:
                        score += dp[k + 1][j]  # Add score for substring after k
                    if i + 1 < k:
                        score += dp[i + 1][k - 1]  # Add score for substring between i and k
                    dp[i][j] = max(dp[i][j], score)
    
    return dp[0][n - 1]


# Test cases
def test_maxRNAFoldingScore():
    """Test the RNA folding score function"""
    
    # Test case 1: Basic example
    assert maxRNAFoldingScore("AUUGC") == 2
    
    # Test case 2: Non-crossing pairs can coexist  
    assert maxRNAFoldingScore("GCAU") == 2  # G-C(0,1) and A-U(2,3) don't cross
    
    # Test case 3: Multiple A-U pairs (corrected)
    assert maxRNAFoldingScore("AAUU") == 2  # A(0)-U(3) and A(1)-U(2) don't cross
    
    # Test case 4: Complex case (fixed)
    assert maxRNAFoldingScore("AUGCAU") == 3  # A-U, G-C, A-U
    
    # Test case 5: Maximum pairing
    assert maxRNAFoldingScore("GGGGCCCC") == 4
    
    # Test case 6: Example with limited pairing options  
    assert maxRNAFoldingScore("AUGU") == 1  # Only A-U pairing possible
    
    # Test case 7: No pairs possible
    assert maxRNAFoldingScore("AC") == 0
    
    # Test case 8: Complex optimal case (fixed)
    assert maxRNAFoldingScore("GCAUGCAU") == 4  # Multiple optimal pairings
    
    print("All tests passed!")


if __name__ == "__main__":
    test_maxRNAFoldingScore()
    
    # Example usage
    examples = ["AUUGC", "GCAU", "AAUU", "GCAUGCAU"]
    for seq in examples:
        score = maxRNAFoldingScore(seq)
        print(f"Sequence: {seq}, Max Folding Score: {score}")