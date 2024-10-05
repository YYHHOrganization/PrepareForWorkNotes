import torch
import torch.nn as nn
import math

class InputEmbeddings(nn.Module):
    def __init__(self, d_model: int, vocab_size: int):
        super().__init__()
        self.d_model = d_model
        self.vocab_size = vocab_size
        self.embedding = nn.Embedding(vocab_size, d_model)
    def forward(self, x):
        return self.embedding(x) * math.sqrt(self.d_model)
    
class PositionalEncoding(nn.Module):
    def __init__(self, d_model:int, seq_len:int, dropout: float)->None:
        super().__init__()
        self.d_model = d_model
        self.seq_len = seq_len  # seq_len是一个超参数，表示输入序列的最大长度
        self.dropout = nn.Dropout(dropout)

        # create a matrix of shape (seq_len, d_model)
        pe = torch.zeros(seq_len, d_model)
        # create a vector of shape(seq_len, 1)
        position = torch.arange(0, seq_len, dtype=torch.float).unsqueeze(1) # shape (seq_len, 1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        # apply sin to even indices in the array; 2i, similar to cos
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        pe = pe.unsqueeze(0)  # shape (1, seq_len, d_model)  # add a batch dimension
        self.register_buffer('pe', pe)  # register the buffer to save it in the model's state_dict, but not to be updated by the optimizer
    
    def forward(self, x):
        x = x + (self.pe[:, :x.size(1), :]).requires_grad_(False) # add positional encoding to the input
        return self.dropout(x)

class LayerNormalization(nn.Module):
    # Layer Normalization operates by calculating the mean and variance of the inputs for each sample.
    def __init__(self, eps: float = 1e-6)->None:
        super().__init__()
        self.eps = eps
        self.alpha = nn.Parameter(torch.ones(1)) # Multiplied
        self.bias = nn.Parameter(torch.zeros(1)) # Added
    def forward(self, x):
        mean = x.mean(dim = -1, keepdim = True)  # mean： (Batch, Seq_len, d_model) -> (Batch, Seq_len, 1)
        std = x.std(dim = -1, keepdim = True)
        return self.alpha * (x - mean) / (std + self.eps) + self.bias
    
class FeedForwardBlock(nn.Module):
    def __init__(self, d_model: int, d_ff: int, dropout: float)->None:
        super().__init__()
        self.d_model = d_model
        self.d_ff = d_ff
        self.dropout = nn.Dropout(dropout)
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
    def forward(self, x):
        # (Batch, Seq_len, d_model) -> (Batch, Seq_len, d_ff) -> (Batch, Seq_len, d_model)
        x = self.linear2(self.dropout(torch.relu(self.linear1(x))))
        return x
    
class MultiHeadAttentionBlock(nn.Module):
    def __init__(self, d_model:int, h:int, dropout:float)->None:
        super().__init__()
        self.d_model = d_model
        self.h = h
        assert d_model % h == 0, "d_model must be divisible by h"
        self.d_k = d_model // h
        self.dropout = nn.Dropout(dropout)
        self.w_q = nn.Linear(d_model, d_model)
        self.w_k = nn.Linear(d_model, d_model)
        self.w_v = nn.Linear(d_model, d_model)
        self.w_o = nn.Linear(d_model, d_model)
    
    @staticmethod  # static method is used to define a method that does not operate on the instance of the class
    def attention(query, key, value, mask, dropout: nn.Dropout):
        d_k = query.shape[-1]
        attention_scores = (query @ key.transpose(-2, -1)) / math.sqrt(d_k)  # (Batch, h, Seq_len, d_k) @ (Batch, h, d_k, Seq_len) -> (Batch, h, Seq_len, Seq_len)
        if mask is not None:
            attention_scores = attention_scores.masked_fill_(mask == 0, -1e9)  # 这样在softmax之后就会变成0
        # mask 的作用是遮挡住那些不应该被关注的位置，比如在decoder中，当前位置之后的位置是不应该被关注的
        attention_scores = attention_scores.softmax(dim = -1)  # (Batch, h, Seq_len, Seq_len)
        if dropout is not None:
            attention_scores = dropout(attention_scores)
        return (attention_scores @ value), attention_scores  # attention_scores 可以用于可视化注意力权重

    
    def forward(self, q, k, v, mask):
        query = self.w_q(q)  # (Batch, Seq_len, d_model) -> (Batch, Seq_len, d_model)
        key = self.w_k(k) # same as query
        value = self.w_v(v) # same as query

        query = query.view(query.shape[0],query.shape[1], self.h, self.d_k).transpose(1, 2) # (Batch, Seq_len, d_model) -> (Batch, h, Seq_len, d_k)
        key = key.view(key.shape[0], key.shape[1], self.h, self.d_k).transpose(1, 2)
        value = value.view(value.shape[0], value.shape[1], self.h, self.d_k).transpose(1, 2)

        x, self.attention_scores = MultiHeadAttentionBlock.attention(query, key, value, mask, self.dropout)
        # x: (Batch, h, Seq_len, d_k) -> (Batch, Seq_len, h, d_k) -> (Batch, Seq_len, d_model)
        x = x.transpose(1, 2).contiguous().view(x.shape[0], -1, self.h * self.d_k) # contiguous() is used to make the tensor contiguous in memory
        return self.w_o(x)  # (Batch, Seq_len, d_model)

class ResidualConnection(nn.Module):
    def __init__(self, dropout: float)->None:
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        self.norm = LayerNormalization()
    def forward(self, x, sublayer):
        return x + self.dropout(sublayer(self.norm(x))) # 注：原论文中是先做sublayer再norm，这里是先norm再sublayer，很多实现都是这样的
    
class EncoderBlock(nn.Module):
    def __init__(self, self_attention_block: MultiHeadAttentionBlock, feed_forward_block: FeedForwardBlock, dropout: float)->None:
        super().__init__()
        self.self_attention_block = self_attention_block
        self.feed_forward_block = feed_forward_block
        self.residual_connection = nn.ModuleList([ResidualConnection(dropout) for _ in range(2)])

    def forward(self, x, src_mask): # src_mask is used to mask out the padding tokens
        x = self.residual_connection[0](x, lambda x: self.self_attention_block(x, x, x, src_mask))
        return self.residual_connection[1](x, lambda x: self.feed_forward_block(x))  # 这里只有一个形参x，所以lambda x: self.feed_forward_block(x)可以简写为self.feed_forward_block
    
class Encoder(nn.Module):
    def __init__(self, layers:nn.ModuleList)->None:
        super().__init__()
        self.layers = layers
        self.norm = LayerNormalization()
    def forward(self, x, src_mask):
        for layer in self.layers:
            x = layer(x, src_mask)
        return self.norm(x)
    
class DecoderBlock(nn.Module):
    def __init__(self, self_attention_block: MultiHeadAttentionBlock, cross_attention_block: MultiHeadAttentionBlock, feed_forward_block: FeedForwardBlock, dropout: float)->None:
        super().__init__()
        self.self_attention_block = self_attention_block
        self.cross_attention_block = cross_attention_block
        self.feed_forward_block = feed_forward_block
        self.residual_connection = nn.ModuleList([ResidualConnection(dropout) for _ in range(3)])
    
    def forward(self, x, encoder_output, src_mask, tgt_mask): # translation task uses both src_mask and tgt_mask
        x = self.residual_connection[0](x, lambda x: self.self_attention_block(x, x, x, tgt_mask)) # 这里用的是tgt_mask
        x = self.residual_connection[1](x, lambda x: self.cross_attention_block(x, encoder_output, encoder_output, src_mask)) # 这里用的是src_mask，注意mask的使用
        return self.residual_connection[2](x, lambda x: self.feed_forward_block(x))

class Decoder(nn.Module):
    def __init__(self, layers:nn.ModuleList)->None:
        super().__init__()
        self.layers = layers
        self.norm = LayerNormalization()
    def forward(self, x, encoder_output, src_mask, tgt_mask):
        for layer in self.layers:
            x = layer(x, encoder_output, src_mask, tgt_mask)
        return self.norm(x)
        
class ProjectionLayer(nn.Module): # 用于将decoder的输出映射到vocab_size维度，这样结果才是词汇
    def __init__(self, d_model:int, vocab_size:int)->None:
        super().__init__()
        self.d_model = d_model
        self.vocab_size = vocab_size
        self.linear = nn.Linear(d_model, vocab_size)
    def forward(self, x):
        # (Batch, Seq_len, d_model) -> (Batch, Seq_len, vocab_size)
        return torch.log_softmax(self.linear(x), dim = -1) # log_softmax is used to calculate the log of softmax values, dim=-1 means the last dimension
    
class Transformer(nn.Module):
    def __init__(self, encoder:Encoder, decoder:Decoder, src_embed:InputEmbeddings, tgt_embed:InputEmbeddings, src_pos:PositionalEncoding, tgt_pos:PositionalEncoding, projection_layer:ProjectionLayer)->None:
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.src_embed = src_embed
        self.tgt_embed = tgt_embed
        self.src_pos = src_pos
        self.tgt_pos = tgt_pos
        self.projection_layer = projection_layer
    
    def encode(self, src, src_mask):
        src = self.src_embed(src)
        src = self.src_pos(src)
        return self.encoder(src, src_mask)
    def decode(self, encoder_output, src_mask, tgt, tgt_mask):
        tgt = self.tgt_embed(tgt)
        tgt = self.tgt_pos(tgt)
        return self.decoder(tgt, encoder_output, src_mask, tgt_mask)
    def project(self, x):
        return self.projection_layer(x)

def build_transformer(src_vocab_size : int, tgt_vocab_size : int, src_seq_len : int, tgt_seq_len : int, d_model : int = 512, N: int = 6, h:int=8, dropout:float=0.1, d_ff:int=2048)->Transformer:
    src_embed = InputEmbeddings(d_model, src_vocab_size)
    tgt_embed = InputEmbeddings(d_model, tgt_vocab_size)
    src_pos = PositionalEncoding(d_model, src_seq_len, dropout)
    tgt_pos = PositionalEncoding(d_model, tgt_seq_len, dropout)

    encoder_blocks = []
    for _ in range(N):
        encoder_blocks.append(EncoderBlock(MultiHeadAttentionBlock(d_model, h, dropout), FeedForwardBlock(d_model, d_ff, dropout), dropout))
    decoder_blocks = []
    for _ in range(N):
        decoder_blocks.append(DecoderBlock(MultiHeadAttentionBlock(d_model, h, dropout), MultiHeadAttentionBlock(d_model, h, dropout), FeedForwardBlock(d_model, d_ff, dropout), dropout))
    
    encoder = Encoder(nn.ModuleList(encoder_blocks))
    decoder = Decoder(nn.ModuleList(decoder_blocks))
    projection_layer = ProjectionLayer(d_model, tgt_vocab_size)
    transformer  = Transformer(encoder, decoder, src_embed, tgt_embed, src_pos, tgt_pos, projection_layer)

    # initialize the weights
    for p in transformer.parameters():
        if p.dim() > 1:
            nn.init.xavier_uniform_(p)
    return transformer
