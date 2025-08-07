"""
Problem: Two Sum
Difficulty: Easy
Topics: array, hash-table

Description:
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Examples:
Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]
Explanation: Because nums[1] + nums[2] == 6, we return [1, 2].

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 6, we return [0, 1].

Constraints:
• 2 <= nums.length <= 10^4
• -10^9 <= nums[i] <= 10^9
• -10^9 <= target <= 10^9
• Only one valid answer exists.
"""

from typing import List, Optional, Dict, Any
import pytest


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        Find two numbers that add up to target and return their indices.
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        
        Args:
            nums: List of integers
            target: Target sum
            
        Returns:
            List of two indices
        """
        # Hash map to store number -> index mapping
        num_to_index = {}
        
        for i, num in enumerate(nums):
            complement = target - num
            
            # Check if complement exists in our hash map
            if complement in num_to_index:
                return [num_to_index[complement], i]
            
            # Store current number and its index
            num_to_index[num] = i
        
        # Should never reach here given problem constraints
        return []


# Test cases
class TestSolution:
    def setup_method(self):
        self.solution = Solution()
    
    def test_example_1(self):
        nums = [2, 7, 11, 15]
        target = 9
        result = self.solution.twoSum(nums, target)
        assert result == [0, 1]
    
    def test_example_2(self):
        nums = [3, 2, 4]
        target = 6
        result = self.solution.twoSum(nums, target)
        assert result == [1, 2]
    
    def test_example_3(self):
        nums = [3, 3]
        target = 6
        result = self.solution.twoSum(nums, target)
        assert result == [0, 1]
    
    def test_negative_numbers(self):
        nums = [-1, -2, -3, -4, -5]
        target = -8
        result = self.solution.twoSum(nums, target)
        assert result == [2, 4]  # -3 + -5 = -8


if __name__ == "__main__":
    # Quick manual testing
    solution = Solution()
    
    # Example usage:
    result = solution.twoSum([2, 7, 11, 15], 9)
    print(f"Result: {result}")  # Should print [0, 1]
    
    # Run tests
    pytest.main([__file__])