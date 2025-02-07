# C# 面经总结



# 一、基础问题

## 1.`Equals`和`GetHashCode`的重写

> 在C#中，`Equals` 和 `GetHashCode` 是两个重要的方法，通常用于对象的比较和哈希表操作。以下是它们的详细解释以及何时需要重写它们。
>
> ### 1. Equals 方法
>
> `Equals` 方法用于比较两个对象是否相等。C#中的 `Equals` 方法有两种形式：
>
> - **实例方法**：`public virtual bool Equals(object obj)`
> - **静态方法**：`public static bool Equals(object objA, object objB)`
>
> 默认情况下，`Equals` 方法（实例方法）在 `System.Object` 中实现为引用相等性检查，即比较两个对象是否引用同一个内存地址。
>
> #### 何时需要重写 `Equals` 方法？
>
> - **值类型**：对于值类型（如结构体），默认的 `Equals` 方法会进行逐字段的比较，但效率较低。如果你希望自定义值类型的相等性比较逻辑，可以重写 `Equals` 方法。
>   
> - **引用类型**：对于引用类型，如果你希望基于对象的内容（而不是引用）来判断相等性，则需要重写 `Equals` 方法。例如，对于自定义类，你可能希望根据某些字段或属性来判断两个对象是否相等。
>
> #### 重写 `Equals` 方法的注意事项：
>
> - **对称性**：如果 `a.Equals(b)` 返回 `true`，那么 `b.Equals(a)` 也应该返回 `true`。
> - **传递性**：如果 `a.Equals(b)` 返回 `true` 且 `b.Equals(c)` 返回 `true`，那么 `a.Equals(c)` 也应该返回 `true`。
> - **一致性**：多次调用 `a.Equals(b)` 应该始终返回相同的结果，前提是对象没有被修改。
> - **非空性**：`a.Equals(null)` 应该返回 `false`。
>
> ### 2. GetHashCode 方法
>
> `GetHashCode` 方法返回对象的哈希码，通常用于哈希表（如 `Dictionary`、`HashSet` 等）中快速查找对象。
>
> #### 何时需要重写 `GetHashCode` 方法？
>
> - **重写 `Equals` 方法时**：如果你重写了 `Equals` 方法，通常也需要重写 `GetHashCode` 方法，以确保相等的对象具有相同的哈希码。这是哈希表正确工作的前提条件。
>
> #### 重写 `GetHashCode` 方法的注意事项：
>
> - **一致性**：如果两个对象通过 `Equals` 方法比较相等，那么它们的 `GetHashCode` 方法必须返回相同的值。
> - **高效性**：`GetHashCode` 方法应该尽可能高效，因为它可能会被频繁调用。
> - **分布均匀**：哈希码应该尽可能均匀分布，以减少哈希冲突。
>
> ### 示例
>
> 假设有一个 `Person` 类，我们希望根据 `Name` 和 `Age` 属性来判断两个 `Person` 对象是否相等：
>
> ```csharp
> public class Person
> {
>     public string Name { get; set; }
>     public int Age { get; set; }
> 
>     public override bool Equals(object obj)
>     {
>         if (obj == null || GetType() != obj.GetType())
>         {
>             return false;
>         }
> 
>         Person other = (Person)obj;
>         return Name == other.Name && Age == other.Age;
>     }
> 
>     public override int GetHashCode()
>     {
>         // 使用 Name 和 Age 的哈希码组合
>         return HashCode.Combine(Name, Age);
>     }
> }
> ```
>
> 在这个例子中，我们重写了 `Equals` 和 `GetHashCode` 方法，以确保两个 `Person` 对象在 `Name` 和 `Age` 相同时被认为是相等的，并且它们的哈希码也相同。
>
> ### 总结
>
> - **重写 `Equals`**：当你需要自定义对象的相等性比较逻辑时。
> - **重写 `GetHashCode`**：当你重写了 `Equals` 方法时，通常也需要重写 `GetHashCode` 方法，以确保相等的对象具有相同的哈希码。
>
> 通过正确实现这两个方法，可以确保你的对象在集合（如 `Dictionary`、`HashSet` 等）中能够正确工作。