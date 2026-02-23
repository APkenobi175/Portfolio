
/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* runningSum(int* nums, int numsSize, int* returnSize) {
    *returnSize = numsSize;
    int newnum = 0;
    int* res = malloc(numsSize * sizeof(int));
    for(int i = 0; i<numsSize; i++){
        newnum = nums[i] + newnum;
        res[i] = newnum;
    }
    return res;
    
}