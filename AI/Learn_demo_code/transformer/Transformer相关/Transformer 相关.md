## Transformer 相关



## 一、Self-attention 机制介绍

### 1.Scaled Dot-Producted Attention

关于self-attention的介绍，李宏毅大佬的课程讲的非常详细了：
[第四节 2021 - 自注意力机制(Self-attention)(上)_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Wv411h7kN/?p=38)

[2021 - 自注意力机制 (Self-attention) (下)_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Wv411h7kN?p=39&vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99)

最关键的核心部分就在于下面这个公式：
![image-20231022144625332](Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231022144625332.png)

其中的Q,K,V都是将输入序列向量按行摆得到的结果，具体来说size应该是**seq_Len * dim**。在原论文中dim_k和dim_v是相等的。

接下来，来写一个Self-attention的相关pytorch代码：

```python
from math import sqrt
import torch
from torch import nn

class Self_Attention(nn.Module):
    # input : batch_size * seq_len * input_dim
    # q : batch_size * input_dim * dim_k
    # k : batch_size * input_dim * dim_k
    # v : batch_size * input_dim * dim_v
    def __init__(self, input_dim, dim_k, dim_v):
        super(Self_Attention, self).__init__()
        self.q = nn.Linear(input_dim, dim_k)
        self.k = nn.Linear(input_dim, dim_k)
        self.v = nn.Linear(input_dim, dim_v)
        self._norm_fact = 1 / sqrt(dim_k)

    def forward(self, x):
        # x: batch_size * seq_len * input_dim
        Q = self.q(x)  # batch_size * seq_len * dim_k
        K = self.k(x)  # batch_size * seq_len * dim_k
        V = self.v(x)  # batch_size * seq_len * dim_v

        atten = nn.Softmax(dim=-1)(torch.bmm(Q, K.permute(0, 2, 1))) * self._norm_fact  # Q * K.T(), batch_size * seq_len * seq_len
        output = torch.bmm(atten, V)  # batch_size * seq_len * dim_v
        return output
    
```

> 相关Python及Pytorch语法补充：
> 【1】关于import xxx 和 from xxx import yyy的区别：[【精选】from xxx import xxx 和 import xxx的区别 ](https://blog.csdn.net/hxxjxw/article/details/107708755)
>
> 【2】`nn.Linear`： [Linear — PyTorch 2.1 documentation](https://pytorch.org/docs/stable/generated/torch.nn.Linear.html)。经过全连接层后的输出与输入的数据除了最后一个维度变了其他维度都是不变的。
>
> 【3】`torch.bmm`：[torch.bmm — PyTorch 2.1 documentation](https://pytorch.org/docs/stable/generated/torch.bmm.html)，直观理解其实就是忽略第一维（即batch_size）的矩阵乘法。
>
> 对于`atten = nn.Softmax(dim=-1)(torch.bmm(Q, K.permute(0, 2, 1))) * self._norm_fact`这段代码，`K.permute(0, 2, 1)`指的也是K在保持第一维度不变时的矩阵转置。**所以这行代码其实就是上图那个公式。**

对搭建的网络进行简单测试：

```python
import torch
from self_attention import Self_Attention

X = torch.randn(4, 3, 2)  # batch_size * seq_len * input_dim
self_attention = Self_Attention(2, 4, 5)
res = self_attention(X)
print(res)
print(res.size())
```

输出结果如下：
![image-20231022152239813](Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231022152239813.png)

------



### 2.Multi-head Self-attention

相关的原理，依旧可以参考李宏毅大佬的视频：[2021 - 自注意力机制 (Self-attention) (下)_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Wv411h7kN?p=39&vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99)，大概从15分钟左右开始。

有时间可以看看下面的文章：[Multi-Head-Attention的作用到底是什么? - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/626820422)

简单来说，Multi-head可以用下图来形容：

![image-20231022155330767](Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231022155330767.png)

参考[Tutorial 6: Transformers and Multi-Head Attention — UvA DL Notebooks v1.2 documentation (uvadlc-notebooks.readthedocs.io)](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial6/Transformers_and_MHAttention.html)，可以给出另一张图：

![image-20231022161612157](Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231022161612157.png)

其实就是把本来的Q，K，V矩阵额外再分出multi-head的head的数量的矩阵，然后对应的head进行attention的求解并求出对应的b，然后可以用一个新的矩阵$W^O$来计算出最后的$b_i$。

下面基于Pytorch实现multi-head self-attention（**注：由于要实现Transformer，这里参考的模型代码链接为[A Comprehensive Guide to Building a Transformer Model with PyTorch | DataCamp](https://www.datacamp.com/tutorial/building-a-transformer-with-py-torch)**，可能相对来说会更严谨一些）：

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttention, self).__init__()
        # Ensure that the model dimension (d_model) is divisible by the number of heads
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"

        # Initialize dimensions
        self.d_model = d_model  # Model's dimension
        self.num_heads = num_heads  # Number of attention heads
        self.d_k = d_model // num_heads  # Dimension of each head's key, query, and value

        # Linear layers for transforming inputs
        self.W_q = nn.Linear(d_model, d_model)  # Query transformation
        self.W_k = nn.Linear(d_model, d_model)  # Key transformation
        self.W_v = nn.Linear(d_model, d_model)  # Value transformation
        self.W_o = nn.Linear(d_model, d_model)  # Output transformation

    # 前面实现的scaled_dot_product_attention的逻辑
    def scaled_dot_product_attention(self, Q, K, V):
        # Calculate attention scores
        attn_scores = torch.matmul(Q, K.transpose(-2, -1)) / sqrt(self.d_k)

        # Softmax is applied to obtain attention probabilities
        attn_probs = torch.softmax(attn_scores, dim=-1)

        # Multiply by values to obtain the final output
        output = torch.matmul(attn_probs, V)
        return output

    def split_heads(self, x):
        # Reshape the input to have num_heads for multi-head attention
        batch_size, seq_length, d_model = x.size()
        return x.view(batch_size, seq_length, self.num_heads, self.d_k).transpose(1, 2)  #  transpose:The given dimensions dim0 and dim1 are swapped.
        # return.shape: [batch_size, self.num_heads, seq_length, self.d_k]

    def combine_heads(self, x):
        # Combine the multiple heads back to original shape
        batch_size, _, seq_length, d_k = x.size()
        # 关于contiguous()函数的意义:https://blog.csdn.net/gdymind/article/details/82662502
        return x.transpose(1, 2).contiguous().view(batch_size, seq_length, self.d_model)

    def forward(self, Q, K, V):  # 实际上传入的可能是(x,x,x)或者(x, enc_output, enc_output)这种
        # Apply linear transformations and split heads
        Q = self.split_heads(self.W_q(Q))
        K = self.split_heads(self.W_k(K))
        V = self.split_heads(self.W_v(V))

        # Perform scaled dot-product attention
        attn_output = self.scaled_dot_product_attention(Q, K, V)

        # Combine heads and apply output transformation
        output = self.W_o(self.combine_heads(attn_output))
        return output
```

补充：关于`torch.matmul`函数的介绍：[torch.matmul — PyTorch 2.1 documentation](https://pytorch.org/docs/stable/generated/torch.matmul.html)

> 关于forward函数的介绍：
>
> The forward method is where the actual computation happens:
>
> 1. Apply Linear Transformations: The queries (Q), keys (K), and values (V) are first passed through linear transformations using the weights defined in the initialization.
> 2. Split Heads: The transformed Q, K, V are split into multiple heads using the split_heads method.
> 3. Apply Scaled Dot-Product Attention: The scaled_dot_product_attention method is called on the split heads.
> 4. Combine Heads: The results from each head are combined back into a single tensor using the combine_heads method.
> 5. Apply Output Transformation: Finally, the combined tensor is passed through an output linear transformation.

**注： Multi-Head Attention里面还可以有个Mask的操作，不过这个我们放在后面学到了再进行总结。**

------



### 3.Positional Encoding

在前面的Self-Attention中，我们并没有引入向量在Sequence所在位置的信息。比如说“Vec1和Vec4”以及“Vec2和Vec3”之间并没有考虑距离的影响。而在做任务中，位置信息往往也是很有用的（比如说对于词性标注任务，动词不太可能出现在句首），而此时的网络还没有考虑这种位置信息。

Positional Encoding就是用来解决这个问题的，示例图如下：

![image-20231023151212281](Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231023151212281.png)

上述参考的文章对此的介绍为：

> Positional Encoding is used to inject the position information of each token in the input sequence. It uses sine and cosine functions of different frequencies to generate the positional encoding.

在《Attention is all you need》这篇初始论文中，作者对此的介绍如下：

![image-20231023151546108](Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231023151546108.png)

也就是说，positional encoding是与input sequence无关的量，可以认为是预定义好的值，只和sequence的最大长度有关。在上面的公式中：

- pos是序列中的word所在的位置；
- d_model是encoding向量的长度（和embedding vector一样）；
- i是上述向量的index value。

下面是示意图：

![img](Transformer%20%E7%9B%B8%E5%85%B3.assets/Embedding-7.png)

其他可以参考的链接：[Transformer Architecture: The Positional Encoding - Amirhossein Kazemnejad's Blog](https://kazemnejad.com/blog/transformer_architecture_positional_encoding/)

接下来，我们会在pytorch中实现Positional Encoding：

```python
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_seq_length):
        super(PositionalEncoding, self).__init__()
        pe = torch.zeros(max_seq_length, d_model)
        position = torch.arange(0, max_seq_length, dtype=torch.float).unsqueeze(1)  # https://pytorch.org/docs/stable/generated/torch.unsqueeze.html
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * -(math.log(10000.0) / d_model))  # 转换一下会发现和论文中公式一样

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x):
        return x + self.pe[:, :x.size(1)]  # todo：是不是可以理解为<END>这种标签不需要PE?
```

介绍如下：

> - d_model: The dimension of the model's input.
> - max_seq_length: The maximum length of the sequence for which positional encodings are pre-computed.
> - pe: A tensor filled with zeros, which will be populated with positional encodings.
> - position: A tensor containing the position indices for each position in the sequence.
> - div_term: A term used to scale the position indices in a specific way.
>
> The sine function is applied to the even indices and the cosine function to the odd indices of pe.
>
> Finally, pe is registered as a buffer, which means it will be part of the module's state but will not be considered a trainable parameter.

 一些新的研究里，Positional Encoding也是能根据数据集被学习出来的，不过这仍然是一个正在被研究的问题（截止到2021年左右，现在不确定）。

------



## 二、Transformer相关

Transformer结构现在有不少变体，有的Transformer架构不包含Decoder，只包含Encoder，不过这里我们还是先介绍最初始的Transformer。

### 1.Seq2Seq介绍

这种模型架构可以参考下面文章：[CS224n笔记[7\]:整理了12小时，只为让你20分钟搞懂Seq2seq - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/147310766)

做简单理解的话，也可以参考李宏毅大佬的视频：[2021 - Transformer (上)_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Wv411h7kN?p=49&vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99)

------



### 2. Transformer-Encoder

注：这部分还没有讲到Transformer网络的训练，只介绍产生结果的过程。

Transformer的Encoder结构如下图所示：

<img src="Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231023162938669.png" alt="image-20231023162938669" style="zoom:80%;" />

一些关于上图的解释：

- （1）Positional Encoding：在第一章节的第3部分有进行介绍，算是对self-attention引入位置相关的信息；
- （2）Add-Norm：其中的Add操作是由Residual Connection带来的，个人理解这是一种利用残差的思想，类似ResNet。而Norm操作则是layer-norm。
- （3）Nx的意思是这种块会重复很多组，共同构成Transformer的Encoder部分。
- （4）关于Feed Forward网络部分的介绍如下；



#### （1）Feed Forward Network

《Attention is All You Need》一文中，对此的介绍为：

![image-20231023163722004](Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231023163722004.png)

其实简单来说就是一个全连接层+ReLU+一个全连接层。Pytorch实现如下：

```python
class PositionWiseFeedForward(nn.Module):
    def __init__(self, d_model, d_ff):
        super(PositionWiseFeedForward, self).__init__()
        self.fc1 = nn.Linear(d_model, d_ff)
        self.fc2 = nn.Linear(d_ff, d_model)
        self.relu = nn.ReLU()

    def forward(self, x):
        return self.fc2(self.relu(self.fc1(x)))
```

------



#### （2）相关代码

有了以上的知识，就可以动手搭建基于Pytorch的transformer encoder的一个块组件了：

```python
class EncoderLayer(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout):
        super(EncoderLayer, self).__init__()
        self.self_atten = MultiHeadAttention(d_model, num_heads)
        self.feed_forward = PositionWiseFeedForward(d_model, d_ff)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        attn_output = self.self_atten(x, x, x)
        x = self.norm1(x + self.dropout(attn_output))  # x + self.dropout(attn_output)就对应上图的残差连接
        ff_output = self.feed_forward(x)
        x = self.norm2(x + self.dropout(ff_output))
        return x
```

> 关于dropout原论文的介绍：
>
> Residual Dropout：We apply **dropout [27] to the output of each sub-layer, before it is added to the sub-layer input and normalized.** In addition, we apply dropout to the sums of the embeddings and the positional encodings in both the encoder and decoder stacks. For the base model, we use a rate of Pdrop = 0.1.

------



### 3.Transformer-Decoder

注：这部分还没有讲到Transformer网络的训练，只介绍产生结果的过程。

接下来介绍Transformer的Decoder部分。

#### （1）Autoregressive Decoder

这也是比较常见的decoder类型，如下图所示：

![Figure 3. The Decoder part of the Transformer network (Souce: Image from the original paper)](Transformer%20%E7%9B%B8%E5%85%B3.assets/Figure_3_The_Decoder_part_of_the_Transformer_network_Souce_Image_from_the_original_paper_b90d9e7f66.png)

上面这张图可能没有那么直观，其实这里的Output Probabilities指的是所有输出的可能性，一个类似于下图的东西：

<img src="Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231023170818008.png" alt="image-20231023170818008" style="zoom:80%;" />

接下来，Decoder会决定输出是什么字符，比如说翻译任务这里得到了”机“字的结果，接着该输出作为下一个”时间点“的输入，整体流程更像是下面一幅图：

<img src="Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231023171011048.png" alt="image-20231023171011048" style="zoom:80%;" />

注：也许这里会出现Error Propagation（一步错，步步错）的问题，不过这里暂时先不讨论，先继续往下看。

另外，这里还有一个**问题**是Decoder现在并没有办法判断任务结束，解决方案是在Output Probabilities的计算中加入一个END字段，使得当任务结束时Decoder有能力将END作为判断的输出，从而结束这个任务：

<img src="Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231023185233101.png" alt="image-20231023185233101" style="zoom:80%;" />



------



##### （a）Decoder的内部结构

**Mask的概念**

注意到Decoder的Multi-Head Attention中引入了一个Masked的概念。如下图：

<img src="Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231023184417990.png" alt="image-20231023184417990" style="zoom:80%;" />

Masked Self-attention和前面的self-attention的区别在于，在计算attention的过程中只考虑左边的向量，而不会考虑右边的向量（比如计算b2的时候只会考虑a1和a2）。这样做是合理的，因为decoder在输出结果的时候是按照顺序生成的，所以只能考虑到左边的内容而不能考虑右边的内容。

> **在计算attention score的时候如何对padding做mask操作？**
>
>- padding位置置为负无穷(一般来说-1000就可以)，再对attention score进行相加。这样的话mask的部分由于值非常小，在做softmax之后就会变成0。

对上述代码的修改部分有：

```python
# class MultiHeadAttention
def scaled_dot_product_attention(self, Q, K, V, mask=None):
    # Calculate attention scores
    attn_scores = torch.matmul(Q, K.transpose(-2, -1)) / sqrt(self.d_k)

    # 核心：mask的相关逻辑
    # Apply mask if provided (useful for preventing attention to certain parts like padding)
    if mask is not None:
        attn_scores = attn_scores.masked_fill(mask == 0, -1e9) 

    # Softmax is applied to obtain attention probabilities
    attn_probs = torch.softmax(attn_scores, dim=-1)
    ...
def forward(self, Q, K, V, mask=None):  # 实际上传入的可能是(x,x,x)或者(x, enc_output, enc_output)这种
    # Apply linear transformations and split heads
    Q = self.split_heads(self.W_q(Q))
    K = self.split_heads(self.W_k(K))
    V = self.split_heads(self.W_v(V))

    # Perform scaled dot-product attention
    attn_output = self.scaled_dot_product_attention(Q, K, V, mask)
    ...
```

```python
# class EncodeLayer
def forward(self, x, mask):
    attn_output = self.self_atten(x, x, x, mask)
    ...
```

其实就是在self-attention的`scaled_dot_product_attention`函数里引入masked的逻辑，并记得在调用该函数的地方和对应类处添加masked参数即可。

------



#### （2）Non-autoregressive（NAT） Decoder

NAT Decoder和Autoregressive（AT） Decoder 的区别如下图：

<img src="Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231023190814297.png" alt="image-20231023190814297" style="zoom: 80%;" />

------



#### （3）Encoder和Decoder之间传递信息

<img src="Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231023191246031.png" alt="image-20231023191246031" style="zoom:80%;" />

Cross Attention实际做的事情，可以用下图来形容：

<img src="Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231023191333470.png" alt="image-20231023191333470" style="zoom:80%;" />

也就是说，实际上Cross Attention是使用Encoder产生k和v向量，使用Decoder产生query（q）向量，来计算attention的操作，得到的结果会进一步输入后面的全连接神经网络中。

注：Decoder不管是哪个block，拿的都是Encoder最后一层的输出，作为Cross Attention的输入。当然这不是绝对的，有些工作也在研究Cross Attention的其他方法。

------



### 4.Decoder的代码实现

```python
class DecoderLayer(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout):
        super(DecoderLayer, self).__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads)
        self.cross_attn = MultiHeadAttention(d_model, num_heads)
        self.feed_forward = PositionWiseFeedForward(d_model, d_ff)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, enc_output, src_mask, tgt_mask):
        attn_output = self.self_attn(x, x, x, tgt_mask)
        x = self.norm1(x + self.dropout(attn_output))
        attn_output = self.cross_attn(x, enc_output, enc_output, src_mask)  # 参数：Q,K,V,其中Q是decoder输出的,K和V是encoder输出的
        x = self.norm2(x + self.dropout(attn_output))
        ff_output = self.feed_forward(x)
        x = self.norm3(x + self.dropout(ff_output))
        return x
```

> 补充说明：
>
> Forward Method **Input**:
>
> 1. x: The input to the decoder layer.
> 2. enc_output: The output from the corresponding encoder (used in the cross-attention step).
> 3. src_mask: Source mask to ignore certain parts of the encoder's output.
> 4. tgt_mask: Target mask to ignore certain parts of the decoder's input.
>
> 
>
> **Processing Steps:**
>
> 1. Self-Attention on Target Sequence: The input x is processed through a self-attention mechanism.
> 2. Add & Normalize (after Self-Attention): The output from self-attention is added to the original x, followed by dropout and normalization using norm1.
> 3. Cross-Attention with Encoder Output: The normalized output from the previous step is processed through a cross-attention mechanism that attends to the encoder's output enc_output.
> 4. Add & Normalize (after Cross-Attention): The output from cross-attention is added to the input of this stage, followed by dropout and normalization using norm2.
> 5. Feed-Forward Network: The output from the previous step is passed through the feed-forward network.
> 6. Add & Normalize (after Feed-Forward): The feed-forward output is added to the input of this stage, followed by dropout and normalization using norm3.
> 7. **Output: The processed tensor is returned as the output of the decoder layer.**



### 5.整个Transformer的代码实现

这里再给出Transformer的结构，方便跟代码对一下：

![image-20231023193351858](Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231023193351858.png)

代码见下：

```python
class Transformer(nn.Module):
    def __init__(self, src_vocab_size, tgt_vocab_size, d_model, num_heads, num_layers, d_ff, max_seq_length, dropout):
        super(Transformer, self).__init__()
        self.encoder_embedding = nn.Embedding(src_vocab_size, d_model)  # The embedding layer maps each input word into an embedding vector, which is a richer representation of the meaning of that word.
        self.decoder_embedding = nn.Embedding(tgt_vocab_size, d_model)
        self.positional_encoding = PositionalEncoding(d_model, max_seq_length)

        self.encoder_layers = nn.ModuleList([EncoderLayer(d_model, num_heads, d_ff, dropout) for _ in range(num_layers)])
        self.decoder_layers = nn.ModuleList([DecoderLayer(d_model, num_heads, d_ff, dropout) for _ in range(num_layers)])

        self.fc = nn.Linear(d_model, tgt_vocab_size)
        self.dropout = nn.Dropout(dropout)

    def generate_mask(self, src, tgt):  # todo:这个逻辑接下来会介绍
        src_mask = (src != 0).unsqueeze(1).unsqueeze(2)
        tgt_mask = (tgt != 0).unsqueeze(1).unsqueeze(3)
        seq_length = tgt.size(1)
        nopeak_mask = (1 - torch.triu(torch.ones(1, seq_length, seq_length), diagonal=1)).bool()
        tgt_mask = tgt_mask & nopeak_mask
        return src_mask, tgt_mask

    def forward(self, src, tgt):
        src_mask, tgt_mask = self.generate_mask(src, tgt)
        src_embedded = self.dropout(self.positional_encoding(self.encoder_embedding(src)))
        tgt_embedded = self.dropout(self.positional_encoding(self.decoder_embedding(tgt)))

        enc_output = src_embedded
        for enc_layer in self.encoder_layers:
            enc_output = enc_layer(enc_output, src_mask)

        dec_output = tgt_embedded
        for dec_layer in self.decoder_layers:
            dec_output = dec_layer(dec_output, enc_output, src_mask, tgt_mask)

        output = self.fc(dec_output)
        return output
```



#### 相关逻辑说明

> 注：这段如果看不太懂的话继续看第6部分，可能会有更好的体会。
>
> 其他可以参考的文档：[Transformer训练及测试阶段的self-attention mask理解 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/616757504)
>
> [浅析Transformer训练时并行问题 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/368592551)

**Generate Mask Method:**

This method is used to create masks for the source and target sequences, ensuring that padding tokens are ignored and that future tokens are not visible during training for the target sequence. The inclusion of masking ensures that the model adheres to the causal dependencies（因果依赖关系） within sequences, ignoring padding tokens and preventing information leakage from future tokens.

**Forward Method:**

This method defines the forward pass for the Transformer, taking source and target sequences and producing the output predictions.

1. Input Embedding and Positional Encoding: The source and target sequences are first embedded using their respective embedding layers and then added to their positional encodings.
2. Encoder Layers: The source sequence is passed through the encoder layers, with the final encoder output representing the processed source sequence.
3. Decoder Layers: The target sequence and the encoder's output are passed through the decoder layers, resulting in the decoder's output.
4. Final Linear Layer: The decoder's output is mapped to the target vocabulary size using a fully connected (linear) layer.



**关于generate_mask函数的分析（来自ChatGPT。。。。我自己没看懂）：**

| 代码                                                         | 解读                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| def generate_mask(self, src, tgt):                           | `generate_mask` 是一个函数，接受两个参数 `src` 和 `tgt`，它的目的是生成用于Transformer模型的输入和输出的掩码。 |
|                                                              | `src_mask` 和 `tgt_mask` 是两个掩码，用于指示输入和输出序列中哪些位置是有效的，哪些位置是无效的（例如，填充位置）。 |
| src_mask = (src != 0).unsqueeze(1).unsqueeze(2)              | `src_mask` 通过检查 `src` 是否不等于0来生成，然后对其进行维度扩展，使其变成一个三维的张量。这个掩码用于输入序列（通常是源语言文本）。 |
| tgt_mask = (tgt != 0).unsqueeze(1).unsqueeze(3)              | `tgt_mask` 通过检查 `tgt` 是否不等于0来生成，然后对其进行维度扩展，使其变成一个四维的张量。这个掩码用于输出序列（通常是目标语言文本）。 |
| seq_length = tgt.size(1)                                     | `seq_length` 是目标序列的长度，通过检查 `tgt` 的第一个维度的大小得到。 |
| nopeak_mask = (1 - torch.triu(torch.ones(1, seq_length, seq_length), diagonal=1)).bool() | `nopeak_mask` 是一个掩码，它的作用是生成一个上三角形的掩码矩阵，该矩阵用于在自注意力机制中阻止模型查看未来的信息。这个掩码通过 `torch.triu` 函数生成，其中 `diagonal=1` 表示只保留主对角线以上的元素，并将其全部设置为1。然后使用 `bool()` 将其转换为布尔值类型。 |
| tgt_mask = tgt_mask & nopeak_mask                            | 最后，`tgt_mask` 与 `nopeak_mask` 进行按位与操作，将 `tgt_mask` 中的一些位置标记为无效，以便在解码时不会看到未来的信息。 |

总之，这个函数的主要目的是生成用于Transformer模型的输入和输出序列的掩码，确保模型在处理序列数据时能够正确地处理无效位置，同时在解码时不会看到未来的信息。这是Transformer模型中关键的一部分，用于自注意力机制和位置编码。

------



### 6.Transformer的训练过程

可以参考的链接：[浅析Transformer训练时并行问题 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/368592551)

这里介绍一下Transformer的训练细节。

step1：标注好每组训练数据和对应的正确答案，即ground truth。

step2：将decoder输出的每个结果与ground truth做一次cross entropy，目标是让所有cross entropy的总和最小。（注意最后一个输出的one-hot要和END向量做一次cross entropy）。

如下图：

<img src="Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231023201544729.png" alt="image-20231023201544729" style="zoom:80%;" />

也就是说，在Decoder进行训练的时候我们要给它看正确答案。但这里有个问题，就是Decoder看到了正确答案但测试的时候没有正确答案，这个问题一会会说。**训练时的这个过程也被称为Teacher Forcing**，具体而言，每次喂给Decoder的序列都是正确的序列，即使decoder可能会推测错误之前的单词。而这可以通过并行化来解决，直接将原来的ground truth+mask喂给decoder，具体见mask部分的分析。

> 具体过程如下：
>
> ![(Image by Author)](Transformer%20%E7%9B%B8%E5%85%B3.assets/Data-1.png)
>
> 1. The input sequence is converted into Embeddings (with Position Encoding) and fed to the Encoder.
> 2. The stack of Encoders processes this and produces an encoded representation of the input sequence.
> 3. The target sequence is prepended with（前面加） a start-of-sentence token, converted into Embeddings (with Position Encoding), and fed to the Decoder.
> 4. The stack of Decoders processes this along with the Encoder stack’s encoded representation to produce an encoded representation of the target sequence.
> 5. The Output layer converts it into word probabilities and the final output sequence.
> 6. The Transformer’s Loss function compares this output sequence with the target sequence from the training data. This loss is used to generate gradients to train the Transformer during back-propagation.

**Teacher Forcing的意义如下：**

>  在训练期间，我们可以使用与测试期间使用的方法相同的方法。换句话说，在循环中运行Transformer，从输出序列中获取最后一个单词，将其附加到Decoder输入，并将其提供给Decoder以进行下一次迭代。最后，当预测到句尾标记时，Loss函数将生成的输出序列与目标序列进行比较，以训练网络。
>
> 这种循环不仅会导致训练花费更长的时间，而且还会使训练模型变得更加困难。该模型必须基于可能错误的第一个预测单词来预测第二个单词，并以此类推。相反，通过将目标序列提供给解码器，我们给了它一个提示，即使它预测了错误的第一个单词，它也可以用正确的第一个单词来预测第二个单词，这样这些错误就不会不断加剧。
>
> 此外，Transformer能够并行输出所有单词而不循环，这大大加快了训练速度。



#### 一些tips

- （1）copy mechanism：可以用在聊天机器人，做文章的摘要。最早具有这种能力的模型叫做Pointer Network，有时间可以了解一下。
- （2）Guided Attention：常用于语音辨识，语音合成领域。
- （3）Beam Search：原理：[What is Beam Search? Explaining The Beam Search Algorithm | Width.ai](https://www.width.ai/post/what-is-beam-search)，有时有用，有时没用。如果任务的答案比较死，可以用Beam Search来帮助找到更好的解。否则如果想让机器产生一些随机性，就可以不用Beam Search。
- （4）之前在Decoder的部分，有提及可能会出现Decoder在训练的时候看到的都是正确答案，这会造成如果测试的时候产生了错误的结果，就很可能继续错下去，对此的解决方案可以是训练的时候给decoder喂一些错误的数据，感兴趣可以参考下图找文献阅读：

<img src="Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20231023203909751.png" alt="image-20231023203909751" style="zoom: 80%;" />

------

#### 相关代码——以随机生成数据集为例

```python
src_vocab_size = 5000
tgt_vocab_size = 5000
d_model = 512
num_heads = 8
num_layers = 6
d_ff = 2048
max_seq_length = 100
dropout = 0.1

transformer = Transformer(src_vocab_size, tgt_vocab_size, d_model, num_heads, num_layers, d_ff, max_seq_length, dropout)

# Generate random sample data
src_data = torch.randint(1, src_vocab_size, (64, max_seq_length))  # (batch_size, seq_length)
tgt_data = torch.randint(1, tgt_vocab_size, (64, max_seq_length))  # (batch_size, seq_length)

# 初始化一个transformer网络
transformer = Transformer(src_vocab_size, tgt_vocab_size, d_model, num_heads, num_layers, d_ff, max_seq_length, dropout)

# training the data
criterion = nn.CrossEntropyLoss(ignore_index=0)
optimizer = optim.Adam(transformer.parameters(), lr=0.0001, betas=(0.9, 0.98), eps=1e-9)

transformer.train()

for epoch in range(100):
    optimizer.zero_grad()
    output = transformer(src_data, tgt_data[:, :-1])  #  Passes the source data and the target data (excluding the last token in each sequence) through the transformer. This is common in sequence-to-sequence tasks where the target is shifted by one token.
    loss = criterion(output.contiguous().view(-1, tgt_vocab_size), tgt_data[:, 1:].contiguous().view(-1))  #  Computes the loss between the model's predictions and the target data (excluding the first token in each sequence). The loss is calculated by reshaping the data into one-dimensional tensors and using the cross-entropy loss function.
    loss.backward()
    optimizer.step()
    print(f"Epoch: {epoch+1}, Loss: {loss.item()}")
    
# eval the model：
transformer.eval()

# Generate random sample validation data
val_src_data = torch.randint(1, src_vocab_size, (64, max_seq_length))  # (batch_size, seq_length)
val_tgt_data = torch.randint(1, tgt_vocab_size, (64, max_seq_length))  # (batch_size, seq_length)

with torch.no_grad():

    val_output = transformer(val_src_data, val_tgt_data[:, :-1])
    val_loss = criterion(val_output.contiguous().view(-1, tgt_vocab_size), val_tgt_data[:, 1:].contiguous().view(-1))
    print(f"Validation Loss: {val_loss.item()}")
```

更为具体的任务放在后面再进行描述。

------



### 7.李沐精读——Transformer

[Transformer论文逐段精读【论文精读】_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1pu411o7BE/?spm_id_from=333.337.search-card.all.click)

#### （1）LayerNorm相关

这里有两个问题：

- LayerNorm和BatchNorm的区别是什么？
- 为什么Transformer使用的是LayerNorm而不是BatchNorm，LayerNorm有什么优势？

对应视频的25分钟开始到32分钟的部分。

以下贴一个关于LayerNorm和BatchNorm的区别的链接：[Build Better Deep Learning Models with Batch and Layer Normalization | Pinecone](https://www.pinecone.io/learn/batch-layer-normalization/)

> 知乎上的某回答：
>
> BatchNorm是对一个batch-size样本内的每个特征做归一化，LayerNorm是对每个样本的所有特征做归一化。
>
> 形象点来说，假设有一个二维矩阵。行为batch-size，列为样本特征。那么BN就是竖着归一化，LN就是横着归一化。
>
> 它们的出发点都是让该层参数稳定下来，避免梯度消失或者梯度爆炸，方便后续的学习。



## 关于Self-attention其他可参考的资料

[Transformer常见问题与回答总结 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/496012402?utm_medium=social&utm_oi=629375409599549440)

[GitHub 7.5k star量，各种视觉Transformer的PyTorch实现合集整理好了 | 机器之心 (jiqizhixin.com)](https://www.jiqizhixin.com/articles/2021-12-31-8)

[UKPLab/sentence-transformers: Multilingual Sentence & Image Embeddings with BERT (github.com)](https://github.com/UKPLab/sentence-transformers)

https://ketanhdoshi.github.io/Transformers-Overview/



## 关于Transformer的一些问题（比如面试问）

### 1.来自作业的问题

（1）Why can transformer train in parallel but not reference in parallel?

> 首先，对于encoder来说是支持并行化训练的，这是因为transformer解决了传统RNN训练时的的时序性问题，使用self-attention机制一次性关注整个输入，因此支持并行化训练。而对于Decoder而言：
>
> - 在train的过程当中，会把整个句子喂给decoder，这个过程叫做teacher forcing，在每一轮预测的时候不使用decoder上一轮的输出，而是使用正确的输入，因此可以直接通过带有mask的self-attention机制来实现，自然就支持并行化训练了；
> - 在test的过程中，由于并没有所谓的ground truth，decoder在t时刻的输入只能依赖于t-1时刻的输出，因此并不支持并行化。



（2）What is the relationship between the convolution operations and the attention operations?

这个可以参考两篇文献：[[1911.03584\] On the Relationship between Self-Attention and Convolutional Layers (arxiv.org)](https://arxiv.org/abs/1911.03584)

[2111.14556.pdf (arxiv.org)](https://arxiv.org/pdf/2111.14556.pdf)

> 可以从以下几点来总结两者间的关系：
>
> - （1）在**局部信息的捕获上**，卷积层和self-attention都具有捕获局部信息的能力。卷积核在输入的局部区域上滑动，而self-attention可以在整个序列上关注不同位置。**卷积**算法是根据卷积核内内容的加权和，而卷积核是全局共享的，为特征图添加了重要的归纳偏置，而**自注意力**计算的是全局信息的加权平均，通过计算相关像素对之间的相似函数动态获得注意力权重，这种灵活性使自注意力模块可以自适应地关注不同区域，捕获更多的特征信息。与卷积相比，自注意力让模型在更大的内容空间中聚焦于重要区域。
> - （2）两者都能够学习到输入序列的特征表示，进而帮助模型理解序列中的关系。
> - （3）根据[[1911.03584\] On the Relationship between Self-Attention and Convolutional Layers (arxiv.org)](https://arxiv.org/abs/1911.03584)这篇文献表明，注意力层能够执行卷积操作，并且证明了具有足够多注意头的多头自注意层至少与任何卷积层一样具有表达能力。
> - （4）Self-attention 的计算复杂度通常较高，尤其是对于较长的序列。相比之下，卷积层的计算复杂度相对较低，计算速度更快。



（3）Why is a mask needed after tokenization? Attention mechanisms also use masks, what are their functions respectively?

> （1）Masking, as name suggests, is a process of replacing real data with null or constant values. When we tokenize a sequence during natural language processing（NLP） tasks,  mask operation serves the purpose of indicating which parts of the sequence are actual content and which parts are padding. Padding is added to ensure that all sequences in a batch have the same length, so that the neural network could deal with them easier;
>
> （2）As for masks in attention mechanisms, it uses masks to hide future information in the sequence, which has not been predicted yet. This part of sequences represents the part the model is trying to predict, and a mask is essential to block the decoder from accessing upcoming tokens in the sequence.  In other words, using a mask ensures that the model focuses solely on the context available from the tokens that have already been processed, preventing it from merging information from the future tokens in the sequence.



（4）Why does Transformer introduce positional coding? Why do RNN, GRU, LSTM not need to introduce positional coding?

> 对于NLP相关的任务而言，对于语句来说，词语的顺序和每个单词所在的位置对句子意思的表达都是至关重要的。传统的RNN、GRU、LSTM网络在处理句子时，以**序列的模式逐个处理句子中的词语**，这使得词语的顺序信息在处理过程中被天然的保存下来了，并不需要额外的处理。
>
> 而对于Transformer来说，由于句子中的词语都是同时进入网络进行并行化处理的，核心的self-attention机制本身并不关心时序信息，所以顺序信息在输入网络时就已丢失。因此，Transformer是需要额外的处理来告知每个词语的相对位置的。而其中的一个解决方案，就是《Attention is All You Need》论文中提到的Positional Encoding，将能表示位置信息的编码添加到输入中，从而让网络知道每个词的位置和顺序，进而手动为网络提供时序相关的信息。



（5）After you finish your assignment, please describe the whole process of machine translation based transformer, in other word, how is an English sentence translated into Chinese ? The more detailed, the better. 

> The whole process of machine translation based on transformer may like below:
>
> #### 1.tokenization
>
> The input sentence (in this situation, input sentences are English sentences) is first broken down into smaller units called tokens. These tokens can be words, subwords, or characters. In this project, we use SentencePiece, which the tokens are subwords.
>
> A common padding operation  is typically performed to keep the sequence lengths consistent, facilitating subsequent computations.
>
> 
>
> #### 2. **Embedding:**
>
> Then, each token is then represented as a high-dimensional vector through an embedding layer. This layer essentially converts each token into a numerical vector, and these vectors  have the ability to capture the semantic meaning and relationships between words.
>
> 
>
> #### 3. **Positional Encoding:**
>
> Since the Transformer model pay attention to the global information instead of directly understanding the order of words, it is neccessary to  provide location information explicitly. In this step, positional encoding is added to the embedded tokens to convey their positions in the sequence.
>
> 
>
> #### 4.Training
>
> The entire model is trained using parallel data(we use masks to provide parallelization), where pairs of input and target language sentences are fed to the encoder and decoder parts of the Transformer model. The stack of Decoders processes this along with the Encoder stack’s encoded representation to produce an encoded representation of the target sequence. Then, the output layer converts it into word probabilities and the final output sequence. The Transformer’s Loss function compares this output sequence with the target sequence from the training data. This loss is used to generate gradients to train the Transformer during back-propagation. During training, a method called teacher forcing is often used.
>
> 
>
> #### 5.Inferencing
>
> During the process of inference, we have only the input sequence and don't have the target sequence to pass to the Decoder. So the goal of decoder is to predict the target sequence from the input sequence in a sequential manner. At each timestep, we re-feed the entire output sequence to the encoder.The final layer of the decoder generates the output sequence in the target language (In this situation, Chinese). This output is again a sequence of vectors, which represents the probability distribution over the vocabulary.
>
> There are some common loss functions and evaluation metrics during the inference process. As for loss functions, Cross Entropy Loss is commonly used for sequence generation tasks. We often use BLEU score or other evaluation metrics to test the ability of our translation neural network.
>
> 
>
> #### 6.Deploy the model
>
> We save the trained Transformer model and its associated parameters and then deploy the model to target platforms.

## 三、ViT

相关链接：[[2010.11929\] An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale (arxiv.org)](https://arxiv.org/abs/2010.11929)





## Future work：

- BERT
- 训练一个transformer在某个数据集上，这个再说（深度学习的作业三就是做这个任务）
- VIT论文阅读，并看一下开源代码[lucidrains/vit-pytorch: Implementation of Vision Transformer, a simple way to achieve SOTA in vision classification with only a single transformer encoder, in Pytorch (github.com)](https://github.com/lucidrains/vit-pytorch)



## 实际跑一个Transformer

以下以机器翻译任务为例，实现中英文翻译。相关的作业已经上传到Github上，可以随时进行复习。以下整理一些比较重要的点。

### 1.SentencePiece包

相关参考：[【LLM】大语言模型学习笔记-3 一文详解sentencepiece（关于大语言模型的词表扩充） - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/649543347)

关于这个包的参数介绍：[sentencepiece/doc/options.md at master · google/sentencepiece (github.com)](https://github.com/google/sentencepiece/blob/master/doc/options.md)

在这个项目中，我们用如下参数：

```python
en_input = english_data_path
en_vocab_size = 32000
en_model_name = tokenizer_dir / Path('eng')
en_model_type = 'bpe'
en_character_coverage = 1

tokenizer_dir  = Path('tokenizer')
eng_model_path = tokenizer_dir / Path('eng.model')
eng_vocab_path = tokenizer_dir /Path('eng.vocab')

if eng_model_path.exists() and eng_vocab_path.exists():
    logging.info(f"{eng_model_path } and {eng_vocab_path} have exist! continue run the code")
else:
    train(en_input, en_vocab_size, en_model_name, en_model_type, en_character_coverage)

ch_input = chinese_data_path
ch_vocab_size = 32000
ch_model_name = tokenizer_dir / Path('chn')
ch_model_type = 'bpe'
ch_character_coverage = 0.9995

chn_model_path = tokenizer_dir / Path('chn.model')
chn_vocab_path = tokenizer_dir / Path('chn.vocab')
if chn_model_path.exists() and chn_vocab_path.exists():
    logging.info(f"{chn_model_path } and {chn_vocab_path} have exist! continue run the code")
else:
    train(ch_input, ch_vocab_size, ch_model_name, ch_model_type, ch_character_coverage)
```

train函数如下：

```python
import sentencepiece as spm
def train(input_file, vocab_size, model_name, model_type, character_coverage):
    """
    search on https://github.com/google/sentencepiece/blob/master/doc/options.md to learn more about the parameters
    :param input_file: one-sentence-per-line raw corpus file. No need to run tokenizer, normalizer or preprocessor.
    By default, SentencePiece normalizes the input with Unicode NFKC.
    You can pass a comma-separated list of files.
    :param vocab_size: vocabulary size, e.g., 8000, 16000, or 32000
    :param model_name: output model name prefix. <model_name>.model and <model_name>.vocab are generated.
    :param model_type: model type. Choose from unigram (default), bpe, char, or word.
                       The input sentence must be pretokenized when using word type.
    :param character_coverage: amount of characters covered by the model, good defaults are: 0.9995 for languages with rich character set like Japanse or Chinese and 1.0 for other languages with small character set.
    """
    input_argument = '--input=%s --model_prefix=%s --vocab_size=%s --model_type=%s --character_coverage=%s ' \
                     '--pad_id=0 --unk_id=1 --bos_id=2 --eos_id=3 '
    cmd = input_argument % (input_file, model_name, vocab_size, model_type, character_coverage)
    #cmd = 'spm_train '+ cmd
    spm.SentencePieceTrainer.Train(cmd)
```

对SentencePiece包的分词结果进行测试，如下：
```python
sp = spm.SentencePieceProcessor()
text = "美国总统特朗普今日抵达夏威夷。"

sp.Load('./tokenizer/chn.model')
print(sp.EncodeAsPieces(text))

# encode the text
s =sp.EncodeAsIds(text)
# embeding vector
print(s)
# decode the embedding vector
print(sp.decode_ids(s))

# let's do little change to the embeding functio vector
for i in range(0,len(s),2):
    print(f'{i}: {s[i]} --> {s[i] + 1}')
    s[i] = s[i] + 1
# look new vector
print(s)
# decode the new embedding vector
print(sp.decode_ids(s))
```

输出结果为：

> ```
> ['▁美国总统', '特朗普', '今日', '抵达', '夏威夷', '。']
> [12908, 277, 7420, 7319, 18385, 28724]
> 美国总统特朗普今日抵达夏威夷。
> 0: 12908 --> 12909
> 2: 7420 --> 7421
> 4: 18385 --> 18386
> [12909, 277, 7421, 7319, 18386, 28724]
> ```

**对于英文也是类似的，在这里就不再展示了。**

------



### 2.关于类的collate_fn函数

[pytorch之深入理解collate_fn-CSDN博客](https://blog.csdn.net/qq_43391414/article/details/120462055)

[pytorch中collate_fn函数的使用&如何向collate_fn函数传参_collate_fn=collater-CSDN博客](https://blog.csdn.net/dong_liuqi/article/details/114521240)

在这个翻译任务当中，collate_fn函数可能如下：

```python
def collate_fn(self, batch):
    src_text = [x[0] for x in batch]
    tgt_text = [x[1] for x in batch]

    src_tokens = [[self.BOS] + self.sp_eng.EncodeAsIds(sent) + [self.EOS] for sent in src_text]
    tgt_tokens = [[self.BOS] + self.sp_chn.EncodeAsIds(sent) + [self.EOS] for sent in tgt_text]

    batch_input = pad_sequence([torch.LongTensor(np.array(l_)) for l_ in src_tokens],
                               batch_first=True, padding_value=self.PAD)
    batch_target = pad_sequence([torch.LongTensor(np.array(l_)) for l_ in tgt_tokens],
                                batch_first=True, padding_value=self.PAD)

    return Batch(src_text, tgt_text, batch_input, batch_target, self.PAD)
```



------

### 3.关于Transformer训练时候的mask策略

在上一部分的最后，有这样一句：`return Batch(src_text, tgt_text, batch_input, batch_target, self.PAD)`，其中src_text和tgt_text是源文本和目标文本，而bactch_input和batch_target是做了tokenize和padding之后的tensor。Batch类的定义如下：
```python
class Batch:
    """Object for holding a batch of data with mask during training."""
    def __init__(self, src_text, trg_text, src, trg=None, pad=0):
        self.src_text = src_text
        self.trg_text = trg_text
        src = src.to(DEVICE)
        self.src = src
        print(self.src.shape)
        # Determine the non-empty part of the current input sentence as a bool sequence.
        # And add one dimension in front of seq length to form a matrix of dimension 1×seq length
        self.src_mask = (src != pad).unsqueeze(-2) # 原来句子的位置会是True，被padding的部分会是False
        # If the output target is not null, then you need to mask the target clause to be used by the decoder.
        if trg is not None:
            trg = trg.to(DEVICE)
            # Target input part to be used by decoder，对于喂给decoder的训练数据，并不包含最后一个向量，因为decoder需要预测后面一个是什么
            self.trg = trg[:, :-1]
            # The decoder training should predict the output target result
            self.trg_y = trg[:, 1:]  # decoder 在training阶段输出的内容应该是从第一个词往后的，同样因为decoder会预测下一个词
            # Attention mask the target input portion
            self.trg_mask = self.make_std_mask(self.trg, pad)
            # Counts the actual number of words in the target results that should be outputted
            self.ntokens = (self.trg_y != pad).data.sum()

    # Mask
    @staticmethod
    def make_std_mask(tgt, pad):
        """Create a mask to hide padding and future words."""
        tgt_mask = (tgt != pad).unsqueeze(-2)  # 原来句子的位置会是True，被padding的部分会是False
        # 关于Variable的用法可以参考博客：https://blog.csdn.net/weixin_42782150/article/details/106854349
        tgt_mask = tgt_mask & Variable(subsequent_mask(tgt.size(-1)).type_as(tgt_mask.data)) # 之前对句子排序可能就是为了这里可以做&运算的时候正好subsequent_mask和tgt_mask基本都是左下角是True，右上角是False的东西
        return tgt_mask
```

相关的注释已经写在代码里了。

------



### 4.一些NLP领域的概念

#### （1）Label Smoothing

相关概念可以参考：[Label Smoothing Explained | Papers With Code](https://paperswithcode.com/method/label-smoothing)



#### （2）Beam Search

[如何通俗的理解beam search？ - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/82829880)

[Transformer中的beam search - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/109183727)



#### （3）BLEU

[BLEU详解 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/223048748)





# Learn From Scratch

![image-20241005153106798](Transformer%20%E7%9B%B8%E5%85%B3.assets/image-20241005153106798.png)

## 1.Input-Embedding

```python
class InputEmbeddings(nn.Module):
    def __init__(self, d_model: int, vocab_size: int):
        super().__init__()
        self.d_model = d_model
        self.vocab_size = vocab_size
        self.embedding = nn.Embedding(vocab_size, d_model)
    def forward(self, x):
        return self.embedding(x) * math.sqrt(self.d_model)
```



## 2.Positional Encoding

