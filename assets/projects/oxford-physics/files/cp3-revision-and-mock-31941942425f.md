下面是整理版表格。符号约定：

$$
A^T=\text{transpose},\qquad A^\dagger=\overline{A}^{,T}.
$$

| 类型 | 定义 | 逆矩阵 | 保持什么 | 特征值性质 | 特征向量性质 | 行列式性质 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Orthogonal** 正交矩阵 | $A^T A=I$，通常 $A$ 为实矩阵 | $A^{-1}=A^T$ | 保实内积：$(Ax)^T(Ay)=x^T y$；保长度：$\lVert Ax \rVert=\lVert x \rVert$ | 所有特征值满足 $\lvert\lambda\rvert=1$；若 $\lambda\in\mathbb{R}$，则 $\lambda=\pm1$ | 不同特征值对应的特征向量正交 | $\det A=\pm1$ | 非实特征值成共轭对出现 |
| **Unitary** 酉矩阵 | $U^\dagger U=I$，通常 $U$ 为复矩阵 | $U^{-1}=U^\dagger$ | 保复内积：$(Ux)^\dagger(Uy)=x^\dagger y$；保长度：$\lVert Ux\rVert=\lVert x\rVert$ | 所有特征值满足 $\lvert\lambda\rvert=1$ | 不同特征值对应的特征向量正交 | $\lvert\det U\rvert=1$ | 一般不要求特征值共轭成对，除非矩阵本身是实矩阵 |
| **Hermitian** 厄米矩阵 | $H^\dagger=H$ | 不一定可逆；若可逆，则 $H^{-1}$ 仍是 Hermitian | 二次型为实数：$x^\dagger Hx\in\mathbb{R}$ | 所有特征值都是实数 | 不同特征值对应的特征向量正交 | $\det H\in\mathbb{R}$ | 可被 unitary 对角化：$H=U\Lambda U^\dagger$，其中 $\Lambda$ 为实对角矩阵 |
| **Symmetric** 对称矩阵 | $A^T=A$，必须为实矩阵 | 不一定可逆；若可逆，则 $A^{-1}$ 仍是对称矩阵 | 二次型为实数：$x^TAx\in\mathbb{R}$ | 所有特征值都是实数 | 不同特征值对应的特征向量正交 | $\det A\in\mathbb{R}$ | 可被正交矩阵对角化：$A=Q\Lambda Q^T$，其中 $\Lambda$ 为实对角矩阵 |

---

# 对应证明速表

| 结论 | 适用对象 | 证明核心 |
| --- | --- | --- |
| $A^{-1}=A^T$ | Orthogonal | 由 $A^TA=I$，所以 $A^T$ 是 $A$ 的逆 |
| $A^T=A$ 的特征值为实数 | Symmetric | 若 $Av=\lambda v$ 且 $A^T=A$，则 $v^TAv=\lambda v^Tv$。左边为实数，且 $v^Tv>0$，所以 $\lambda\in\mathbb{R}$ |
| $U^{-1}=U^\dagger$ | Unitary | 由 $U^\dagger U=I$，所以 $U^\dagger$ 是 $U$ 的逆 |
| 保内积 | Orthogonal / Unitary | $(Ax)^T(Ay)=x^TA^TAy=x^Ty$；$(Ux)^\dagger(Uy)=x^\dagger U^\dagger Uy=x^\dagger y$ |
| 特征值在单位圆上 | Orthogonal / Unitary | 若 $Av=\lambda v$，则 $\lVert v\rVert=\lVert Av\rVert=\lvert\lambda\rvert\lVert v\rVert$，所以 $\lvert\lambda\rvert=1$ |
| Hermitian 特征值为实数 | Hermitian | 若 $Hv=\lambda v$，则 $v^\dagger Hv=\lambda v^\dagger v$。左边为实数，且 $v^\dagger v>0$，所以 $\lambda\in\mathbb{R}$ |
| 不同特征值的特征向量正交 | Symmetric / Hermitian / Unitary / Orthogonal | 利用保内积或 $H^\dagger=H$ 或 $A^T=A$，推出 $(\lambda-\mu)\langle x,y\rangle=0$ 或等价形式 |
| 非实特征值共轭成对 | 实矩阵，例如 Orthogonal | 特征多项式系数为实数，所以若 $p(\lambda)=0$，则 $p(\overline{\lambda})=0$ |
| $\det A=\pm1$ | Orthogonal | $\det(A^TA)=\det I\Rightarrow (\det A)^2=1$ |
| $\lvert\det U\rvert=1$ | Unitary | $\det(U^\dagger U)=1\Rightarrow \overline{\det U}\det U=1$ |
| $\det H\in\mathbb{R}$ | Hermitian | Hermitian 的特征值全为实数，行列式等于特征值乘积 |

---

最容易混的地方：

| 容易混淆点 | 正确说法 |
| --- | --- |
| Symmetric 和 Hermitian 是同一类？ | 是的关系。Symmetric 是实矩阵的 Hermitian；都有实特征值和正交特征向量。 |
| Orthogonal 的特征值都是 $\pm1$？ | 错。只有实特征值才只能是 $\pm1$。一般可以是 $e^{i\theta}$。 |
| Unitary 的特征值一定共轭成对？ | 错。只有实系数矩阵才保证共轭成对。 |
| Hermitian 的特征值在单位圆上？ | 错。Hermitian 的特征值是实数，不一定模长为 1。 |
| Unitary 和 Hermitian 是同一类？ | 不是。Unitary 满足 $U^\dagger U=I$，Hermitian 满足 $H^\dagger=H$。 |
| Orthogonal 是不是 Unitary 的特例？ | 是。实矩阵中，$A^\dagger=A^T$，所以正交矩阵是酉矩阵的实数特例。 |
