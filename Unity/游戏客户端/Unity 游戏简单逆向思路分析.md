# Unity 游戏简单逆向思路分析



# 一、AssetStudio解包美术资产/shader

直接去Github的AssetStudio仓库中拉取最新的release文件，打开GUI.exe使用即可提取AB包。



# 二、有关代码文件

> 以下内容暂且只包含没做加密的项目，仅供学习，不涉及侵权问题，也不会给出具体的游戏画面和美术资产。

## 1.IL2CPP

基本流程参考这篇文章：[【游戏开发进阶】教你使用IL2CppDumper从Unity il2cpp的二进制文件中获取类型、方法、字段等（反编译）-CSDN博客](https://blog.csdn.net/linxinfa/article/details/116572369)

以下是一些实际应用中的补充：

【1】在IL2CppDumper运行之后，我们用DotPeek打开DummyDll中的文件，此时就可以看到类似如下：

![image-20250208225039818](Unity%20%E6%B8%B8%E6%88%8F%E7%AE%80%E5%8D%95%E9%80%86%E5%90%91%E6%80%9D%E8%B7%AF%E5%88%86%E6%9E%90.assets/image-20250208225039818.png)

这里的VA字段是我们关注的。



【2】IDA加载IL2CppDumper反编译前的GameAssembly.dll文件，