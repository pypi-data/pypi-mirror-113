import torch
import numpy as np

def sparse_coo_mul(tensor1, tensor2):
  # **tensor1 and tensor2 should be data type torch.sparse_coo_tensor
  tensor1_indices = tensor1.coalesce().indices() # Get indices of sparse coo tensor 1
  tensor2_indices = tensor2.coalesce().indices() # Get indices of sparse coo tensor 2
  tensor1_values = tensor1.coalesce().values() # Get values of sparse coo tensor 1
  tensor2_values = tensor2.coalesce().values() # Get values of sparse coo tensor 2

  def swap_two_rows(tensor):
    # This function swaps first row and second row of (usually) index tensor (first parameter for torch.sparse_coo_tensor())
    index = [1, 0]
    tensor[index,] = tensor.clone() # Swaps first and second row
    return tensor

  test_1 = tensor1_indices.t() # Transpose index tensor, as this transposed tensor has non-zero sparse tensor coordinates in each rows
  test_2 = swap_two_rows(tensor2_indices).t() # Transpose for same reason. Swapping first and second row due to "the property of mat mul"
  # "the property of mat mul"
  # If you think carefully on matrix multiplication, you can see that we are multiplying elements in rows of first matrix and cols of second matrix where
  # row index of first matrix = col index of second matrix. For such row and col, we multiply each elements of first and second matrices where col index of
  # first index = row index of second index.

  # The reason for swapping rows:
  # This is more of convenience than necessity. Let columns of first matrix as col1, columns of second matrix as col2, rows of first matrix as row1,
  # rows of second matrix as row2. As by "the property of mat mul" said above, we need to first meet row1 = col2. Then, we need to sum the multiplication
  # of elements that meet col1 = row2. This is just how matrix multiplication is. Nothing too complicated.

  mul_i_j = [] # A list that will store multiplication results of each one element from first matrix and second matrix
  # This will be later summed up just like how matrix multiplication works

  final = {} # A dict that will store output matrix coordinate and multiplication result.

  final_list = [] # A list that will store final outputted indecies and values for returning sparse coo tensor. 
  # This will be used to make returning sparse coo tensor (new_sparse_coo_tensor)

  for i, val_i in enumerate(test_1):
    for j, val_j in enumerate(test_2):

      if torch.equal(val_i[1], val_j[1]):
        mul_i_j.append([val_i[0].item(), val_j[0].item(), (tensor1_values[i]*tensor2_values[j]).item()]) # val_i[0]: row 1, val_i[1]: col 1, val_j[0]: col 2, val_j[1]: row 2

  # Try print(mul_i_j) to see how this works
  for ele1, ele2, ele3 in mul_i_j: # For each multiplications
    if (ele1, ele2) not in final: # If there were not yet multiplication result regarding the output coordinate
      final[(ele1, ele2)] = ele3 # Store the multiplication result for the regarding output coordinate
    else: # If there were already multiplication result regarding the output coordinate
      final[(ele1, ele2)] = final[(ele1, ele2)] + ele3 # Add the multiplication result for the existing regarding output coordinate

  for key, value in final.items(): # For keys and values in dictionary "final"
    temp = [key[0], key[1] ,value] # Make this dictionary as list of lists
    final_list.append(temp)

  final_list = np.array(final_list).T # Transpose back to make index tensor and value tensor used for parameters in torch.sparse_coo_tensor()

  new_index = final_list[0:2,] # Will be put into torch.sparse_coo_tensor() as first parameter 
  new_value = final_list[2,] # Will be put into torch.sparse_coo_tensor() as second parameter

  new_sparse_coo_tensor = torch.sparse_coo_tensor(new_index, new_value) # Finally made sparse_coo_tensor to be returned
  
  return new_sparse_coo_tensor