"""
findiff is a Python package for finite difference numerical derivatives
and partial differential equations in any number of dimensions.

Features:

- Differentiate arrays of any number of dimensions along any axis with any desired accuracy order
- Accurate treatment of grid boundary
- Includes standard operators from vector calculus like gradient, divergence and curl
- Can handle uniform and non-uniform grids
- Can handle arbitrary linear combinations of derivatives with constant and variable coefficients
- Fully vectorized for speed
- Calculate raw finite difference coefficients for any order and accuracy for uniform and non-uniform grids
- New in version 0.7: Generate matrix representations of arbitrary linear differential operators
- New in version 0.8: Solve partial differential equations with Dirichlet or Neumann boundary conditions
findiff 是一个用于有限差分数值导数的 Python 包
和任意维数的偏微分方程。
特征：
- 沿任何轴以任何所需的精度顺序区分任意数量的维数阵列
- 精确处理网格边界
- 包括矢量演算中的标准运算符，如梯度、发散和卷曲
- 可以处理均匀和非均匀网格
- 可以处理具有常数和可变系数的导数的任意线性组合
- 完全矢量化的速度
- 计算均匀和非均匀网格的任何顺序和精度的原始有限差分系数
- 0.7 新版功能：生成任意线性微分算子的矩阵表示
- 0.8 版中的新功能：使用 Dirichlet 或 Neumann 边界条件求解偏微分方程
"""


# flake8: noqa: F401
from ._version import version as __version__

from .coefs import coefficients
from .operators import FinDiff, Coef, Identity, Coefficient
from .vector import Gradient, Divergence, Curl, Laplacian
from .pde import PDE, BoundaryConditions
