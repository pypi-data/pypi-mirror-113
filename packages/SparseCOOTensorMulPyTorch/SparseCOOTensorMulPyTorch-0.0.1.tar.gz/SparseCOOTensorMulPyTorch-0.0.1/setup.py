from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name = 'SparseCOOTensorMulPyTorch',
    version = '0.0.1',
    description = 'Pytorch based sparse coo tensor multiplication (returns same elements with torch.matmul function but returns torch.tensor)',
    Long_description = open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url = 'https://github.com/dqj5182/Sparse_COO_Tensor_Multiplication_Pytorch',
    author = 'Daniel Jung',
    author_email = 'dqj5182@psu.edu',
    license = 'MIT',
    classifiers = classifiers,
    keywords = 'graph, matrix-multiplication, sparse-matrix, sparse-tensors, gnn',
    packages = find_packages(),
    setup_requires = ['torch', 'numpy'],
    install_requires = ['torch', 'numpy']
)