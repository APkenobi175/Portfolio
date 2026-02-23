#include <vector>
#include <iostream>

using namespace std;

class Solution {
public:
    vector<int> runningSum(vector<int>& nums) {
        int newnum = 0;
        vector<int> res;
        for(int i = 0; i < nums.size(); i++){
            newnum = nums[i] + newnum;
            res.push_back(newnum);
        }
        return res;

    }
};