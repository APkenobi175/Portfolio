
from typing import List


class Solution:
    def runningSum(self, nums: List[int]) -> List[int]:
        newnum = 0
        res = []
        for i in range(len(nums)):
            newnum = nums[i] + newnum
            res.append(newnum)
        return res
   