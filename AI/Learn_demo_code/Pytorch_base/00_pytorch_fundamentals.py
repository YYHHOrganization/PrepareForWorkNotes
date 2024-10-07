import torch
def tensor_01():
    scalar = torch.tensor(7)
    print(scalar)
    print(scalar.ndim)  # 0
    print(scalar.item()) # 7, get the value of the scalar, only works for one element tensor

    vector = torch.tensor([1, 2, 3])
    print(vector)
    print(vector.ndim) # 1
    print(vector.shape)  # torch.Size([3]), shape tells how the elements inside them are arranged.

    MATRIX = torch.tensor([[7, 8],
                           [9, 10]])
    print(MATRIX)
    print(MATRIX.ndim)  # 2
    print(MATRIX.shape) # torch.Size([2,2])

    TENSOR = torch.tensor([[[1,2,3],
                            [3,6,9],
                            [2,4,5]]])
    print(TENSOR.ndim)  # 3
    print(TENSOR.shape) # torch.Size([1,3,3]) dimensions go outer to inner


def rand_tensor_02():
    random_tensor = torch.rand(size=(3, 4))
    print(random_tensor)
    print(random_tensor.dtype) # torch.float32

def other_tensor_03():
    zero_to_ten = torch.arange(start=0, end=10, step=1)
    print(zero_to_ten)  # tensor([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    ten_zeros = torch.zeros_like(input=zero_to_ten)  # tensor([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    print(ten_zeros)

def tensor_datatypes_04():
    float_32_tensor = torch.tensor([4.0, 6.0, 8.0], 
                                   dtype=None, # defaults, which is torch.float32 or other
                                   device=None,
                                   requires_grad=False)
    print(float_32_tensor.device) # cpu
    float_16_tensor = torch.tensor([3.0, 5.0, 6.0], dtype=torch.float16)
    print(float_16_tensor)

def basic_operations_05():
    tensor = torch.tensor([1,2,3])
    # multiply
    print(tensor * tensor)  # tensor([1, 4, 9])
    # most common in deep learning, matrix
    print(torch.matmul(tensor, tensor)) # tensor(14)
    print(tensor @ tensor) # not recommended
    # other operations, not check

    # torch.transpose
    # tensor.T
    # torch.mm (short for torch.matmul)
    # min, max, mean, sum
    # find the index of tensor which has the max value
    tensor =torch.arange(10, 100, 10)
    print(tensor.argmax())  # tensor(8)

    tensor_float32 = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float32)
    tensor_int8 = tensor_float32.type(torch.int8)
    print(tensor_int8)  #tensor([1, 2, 3], dtype=torch.int8)

def popular_resize_06():
    # reshape, view, stack, squeeze, unsqueeze, permute, 
    x = torch.arange(1., 8.)
    print(x.shape) # torch.Size([7])
    x_reshaped = x.reshape(1, 7)
    print(x_reshaped, x_reshaped.shape) # tensor([[1., 2., 3., 4., 5., 6., 7.]]),torch.Size([1, 7])

    z = x.view(1, 7) # change view: remember that changing the view of a tensor will change the original tensor
    print(z, z.shape) # tensor([[1., 2., 3., 4., 5., 6., 7.]]), torch.Size([1, 7])
    z[:, 0] = 5
    print(x, x.shape) # tensor([5., 2., 3., 4., 5., 6., 7.]), torch.Size([7])

    # stack
    x_stack = torch.stack([x, x, x, x], dim=0) # if dim=1, torch.Size([7, 4])
    print(x_stack, x_stack.shape) # torch.Size([4, 7]

    # squeeze
    x_squeeze = x_reshaped.squeeze()
    print(x_squeeze, x_squeeze.shape) # tensor([1., 2., 3., 4., 5., 6., 7.]), torch.Size([7])
    # unsqueeze
    x_unsqueeze = x_squeeze.unsqueeze(dim=0)
    print(x_unsqueeze, x_unsqueeze.shape) # tensor([[1., 2., 3., 4., 5., 6., 7.]]), torch.Size([1, 7])

    # permute: rearrange the dimensions of a tensor
    x_original = torch.rand(size=(224,224,3))
    x_permute = x_original.permute(2, 0, 1)
    print(x_permute.shape) # torch.Size([3, 224, 224]), permuting returns a view of the original tensor, so if you change the permuted tensor, the original tensor will also change.

    # tensor的index暂时先省略，后面写多了就懂了

def tensor_with_numpy_07():
    # note:这里的tensor和numpy array共享内存，所以一个改变了，另一个也会改变
    # 想要不共享内存，可以用别的方式，等后面需要的话再说吧，或者再查资料
    # tensor to numpy
    tensor = torch.tensor([1, 2, 3])
    numpy_array = tensor.numpy()
    print("=====tensor to numpy=====")
    print(numpy_array) # [1, 2, 3]
    tensor[0] = 100
    print(tensor) # tensor([100, 2, 3])
    print(numpy_array) # [1, 2, 3]

    print("=====numpy to tensor=====")
    # numpy to tensor
    import numpy as np
    numpy_array = np.array([1, 2, 3])
    tensor = torch.from_numpy(numpy_array)
    print(tensor) # tensor([1, 2, 3])
    numpy_array[0] = 100
    print(tensor) # tensor([100, 2, 3])
    print(numpy_array) # [100, 2, 3]

    
   


# tensor_01()
# rand_tensor_02()
# other_tensor_03()
# tensor_datatypes_04()
# basic_operations_05()
# popular_resize_06()
tensor_with_numpy_07()
