# Instruct-Pix2Pix 源码阅读

# 一、Test

## 1.模型加载阶段

### （1）Ema

来自`ddpm_edit.py`文件的第105行左右：

```python
if self.use_ema and load_ema:
    self.model_ema = LitEma(self.model)
    print(f"Keeping EMAs of {len(list(self.model_ema.buffers()))}.")
```

GPT对此的解释如下：

> `LitEma` 是一个在深度学习训练过程中常用于实现 Exponential Moving Average (EMA) 的类。EMA 是一种对模型参数进行平滑处理的技术，可以在训练过程中提升模型的性能和稳定性。
>
> ### LitEma 的作用：
>
> 1. **平滑参数更新**：EMA 保持了模型参数的加权平均值，这通常比直接使用当前参数提供更稳定的预测。
> 2. **提升泛化能力**：通过使用 EMA，模型在测试时可能会表现得更加稳健，因为它减少了噪声对参数更新的影响。
> 3. **减少过拟合风险**：EMA 可以帮助缓解训练过程中的过拟合问题，使得最终模型在验证集或测试集上的表现更佳。
> 4. **易于实现**：EMA 的实现相对简单，只需要在每次参数更新后，按照某个衰减率更新 EMA 参数即可。



### （2）eps & x0

> 在扩散模型（Diffusion Models）中，`eps` 和 `x0` 是两种不同的参数化方法，用于描述和处理模型中的噪声。
>
> ### `eps` 参数化
>
> - **定义**: 在 `eps` 参数化中，模型直接预测给定图像样本的噪声（即干扰项），而不是直接预测目标图像。这个参数化方式通常是在训练时将真实图像与加噪声图像之间的差异作为目标。
> - **公式**:
>   - 在代码中，`lvlb_weights = self.betas ** 2 / (2 * self.posterior_variance * to_torch(alphas) * (1 - self.alphas_cumprod))` 是计算与 `eps` 参数化相关的权重。这里利用了模型的后验方差和累积乘积来调整权重，从而对预测的噪声进行加权。
>
> ### `x0` 参数化
>
> - **定义**: 在 `x0` 参数化中，模型直接预测的是去噪后的图像（原始图像），而不是噪声。这种方式通常会简单明了地表示生成过程，特别是对于反向扩散过程的理解。
> - **公式**:
>   - 在代码中，`lvlb_weights = 0.5 * np.sqrt(torch.Tensor(alphas_cumprod)) / (2. * 1 - torch.Tensor(alphas_cumprod))` 是计算与 `x0` 参数化相关的权重。在这里，使用了`alphas_cumprod`（累积的 alpha 值）来帮助计算权重，并且方式上与 `eps` 不同。
>
> ### 总结
>
> - **`eps`**: 参数化为噪声预测，即模型学习如何预测输入图像中的噪声成分。
> - **`x0`**: 参数化为原始图像预测，即模型学习如何从噪声中恢复出原始或无噪声的图像。
>
> 选择哪种参数化方式取决于具体的任务和模型架构。每种参数化都有其优缺点，对于不同的应用场景可能会有不同的效果。



### （3）CLIP

这里用的是OpenAI训练好的，具体的huggingface的链接为：https://huggingface.co/openai/clip-vit-large-patch14/tree/main，这里我们用Pytorch的话模型参数只需要下载pytorch_model.bin这个文件和其他的config.json等文件就行。然后在instructPix2Pix的路径下新建一个openai的空文件夹，把下载的那些文件拖拽进去即可。

