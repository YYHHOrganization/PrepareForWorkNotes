# enable_shared_from_this

### 通俗解释：`enable_shared_from_this` 是什么？

想象你有一栋房子（对象），房子自己需要知道房产证（`shared_ptr`）在哪里。`enable_shared_from_this` 就是给房子装了个特殊装置，让它能安全地拿到自己的房产证复印件。

#### 核心作用：
让对象内部能安全获取指向自己的 `shared_ptr`，避免创建多个独立的智能指针导致内存被多次删除。

---

### 为什么需要它？直接看问题场景

```cpp
class Cat {
public
    void Meow() {
         危险操作！直接创建新shared_ptr
        stdshared_ptrCat badPtr(this);
    }
};

int main() {
    auto cat = stdmake_sharedCat();
    cat-Meow();  灾难：两个独立的shared_ptr指向同一对象
}
```
当程序结束时：
1. `cat` 析构 → 删除 Cat 对象
2. `badPtr` 析构 → 再次删除同一对象！ → 程序崩溃 💥

---

### 正确使用方式

```cpp
#include memory

 关键步骤：继承 enable_shared_from_this
class SafeCat  public stdenable_shared_from_thisSafeCat {
public
    void SafeMeow() {
         安全获取指向自己的shared_ptr
        stdshared_ptrSafeCat safePtr = shared_from_this();
         现在可以安全传递这个指针了...
    }
};

int main() {
     必须用shared_ptr创建对象（重要！）
    auto cat = stdmake_sharedSafeCat();
    cat-SafeMeow();  安全：所有指针共享同一份计数
}
```

#### 工作原理图解
```
             控制块
          +------------+
           引用计数 = 2 
           weak计数 = 1 
          +-----▲------+
                │
                │
+---------------┼------------------+
 SafeCat 对象                      
  继承 enable_shared_from_this     
  内部隐藏的 weak_ptr◄─────────────┘
+-----------------------------------+
         ▲              ▲
         │              │
         │              │
    main中的cat    SafeMeow中的safePtr
```

---

### 必须遵守的规则

1. 必须公有继承  
   ```cpp 
   class T  public stdenable_shared_from_thisT { ... }
   ```

2. 对象必须由 `shared_ptr` 管理  
   错误示例：
   ```cpp
   SafeCat localCat;  栈对象，未用shared_ptr管理
   localCat.SafeMeow();  抛出 stdbad_weak_ptr 异常
   ```

3. 禁止在构造函数内调用  
   对象构造完成前控制块尚未建立：
   ```cpp
   SafeCat() {
       shared_from_this();  错误！会崩溃
   }
   ```

---

### 实际应用场景
当对象需要把自己的智能指针传给其他组件时：
```cpp
class GameCharacter 
     public stdenable_shared_from_thisGameCharacter 
{
public
    void JoinTeam() {
         把自身指针传给队伍系统
        TeamSystemRegister(shared_from_this());
    }
};

 使用
auto player = stdmake_sharedGameCharacter();
player-JoinTeam();   安全传递智能指针
```

---

### 总结：新手记忆要点

 要点  说明 
------------
 做什么用  **让对象内部能安全获取自己的 `shared_ptr`** 
 何时用  当对象需要把自身指针传递给其他组件时 
 怎么用  1. 继承它br2. 用 `shared_from_this()` 获取指针br3. 对象必须由 `shared_ptr` 创建 
 禁止场景  1. 未被 `shared_ptr` 管理的对象br2. 构造函数内调用 
 错误代价  双重释放 → 程序崩溃 

 就像你不能自己给自己发房产证一样，`enable_shared_from_this` 是对象获取合法身份证明的安全通道。