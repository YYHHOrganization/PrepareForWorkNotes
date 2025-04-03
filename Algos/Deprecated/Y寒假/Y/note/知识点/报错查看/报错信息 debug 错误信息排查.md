## 越界

 --leetcode

快排时候(下面这个是已经对的)

`while(i<j)//【拜托你为啥会协程L<R 这俩都不改变的。。】`  写错 报的错

```C++
class Solution {
public:
//5min可出去
    //1、找到pivot
    //2、用pivot分割序列，左边都是<=的，右边都是>=的
    //3、左右两边分别递归qsort
    //4、退出条件是l>=r
    void qsort(vector<int>& nums,int l,int r)
    {
        if(l>=r)return;
        int pivot = nums[l+((r-l)>>1)];//nums[l+(r-l)>>1];这是错的
        int i=l-1,j=r+1;
        while(i<j)//【拜托你为啥会协程L<R 这俩都不改变的。。】
        {
            do i++;while(nums[i]<pivot);
            do j--;while(nums[j]>pivot);
            if(i<j)swap(nums[i],nums[j]);
        }
        qsort(nums,l,j);
        qsort(nums,j+1,r);
    }
    vector<int> sortArray(vector<int>& nums) 
    {
        qsort(nums,0,nums.size()-1);
        return nums;
    }
};
```



这个错误信息表明在代码的第1122行，第34个字符处发生了一个运行时错误。具体来说，错误是由于对一个无符号偏移量进行加法操作时发生了溢出，导致结果从 `0x502000000090` 溢出到了 `0x50200000008c`。这个错误通常发生在使用C++标准库中的 `std::vector` 时。

### 可能的原因：
1. **越界访问**：你可能在访问 `std::vector` 时使用了超出其范围的索引。例如，如果你有一个大小为 `n` 的 `std::vector`，但你尝试访问第 `n+1` 个元素，就会导致这种错误。

2. **无符号整数溢出**：`std::vector` 的 `size()` 函数返回的是一个无符号整数（通常是 `size_t` 类型）。如果你在对这个无符号整数进行加法或减法操作时，结果超出了无符号整数的表示范围，就会发生溢出。

3. **迭代器失效**：如果你在使用迭代器遍历 `std::vector` 时，修改了 `std::vector`（例如添加或删除元素），可能会导致迭代器失效，进而引发类似的错误。

### 如何排查和修复：
1. **检查索引范围**：确保你在访问 `std::vector` 时使用的索引在有效范围内（即 `0` 到 `size() - 1`）。

2. **检查无符号整数运算**：如果你在对 `size()` 的结果进行运算，确保不会发生溢出。例如，如果你要计算 `size() - 1`，确保 `size()` 不为 `0`。

3. **检查迭代器使用**：如果你在使用迭代器，确保在遍历过程中没有修改 `std::vector`。

### 示例代码：
```cpp
#include <vector>
#include <iostream>

int main() {
    std::vector<int> vec = {1, 2, 3, 4, 5};

    // 错误的访问方式，可能导致越界
    for (size_t i = 0; i <= vec.size(); ++i) {
        std::cout << vec[i] << std::endl;  // 当 i == vec.size() 时，访问越界
    }

    // 正确的访问方式
    for (size_t i = 0; i < vec.size(); ++i) {
        std::cout << vec[i] << std::endl;
    }

    return 0;
}
```

在上面的代码中，第一个循环会导致越界访问，从而可能引发类似的运行时错误。第二个循环是正确的访问方式。

### 总结：
这个错误通常是由于越界访问或无符号整数溢出引起的。你需要仔细检查代码中对 `std::vector` 的访问和操作，确保它们在有效范围内进行。