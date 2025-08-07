/**
 * Problem: Two Sum
 * Difficulty: Easy
 * Topics: array, hash-table
 * 
 * Description:
 * Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
 * 
 * You may assume that each input would have exactly one solution, and you may not use the same element twice.
 * 
 * You can return the answer in any order.
 * 
 * Examples:
 * Example 1: Input: nums = [2,7,11,15], target = 9, Output: [0,1]
 * Example 2: Input: nums = [3,2,4], target = 6, Output: [1,2]
 * Example 3: Input: nums = [3,3], target = 6, Output: [0,1]
 * 
 * Constraints:
 * • 2 <= nums.length <= 10^4
 * • -10^9 <= nums[i] <= 10^9
 * • -10^9 <= target <= 10^9
 * • Only one valid answer exists.
 */

interface TestCase {
  input: [number[], number];
  expectedOutput: number[];
  description: string;
}

class Solution {
  /**
   * Find two numbers that add up to target and return their indices.
   * 
   * Time Complexity: O(n)
   * Space Complexity: O(n)
   * 
   * @param nums Array of integers
   * @param target Target sum
   * @returns Array of two indices
   */
  twoSum(nums: number[], target: number): number[] {
    // Hash map to store number -> index mapping
    const numToIndex = new Map<number, number>();
    
    for (let i = 0; i < nums.length; i++) {
      const num = nums[i];
      const complement = target - num;
      
      // Check if complement exists in our hash map
      if (numToIndex.has(complement)) {
        return [numToIndex.get(complement)!, i];
      }
      
      // Store current number and its index
      numToIndex.set(num, i);
    }
    
    // Should never reach here given problem constraints
    return [];
  }
}

// Test cases
const testCases: TestCase[] = [
  {
    input: [[2, 7, 11, 15], 9],
    expectedOutput: [0, 1],
    description: "Example 1: Basic case with solution at beginning"
  },
  {
    input: [[3, 2, 4], 6],
    expectedOutput: [1, 2],
    description: "Example 2: Solution not at beginning"
  },
  {
    input: [[3, 3], 6],
    expectedOutput: [0, 1],
    description: "Example 3: Duplicate numbers"
  },
  {
    input: [[-1, -2, -3, -4, -5], -8],
    expectedOutput: [2, 4],
    description: "Negative numbers"
  }
];

// Test runner
function runTests(): void {
  const solution = new Solution();
  let passed = 0;
  let total = testCases.length;

  console.log(`Running ${total} test cases...\n`);

  testCases.forEach((testCase, index) => {
    try {
      const [nums, target] = testCase.input;
      const result = solution.twoSum(nums, target);
      
      // Check if result matches expected (order may vary)
      const isEqual = JSON.stringify(result.sort()) === JSON.stringify(testCase.expectedOutput.sort());
      
      if (isEqual) {
        console.log(`✅ Test ${index + 1}: ${testCase.description} - PASSED`);
        passed++;
      } else {
        console.log(`❌ Test ${index + 1}: ${testCase.description} - FAILED`);
        console.log(`   Expected: ${JSON.stringify(testCase.expectedOutput)}`);
        console.log(`   Got: ${JSON.stringify(result)}`);
      }
    } catch (error) {
      console.log(`❌ Test ${index + 1}: ${testCase.description} - ERROR`);
      console.log(`   Error: ${error}`);
    }
  });

  console.log(`\n${passed}/${total} tests passed`);
}

// Export for testing framework
export { Solution, testCases, runTests };

// Run tests if this file is executed directly
if (require.main === module) {
  runTests();
}