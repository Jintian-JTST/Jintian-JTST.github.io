# Lvovsky《Quantum Physics: An Introduction Based on Photons》第 1–3.3 章学习笔记

> 全书主线：第 1 章在最简单的二维 Hilbert 空间（光子偏振 qubit）上建立量子力学全部公理 → 第 2 章引入张量积与纠缠，讨论非局域性与测量的本质 → 第 3 章把同一套公理推广到连续无穷维空间，处理一维运动。

---

# 第 1 章 The Quantum Postulates（量子假设）

## 1.1 量子力学的适用范围

经典物理用**量**（quantities，如速度、电流）描述世界，原则上一切量都可以无限精确地获知——*经典世界是无限可知的*。量子物理中某些知识**原则上**不可同时获得（如位置与动量的同时精确值），因此必须改用 **quantum state（量子态）** 描述系统：它内禀地包含了"可知与不可知的边界"。

**Correspondence principle（对应原理）**：任何更新的理论必须在旧理论已被检验的领域复现旧理论的结果。例如相对论在低速极限回到牛顿力学；量子物理在宏观极限回到经典物理。用量子物理描述宏观现象通常是不必要的过度复杂化。

量子力学的主要数学工具是**线性代数**（附录 A）。

## 1.2 The Hilbert Space Postulate（希尔伯特空间公设）

> **第一公设**：
> a) 物理系统的所有可能状态构成**复数域**上的 Hilbert space；
> b) **不相容**（incompatible）的量子态对应**正交**向量；
> c) 代表物理态的向量都是**归一化**的（norm = 1）。

- **Physical system（物理系统）**：可独立于其他自由度研究的对象或自由度（一个原子的整体运动、其内部电子运动等可视为不同的物理系统）。
- **不相容**的含义：若系统确定处于态 A，则测量绝不会发现它处于态 B。例如 $|x=5\,\mathrm{m}\rangle$ 与 $|x=3\,\mathrm{m}\rangle$ 不相容（正交）；但 $|x=5\,\mathrm{m}\rangle$ 与 $|v=4\,\mathrm{m/s}\rangle$ 不正交——动量确定的态位置完全不确定，仍可能在 $x=5$ m 被探测到。
- 空间是线性的 ⟹ **superposition（叠加）原理**：若 $|a\rangle,|b\rangle$ 是合法物理态，则 $(|a\rangle+|b\rangle)/\sqrt2$ 也是。宏观叠加态（Schrödinger's cat）数学上合法，但极其脆弱、会迅速退化为其中一个分量（第 2 章 decoherence 解释），故日常不可见；微观叠加态则相对稳健且是物理描述所必需。

## 1.3 光子偏振（photon polarization）

水平偏振 $|H\rangle$ 与垂直偏振 $|V\rangle$ 不相容（$|H\rangle$ 光子过 polarizing beam splitter 必透射、永不反射）⟹ 正交，构成二维 Hilbert 空间的 **canonical basis** $\{|H\rangle,|V\rangle\}$。

经典波 $\vec E(z,t)=\mathrm{Re}\big[(A_H e^{i\varphi_H}\hat i + A_V e^{i\varphi_V}\hat j)\,e^{ikz-i\omega t}\big]$ 对应的单光子态：

$$|\psi\rangle = \frac{1}{\sqrt{A_H^2+A_V^2}}\left(A_H e^{i\varphi_H}|H\rangle + A_V e^{i\varphi_V}|V\rangle\right)e^{-i\omega t}$$

**重要偏振态（Table 1.1，必背）**：

| 态 | 矩阵 | 描述 |
|---|---|---|
| $\|H\rangle$ | $\binom{1}{0}$ | 水平 |
| $\|V\rangle$ | $\binom{0}{1}$ | 垂直 |
| $\|\theta\rangle=\cos\theta\,\|H\rangle+\sin\theta\,\|V\rangle$ | $\binom{\cos\theta}{\sin\theta}$ | 与水平成 $\theta$ 角的线偏振 |
| $\|{+}\rangle\equiv\|{+}45^\circ\rangle=\frac{1}{\sqrt2}(\|H\rangle+\|V\rangle)$ | $\frac{1}{\sqrt2}\binom{1}{1}$ | 对角偏振 |
| $\|{-}\rangle\equiv\|{-}45^\circ\rangle=\frac{1}{\sqrt2}(\|H\rangle-\|V\rangle)$ | $\frac{1}{\sqrt2}\binom{1}{-1}$ | 反对角偏振 |
| $\|R\rangle=\frac{1}{\sqrt2}(\|H\rangle+i\|V\rangle)$ | $\frac{1}{\sqrt2}\binom{1}{i}$ | 右旋圆偏振 |
| $\|L\rangle=\frac{1}{\sqrt2}(\|H\rangle-i\|V\rangle)$ | $\frac{1}{\sqrt2}\binom{1}{-i}$ | 左旋圆偏振 |

$\{|H\rangle,|V\rangle\}$、$\{|+\rangle,|-\rangle\}$（diagonal basis）、$\{|R\rangle,|L\rangle\}$（circular basis）都是正交归一基。

**Phase factor（相位因子）**：整体乘 $e^{i\varphi}$（$\varphi$ 实）不改变态的物理性质（$|V\rangle$ 与 $-|V\rangle$ 同一物理对象）；但**相对相位**改变物理：只给 $|+\rangle$ 的 $V$ 分量加 $\pi/2$ 相位得 $(|H\rangle+i|V\rangle)/\sqrt2=|R\rangle$，是不同的物理态。因此式中 $e^{-i\omega t}$ 因子可暂时忽略。

**为什么偏振空间 2 维而位置空间无穷维**：任何线偏振态都能写成 $|H\rangle,|V\rangle$ 的叠加（对角偏振光部分透过水平 PBS）；而不同位置态全部互相正交、无法互相叠加表出。

光子偏振是 **qubit（量子比特）**——任何二维 Hilbert 空间信息载体——的一种实现。与经典 bit 不同，qubit 可以处于基态的叠加。

**Box 1.1 光子的发现**：Planck（1900，黑体辐射）$E=\hbar\omega$，$\hbar=1.054\,571\,48\times10^{-34}$ J·s；Einstein（1905 光电效应；1916 光子动量 $p=E/c=\hbar\omega/c=2\pi\hbar/\lambda$）；Compton（1923，X 射线-电子散射证实光子存在）；"photon"一词由 G. Lewis 于 1926 年引入。

## 1.4 量子测量

### 1.4.1 Measurement Postulate（测量公设）

经典测量只是技术问题（可不扰动地测量）；量子测量中"我们很大、对象很小"，测量几乎必然改变系统状态，且是微观量子态影响宏观仪器的事件——跨越量子与经典的边界。

单光子 $|\psi\rangle=\psi_H|H\rangle+\psi_V|V\rangle$ 打到 PBS：光子是不可分割的最小能量单元，不能分裂；但大量光子的统计必须复现经典分光比 $A_H^2/A_V^2$。唯一的调和方式是**随机性**：

> **测量公设**：理想测量装置关联一组正交归一基 $\{|v_i\rangle\}$。测量后装置随机指向某个 $|v_i\rangle$，概率由 **Born's rule** 给出
> $$\mathrm{pr}_i = |\langle v_i|\psi\rangle|^2,$$
> 系统（若未被销毁）被投影（**collapse，塌缩**）到 $|v_i\rangle$。

- 这类测量称 **projective measurement（投影测量）**。塌缩后在同一基重复测量不再有随机性。
- 物理实现：PBS + 两个 single-photon detector 实现 canonical 基测量；前置 $\lambda/2$ @ $22.5^\circ$ 实现 diagonal 基；前置 $\lambda/4$ @ $0^\circ$ + $\lambda/2$ @ $22.5^\circ$ 实现 circular 基（Fig. 1.2）。任意正交基均可实现。
- 概率归一：$\sum_i \mathrm{pr}_i = \langle\psi|\psi\rangle = 1$；整体相位不影响任何测量概率。
- 量子随机性击碎了 19 世纪末的决定论信念（Einstein："God does not play dice"，由此引出 EPR，见第 2 章）。

### 1.4.2 偏振测量与量子层析

单次测量信息极少（如在 canonical 基测得透射，只能排除 $|V\rangle$）。对**同一态的多份拷贝**反复测量得到 **measurement statistics**：在 canonical 基得 $|\psi_H|^2,|\psi_V|^2$；再补充 diagonal、circular 基的统计（$\mathrm{pr}_+,\mathrm{pr}_R$ 等），可把 $\psi_H,\psi_V$ 确定到一个公共相位因子——完整重构量子态。该方法称 **quantum state tomography（量子态层析）**（Ex. 1.15：六个概率 $\mathrm{pr}_H,\mathrm{pr}_V,\mathrm{pr}_\pm,\mathrm{pr}_{R,L}$ 中 $\mathrm{pr}_H,\mathrm{pr}_+,\mathrm{pr}_R$ 已足够；只用两组基不够）。

**叠加态 vs 统计混合（ensemble）**（Ex. 1.12，重要）：

- 叠加态 $|+\rangle$：canonical 基测得 50/50；diagonal 基测得确定的 "+"。
- 混合态"½ 概率 $|H\rangle$ 或 ½ 概率 $|V\rangle$"：canonical 基 50/50；diagonal 基也 50/50。

混合态不是 Hilbert 空间中的向量（第 5 章用 density matrix 描述）。

**Box 1.2 单光子探测器**：超导纳米线探测器——吸收单光子局部失超→电阻脉冲。特性参数：quantum efficiency（响应概率，现代可 >99%）、non-discriminating（不能分辨光子数）、dark counts（无光子时的误触发）。

## 1.5 量子干涉与互补性

**单光子 Mach–Zehnder 干涉仪**（Fig. 1.3）：$|+\rangle$ 入射，第一个 PBS 透射 H 分量、反射 V 分量；V 路经可变 delay line 获得相位 $\varphi = kl$；第二个 PBS 合束，输出 $|\psi\rangle = (|H\rangle + e^{i\varphi}|V\rangle)/\sqrt2$；在 diagonal 基测量：

$$\mathrm{pr}_\pm = \tfrac12(1\pm\cos\varphi)$$

改变 delay line 长度即观察到**干涉条纹**——由单个光子产生。光子不可分裂，却"同时"以叠加形式存在于两条路径——这就是 **wave-particle duality（波粒二象性）**。

**Welcher-Weg（which-way）测量**：若在臂中放置（哪怕无损的）路径探测器，测量将叠加塌缩为路径的统计混合，**quantum coherence**（叠加分量间确定的相位关系）丢失，干涉条纹消失——即使没有人查看探测器读数。这体现 **quantum complementarity（量子互补性）**：路径信息与干涉不可同时获得。

**Box 1.4 Elitzur–Vaidman "炸弹检验"（interaction-free measurement）**：臂中可能藏有"见单光子即爆"的炸弹。调 $\varphi=0$ 使无炸弹时探测器 "−" 永不响。炸弹存在时它实施了 which-way 测量：光子 50% 走下路引爆炸弹；50% 走上路，炸弹未爆、光子以 $|V\rangle$ 出射，在 diagonal 基测量时 25% 触发 "−"。因此 "−" 一响即可断定炸弹存在——而光子从未与炸弹相互作用。用高精细度谐振腔可将效率推近 100%。

## 1.6 量子密码学

**Box 1.5 经典密码**：private-key（one-time pad，逐位 XOR）绝对安全但密钥分发昂贵；public-key（RSA 等单向函数）便宜但可被算力与量子计算机攻破。**Quantum key distribution（QKD）** 兼得两者之长：安全性由自然规律保证，且无需预共享秘密。

### 1.6.1 BB84 协议（Bennett & Brassard, 1984）

1. Alice 随机选 bit（0/1）并随机选编码基（canonical 或 diagonal）：
   $$\begin{cases}0\to|H\rangle\\ 1\to|V\rangle\end{cases}\quad\text{或}\quad\begin{cases}0\to|{+}45^\circ\rangle\\ 1\to|{-}45^\circ\rangle\end{cases}$$
2. Bob 随机选基测量。同基 ⟹ 结果与 Alice 一致；异基 ⟹ 结果随机。
3. 事后经公开经典信道比对**基的选择**（不公开 bit 值），保留同基事件 → 共享密钥（用作 one-time pad）。
4. 防窃听：Eve 不知道每个光子的编码基，intercept-resend 攻击必然以一定概率改变光子态，使 Alice–Bob 密钥出现 **25% 错误率**（Ex. 1.18）。双方公开比对一部分密钥位即可检测窃听。错误率低于约 **11%**（Shor–Preskill 界）时可用 **privacy amplification** 提纯出完全保密的密钥。

### 1.6.2 实际问题

光纤损耗服从 **Beer's law** $n(L)=n_0e^{-\beta L}$（优质光纤约 5%/km）。光子率指数衰减而 dark counts 恒定，错误占比随距离上升，超过 11% 阈值后无法保密 ⟹ 直接传输距离上限约数百公里。提高发射率收效甚微（指数规律），根本出路是 **quantum repeater**（第 2 章末）。

## 1.7 量子力学中的算符

线性算符的双重角色：① 描述态的**演化**；② 形式化描述**测量**（→ 1.9 节 observable）。

**Waveplate（波片）约定**：光轴与水平成 $\theta$ 角的波片使 extraordinary 分量获得相移 $\Delta\varphi$（ordinary 分量不变）：

$$|\theta\rangle \to e^{i\Delta\varphi}|\theta\rangle,\qquad \left|\tfrac\pi2+\theta\right\rangle \to \left|\tfrac\pi2+\theta\right\rangle$$

$\Delta\varphi=\pi$ 为 half-wave plate（HWP），$\Delta\varphi=\pi/2$ 为 quarter-wave plate（QWP）。在 canonical 基（Ex. 1.24）：

$$\hat A_{\mathrm{HWP}}(\alpha)=\begin{pmatrix}-\cos2\alpha & -\sin2\alpha\\ -\sin2\alpha & \cos2\alpha\end{pmatrix},\qquad
\hat A_{\mathrm{QWP}}(\alpha)=\begin{pmatrix}\sin^2\alpha+i\cos^2\alpha & (i-1)\sin\alpha\cos\alpha\\ (i-1)\sin\alpha\cos\alpha & i\sin^2\alpha+\cos^2\alpha\end{pmatrix}$$

重要推论：HWP@$\alpha$ 把线偏振 $|\theta\rangle$ 变为 $|2\alpha-\theta\rangle$（关于光轴的镜像）；QWP（光轴水平/垂直）在圆偏振与 $\pm45^\circ$ 偏振之间互换。

**Pauli operators（必背）**：

$$\hat\sigma_x \equiv |H\rangle\langle V|+|V\rangle\langle H| \simeq \begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
\hat\sigma_y \equiv -i|H\rangle\langle V|+i|V\rangle\langle H| \simeq \begin{pmatrix}0&-i\\i&0\end{pmatrix},\quad
\hat\sigma_z \equiv |H\rangle\langle H|-|V\rangle\langle V| \simeq \begin{pmatrix}1&0\\0&-1\end{pmatrix}$$

**Hadamard operator**：$\hat H = \frac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$，把 $|H\rangle\mapsto|+\rangle$、$|V\rangle\mapsto|-\rangle$，可用 HWP@$\pi/8$ 实现。

**Box 1.6 如何产生单光子**：衰减激光（泊松分布，不是真单光子，但弱衰减下可用于 QKD）；单原子自发辐射 / cavity QED；固态类原子源（色心、量子点）；**spontaneous parametric down-conversion（SPDC）**——强激光过非线性晶体，单光子自发劈裂为一对低能光子，探测其一即"预告"（herald）另一个的存在（heralded single-photon source）。

## 1.8 投影算符与未归一化态

约定扩展：norm < 1 的态表示"以概率 $\mathrm{pr}_a = \||a\rangle\|^2 = \langle a|a\rangle$ 存在"的态——**unnormalized state**。

**Projection operator（投影算符）**：

$$\hat\Pi_i = |v_i\rangle\langle v_i|,\qquad \hat\Pi_i|\psi\rangle = \langle v_i|\psi\rangle\,|v_i\rangle \equiv |\psi_i'\rangle$$

测量把 $|\psi\rangle$ 变为未归一化态集 $\{|\psi_i'\rangle\}$，每个的 $\langle\psi_i'|\psi_i'\rangle = |\langle v_i|\psi\rangle|^2 = \mathrm{pr}_i$ 正是 Born 概率。

## 1.9 量子可观测量

### 1.9.1 Observable operators

给测量基每个元素 $|v_i\rangle$ 关联实数 $v_i$（测量读数），打包为 **observable（可观测量算符）**：

$$\hat V = \sum_i v_i\,|v_i\rangle\langle v_i|$$

$\{|v_i\rangle\}$ 是其本征基（eigenbasis），$v_i$ 是本征值。**可观测量 ⟺ Hermitian 算符**（Ex. 1.30：物理可观测量必 Hermitian；任何 Hermitian 算符按 spectral theorem 都可写成上式）。已知 Hermitian 矩阵 ⟹ 谱分解还原出测量基和读数。

例（Ex. 1.29）：

$$|H\rangle\langle H|-|V\rangle\langle V| = \hat\sigma_z,\qquad |+\rangle\langle +|-|-\rangle\langle -| = \hat\sigma_x,\qquad |R\rangle\langle R|-|L\rangle\langle L| = \hat\sigma_y$$

注意：**时间不是算符**——没有时间本征态或时间量子，时间只是参数。同一算符的两种角色（态变换 vs 测量装置）物理实现完全不同。

### 1.9.2 期望值与不确定度

在态 $|\psi\rangle$ 中测量 $\hat V$：

$$\langle V\rangle = \langle\psi|\hat V|\psi\rangle$$

$$\big\langle \Delta V^2 \big\rangle = \big\langle\psi\big|\big(\hat V-\langle\psi|\hat V|\psi\rangle\big)^2\big|\psi\big\rangle = \langle\psi|\hat V^2|\psi\rangle - \langle\psi|\hat V|\psi\rangle^2$$

**uncertainty（不确定度）** = 方差的平方根。例：$|+\rangle$ 中测 $\hat\sigma_z$：$\langle\sigma_z\rangle=0$，$\langle\Delta\sigma_z^2\rangle=1$。

**经典过渡**：$N$ 个 $|+\rangle$ 光子过 PBS，透射-反射光子数之差 $N_-$ 的期望为 0、涨落 $\sqrt{\langle\Delta N_-^2\rangle}=\sqrt N$；相对涨落 $1/\sqrt N\to0$——宏观光强下量子随机性湮没于精度之下（对应原理）。

### 1.9.3 The uncertainty principle（不确定性原理）

- $|\psi\rangle$ 中 $\hat V$ 零不确定度 ⟺ $|\psi\rangle$ 是 $\hat V$ 的本征态（Ex. 1.35）。
- 两个 Hermitian 算符可同时对角化（可同一装置测量，"compatible"）⟺ $[\hat A,\hat B]=0$（Ex. 1.36）。
- 对任意 Hermitian $\hat A,\hat B$ 与任意态（Ex. 1.39，用 Cauchy–Schwarz）：

$$\boxed{\;\big\langle \Delta A^2\big\rangle\big\langle \Delta B^2\big\rangle \ge \frac14\big|\big\langle[\hat A,\hat B]\big\rangle\big|^2\;}$$

- 特例（Ex. 1.41）：若 $[\hat A,\hat B]=\varepsilon\hat 1$，则对**一切态** $\langle\Delta A^2\rangle\langle\Delta B^2\rangle \ge |\varepsilon|^2/4$。位置-动量 $[\hat x,\hat p]=i\hbar$ 即属此类：$\sqrt{\langle\Delta x^2\rangle\langle\Delta p^2\rangle}\ge\hbar/2$。

物理意义：不确定性不是仪器缺陷，而是态的内禀属性——为某可观测量优化的装置测量与之不对易的可观测量时必然表现随机。

## 1.10 量子演化

从光子 $|\psi(t)\rangle = |\psi(0)\rangle e^{-i\omega t}$ 与 $E=\hbar\omega$ 出发：能量本征态演化为

$$|\psi_E(t)\rangle = |\psi_E(0)\rangle\,e^{-\frac{i}{\hbar}Et}$$

由 de Broglie 假设推广为公设：对一切非相对论量子系统成立。Hamiltonian（能量可观测量）谱分解 $\hat H=\sum_j E_j|E_j\rangle\langle E_j|$，任意初态 $|\psi(0)\rangle=\sum_j\psi_j|E_j\rangle$ 逐项演化：

$$|\psi(t)\rangle = \sum_j \psi_j\,|E_j\rangle\,e^{-\frac{i}{\hbar}E_j t}$$

三种等价表述：

1. **能量基分解**（上式）。
2. **Evolution operator**：$|\psi(t)\rangle = \hat U(t)|\psi(0)\rangle$，
   $$\hat U(t) = e^{-\frac{i}{\hbar}\hat Ht}$$
   $\hat U$ 是 **unitary** 的：保 norm（物理态→物理态）、可逆（$\hat H\to-\hat H$ 等价于时间反演；孤立量子系统演化不丢失信息、熵不增）。
3. **Schrödinger equation**：
   $$\frac{d|\psi(t)\rangle}{dt} = -\frac{i}{\hbar}\hat H|\psi(t)\rangle$$
   矩阵形式 $\binom{\dot\psi_H}{\dot\psi_V} = -\frac{i}{\hbar}\begin{pmatrix}H_{HH}&H_{HV}\\H_{VH}&H_{VV}\end{pmatrix}\binom{\psi_H}{\psi_V}$。

能量本征态只获得相位、物理不变 ⟹ **stationary states**。叠加态（如 $(|E_1\rangle+|E_2\rangle)/\sqrt2$）的物理构成随时间真实变化。波片演化与 Hamiltonian 演化数学等价（本征态获得不同相位），但物理机制不同（折射率差 vs 能量差）。

**第 1 章骨架**：态 = Hilbert 空间归一向量；测量 = 正交基上的随机投影，$\mathrm{pr}=|\langle v|\psi\rangle|^2$；可观测量 = Hermitian 算符；演化 = $e^{-i\hat Ht/\hbar}$ 的 unitary 变换。

---

# 第 2 章 Entanglement（纠缠）

## 2.1 Tensor product spaces（张量积空间）

### 2.1.1 张量积态与纠缠态

两个（曾经/正在）相互作用的系统必须作为整体处理：联合空间为 **tensor product space** $\mathbb V_A\otimes\mathbb V_B$。记号 $|H\rangle_A\otimes|V\rangle_B \equiv |H\rangle|V\rangle \equiv |HV\rangle$（第一个符号属于 Alice）。维数 $\dim(\mathbb V_A\otimes\mathbb V_B)=NM$；$\{|v_i\rangle\otimes|w_j\rangle\}$ 是正交归一基（两光子偏振空间为 4 维，基 $\{|HH\rangle,|HV\rangle,|VH\rangle,|VV\rangle\}$）。

运算规则：

$$\lambda(|a\rangle\otimes|b\rangle) = (\lambda|a\rangle)\otimes|b\rangle = |a\rangle\otimes(\lambda|b\rangle)$$

$$(|a_1\rangle+|a_2\rangle)\otimes|b\rangle = |a_1\rangle\otimes|b\rangle + |a_2\rangle\otimes|b\rangle\quad(\text{对第二因子同理})$$

$$\langle ab|a'b'\rangle = \langle a|a'\rangle\,\langle b|b'\rangle$$

能写成 $|a\rangle\otimes|b\rangle$ 的态叫 **separable（可分的）**；不能的叫 **entangled（纠缠的）**——非局域叠加。

**Bell states（必背，构成两 qubit 空间的正交归一基）**：

$$|\Psi^\pm\rangle = \frac{1}{\sqrt2}\big(|HV\rangle \pm |VH\rangle\big),\qquad
|\Phi^\pm\rangle = \frac{1}{\sqrt2}\big(|HH\rangle \pm |VV\rangle\big)$$

**$|\Psi^-\rangle$ 的 isotropy（各向同性，Ex. 2.9，全章反复使用）**：对任意 $\theta$，

$$|\Psi^-\rangle = \frac{1}{\sqrt2}\Big(|\theta\rangle\otimes\big|\tfrac\pi2+\theta\big\rangle - \big|\tfrac\pi2+\theta\big\rangle\otimes|\theta\rangle\Big)$$

在 Bell 态中唯有 $|\Psi^-\rangle$ 具有此性质。

**Box 2.1 纠缠态的制备**：两块级联非线性晶体的 SPDC，第一块只产生 $|HH\rangle$ 对、第二块只产生 $|VV\rangle$ 对，输出 $|HH\rangle+e^{i\varphi}|VV\rangle$，选取 $\varphi$ 得 $|\Phi^\pm\rangle$；一臂加 HWP 可转换为 $|\Psi^\pm\rangle$。

### 2.1.2 张量积空间中的测量

测量公设照常适用；测量基可由可分态构成（= Alice、Bob 各自局域测量），也可含纠缠态。重要结论：**纠缠态只能通过相互作用产生，但区分/层析纠缠态只需局域测量**（如区分 $|\Psi^-\rangle$ 与 $|\Psi^+\rangle$：canonical 基测量无法区分，diagonal 基可以）。

### 2.1.3 算符的张量积

$$(\hat A\otimes\hat B)\Big(\sum_i\lambda_i|a_i\rangle\otimes|b_i\rangle\Big) \equiv \sum_i\lambda_i(\hat A|a_i\rangle)\otimes(\hat B|b_i\rangle)$$

矩阵元（双指标）：$C_{ij,i'j'} = \langle v_iw_j|\hat C|v_{i'}w_{j'}\rangle = A_{ii'}B_{jj'}$。性质：$\hat A_1\hat A_2\otimes\hat B_1\hat B_2 = (\hat A_1\otimes\hat B_1)(\hat A_2\otimes\hat B_2)$；$(\hat A\otimes\hat B)^\dagger = \hat A^\dagger\otimes\hat B^\dagger$；Hermitian⊗Hermitian = Hermitian，unitary⊗unitary = unitary；$|a_1\rangle\langle a_2|\otimes|b_1\rangle\langle b_2| = |a_1b_1\rangle\langle a_2b_2|$。本征值：$\hat A|v\rangle=v|v\rangle,\ \hat B|w\rangle=w|w\rangle \Rightarrow (\hat A\otimes\hat B)|vw\rangle = vw|vw\rangle$。

**No-cloning theorem（Wootters–Zurek 1982，Ex. 2.19）**：不存在使任意 $|a\rangle\otimes|0\rangle \to |a\rangle\otimes|a\rangle$ 的物理演化。证明要点：物理演化是线性算符；对基矢克隆成立时，线性性给出 $\sum_i\psi_i|v_i\rangle|v_i\rangle$，而真正克隆要求 $\big(\sum_i\psi_i|v_i\rangle\big)\otimes\big(\sum_i\psi_i|v_i\rangle\big)$，两者不等。

### 2.1.4 Local operators

形如 $\hat A\otimes\hat 1$ 或 $\hat 1\otimes\hat B$ 的算符（如只插在 Alice 光路中的波片）。要点：

- **局域 unitary 操作不能改变态的纠缠性**（Ex. 2.22）；张量积算符不能从可分态制造纠缠态（Ex. 2.17）——产生纠缠必须有相互作用。
- $\hat H = \hat H_A + \hat H_B$（局域 Hamiltonian 之和）⟹ 可分初态保持可分，各自独立演化；总能量 $E = E_A + E_B$。
- Alice 对 $|\Psi^-\rangle$ 局域施加 Pauli 算符可在 Bell 态间切换（Ex. 2.25）：$(\hat\sigma_z)_A|\Psi^-\rangle = |\Psi^+\rangle$，$(\hat\sigma_x)_A|\Psi^-\rangle = -|\Phi^-\rangle$，$(\hat\sigma_y)_A|\Psi^-\rangle = i|\Phi^+\rangle$。

**Box 2.2 Quantum dense coding**：Holevo bound——$n$ 个 qubit 至多承载 $n$ 个经典 bit。但若预共享 $|\Psi^-\rangle$：Alice 按要发送的 2 bit 选择 $\hat 1,\hat\sigma_x,\hat\sigma_y,\hat\sigma_z$ 之一作用于自己的 qubit（共享态变为四个 Bell 态之一），寄给 Bob；Bob 在 Bell 基测量两个 qubit 即恢复 2 bit——只传一个 qubit 送达 2 bit。

## 2.2 纠缠态的局域测量

### 2.2.1 Remote state preparation（远程态制备）

共享 $|\Psi^-\rangle$，Alice 在基 $\{|\theta\rangle,|\tfrac\pi2+\theta\rangle\}$ 测量（用 isotropy）：

- 若得 $|\theta\rangle$（概率 ½），Bob 的光子瞬间变为 $\big|\tfrac\pi2+\theta\big\rangle$；
- 若得 $\big|\tfrac\pi2+\theta\big\rangle$（概率 ½），Bob 的光子变为 $|\theta\rangle$。

Alice 通过选择测量基，可在任意远处"瞬间"制备任意线偏振态（有 ±90° 二义性）——表面上违反相对论与因果律。实验（包括类空间隔的安排）已充分证实量子预言。注意与经典关联（"鞋盒类比"：一双鞋分装两盒寄给两人，打开一盒立刻知道另一只的左右）的区别：量子态还携带**相位关系**，关联性随双方基的选择而变，远超经典图像。

### 2.2.2 Partial inner product 与局域测量法则

**Partial inner product**：对 $|\Psi\rangle = \sum_{ij}\Psi_{ij}|v_i\rangle\otimes|w_j\rangle$ 与 Alice 空间局域态 $|a\rangle$，

$$\langle a|\Psi\rangle \equiv \sum_{ij}\Psi_{ij}\,\langle a|v_i\rangle\,|w_j\rangle \in \mathbb V_B$$

（结果与基的选择无关。）把 $|\Psi\rangle$ 按 Alice 的测量基展开：

$$|\Psi\rangle = \sum_i \frac{1}{\mathcal N_i}\,|v_i\rangle\otimes|b_i\rangle,\qquad |b_i\rangle = \mathcal N_i\langle v_i|\Psi\rangle\ \text{（归一化）},\quad \mathcal N_i = \Big(\sum_j|\Psi_{ij}|^2\Big)^{-1/2}$$

> **局域测量法则**：Alice 在基 $\{|v_i\rangle\}$ 中测量，得到结果 $i$ 的概率为
> $$\mathrm{pr}_{A,i} = \frac{1}{\mathcal N_i^2} = \big\|\langle v_i|\Psi\rangle\big\|^2 = \langle\Psi|v_i\rangle\langle v_i|\Psi\rangle,$$
> 此时 Bob 的系统被投影到 $|b_i\rangle = \mathcal N_i\langle v_i|\Psi\rangle$。

（等价地：投影算符 $\hat\Pi_i = |v_i\rangle\langle v_i|\otimes\hat 1$ 作用后的未归一化态的 norm² 即概率。）纠缠态经局域测量后塌缩为**可分**态。

### 2.2.3 局域测量与因果律（关键论证）

- **时序无关性**（Ex. 2.41）：同时测 / Alice 先 / Bob 先，三种场景的联合概率都为 $\mathrm{pr}_{ij} = |\langle v_iw_j|\Psi\rangle|^2$。
- Bob 不知道 Alice 的结果时，他那边任何可测统计都不变（对 Bell 态：任何基都是 50/50，Ex. 2.37/2.40）⟹ **远程制备不能用于超光速通信**。"态"瞬间改变，但量子态是理论构造、从不被单次直接观测；可观测的只有统计，而统计不受影响。
- 更尖锐的版本：Bob **先**测量并销毁了光子，Alice 后测，按 Alice 结果 $|\theta\rangle$ 做 postselection，Bob 的数据仍重构出 $|\tfrac\pi2+\theta\rangle$——"远程制备"甚至发生在 Bob 测量之后。
- 若量子克隆可能，则结合远程制备与层析可实现超光速通信（Ex. 2.44）——no-cloning 保护了因果律。

### 2.2.4 Mixed states（混合态）

Alice 丢失了她那一半（或不告知结果）：Bob 的光子只能描述为 **ensemble**——对 $|\Psi^-\rangle$ 即"½ 概率 $|H\rangle$ 或 ½ 概率 $|V\rangle$"（等价地"½ $|+\rangle$ 或 ½ $|-\rangle$"、"½ $|R\rangle$ 或 ½ $|L\rangle$"——这些描述给出完全相同的测量统计，物理上等价）。其偏振**完全混合**（类似自然光），不对应 Hilbert 空间中任何向量。

> **失去纠缠态的一部分 ⟹ 剩余部分丧失 coherence，从量子叠加退化为经典统计混合。** 这与 1.5 节 Welcher-Weg 测量破坏干涉是同一机制（见 2.4 节）。

## 2.3 Quantum nonlocality（量子非局域性）

### 2.3.1 Einstein–Podolsky–Rosen 佯谬（1935；此处为 Bohm 1951 偏振版）

**Element of physical reality（物理实在元素）**：测量前即可被确定预测的物理量。共享 $|\Psi^-\rangle$：

- Alice 在 canonical 基测量 ⟹ Bob 的 $\hat\sigma_z$ 结果可确定预测 ⟹ $\hat\sigma_z$ 是 Bob 光子的实在元素；
- Alice 在 diagonal 基测量 ⟹ 同理 $\hat\sigma_x$ 是实在元素。

**Locality principle（局域实在论）**：相距遥远的一方的操作不能改变另一方处的物理实在 ⟹ $\hat\sigma_z$ 与 $\hat\sigma_x$ 必须**同时**是 Bob 光子的实在元素。但二者不对易、无共同本征态——量子理论无法容纳。EPR 结论："量子力学对实在的描述不完备"，暗示可能存在**隐变量（hidden parameters）**理论：粒子在产生时即携带预先决定一切测量结果的参数（鞋盒类比中装箱人知道的"左/右"）。EPR 未给出具体理论，当时看似不可检验。

### 2.3.2 The Bell inequality（1964）

Bell 的天才之处：不需要知道任何隐变量理论的细节，仅从"前面板"描述+局域实在论即可导出可检验的预言。装置：Alice、Bob 各持一台仪器，各有 $M,N$ 两个按钮、显示 $\pm1$；中央源每次发出一对粒子；双方随机按钮并记录读数；事后计算

$$\langle S\rangle = \langle M_AM_B\rangle - \langle M_AN_B\rangle + \langle N_AM_B\rangle + \langle N_AN_B\rangle$$

局域实在论下，每个事件的四个值 $(M_A,N_A,M_B,N_B)$ 由隐变量 $\lambda_A,\lambda_B$（可关联）与局域算法预先决定，服从合法的联合概率分布，由 $M_A(M_B-N_B)+N_A(M_B+N_B)=\pm2$ 得 **Bell inequality（CHSH 形式）**：

$$\boxed{\;\big|\langle M_AM_B\rangle - \langle M_AN_B\rangle + \langle N_AM_B\rangle + \langle N_AN_B\rangle\big| \le 2\;}$$

### 2.3.3 违反 Bell 不等式

量子方案：共享 $|\Psi^-\rangle$；双方测量可观测量

$$\hat\sigma_\theta = |\theta\rangle\langle\theta| - \big|\tfrac\pi2+\theta\big\rangle\big\langle\tfrac\pi2+\theta\big|$$

角度选取：Alice 的 $M,N$ 对应 $\theta = 0,\ \pi/4$；Bob 的对应 $\theta = \pi/8,\ 3\pi/8$。利用 isotropy 算得各关联项 $\mp1/\sqrt2$，于是

$$\langle S\rangle_{\mathrm{QM}} = -2\sqrt2 \quad\Rightarrow\quad |\langle S\rangle| = 2\sqrt2 > 2$$

**局域实在论被实验排除**。两类 loophole：**locality loophole**（双方太近可能互相影响；用数百米–千米级距离 + 纳秒级电光调制随机选基，使决策处于类空间隔）；**detection loophole**（探测效率低时需 fair sampling 假设；用高效探测器关闭）。2015 年三个实验（Hanson 组 NV 色心 + entanglement swapping；Zeilinger 组与 Shalm 组的高效率光子实验）同时关闭两大 loophole。

### 2.3.4 Greenberger–Horne–Zeilinger (GHZ) nonlocality

三方共享

$$|\Psi_{GHZ}\rangle = \frac{1}{\sqrt2}\big(|HHH\rangle + |VVV\rangle\big)$$

可验证 $|\Psi_{GHZ}\rangle$ 是 $\hat\sigma_y\otimes\hat\sigma_y\otimes\hat\sigma_x$（及两个轮换）的本征态，本征值 $-1$；同时是 $\hat\sigma_x\otimes\hat\sigma_x\otimes\hat\sigma_x$ 的本征态，本征值 $+1$。局域实在论：把前三条关系 $\sigma_{y_A}\sigma_{y_B}\sigma_{x_C} = \sigma_{y_A}\sigma_{x_B}\sigma_{y_C} = \sigma_{x_A}\sigma_{y_B}\sigma_{y_C} = -1$ 相乘（每个 $\sigma_y$ 出现两次、平方为 1），得 $\sigma_{x_A}\sigma_{x_B}\sigma_{x_C} = -1$；量子预言为 $+1$。**无需统计不等式，每一次测量都直接矛盾。**

## 2.4 量子测量的本质

### 2.4.1 Von Neumann measurements

矛盾：演化是 unitary（线性、确定论）的，测量却是随机、非线性的塌缩——它们如何相容？测量到底发生在哪一刻（光子过 PBS？雪崩产生？人耳听到 click？）

**Von Neumann 模型**：把仪器也当作量子系统。测量 = 系统与仪器经 unitary 演化**纠缠**：

$$\hat U\big(|\psi\rangle\otimes|w_1\rangle\big) = \sum_{i=1}^N \psi_i\,|v_i\rangle\otimes|w_i\rangle$$

其中 $\{|w_i\rangle\}$ 宏观可分辨（不同的灯亮、指针位置）。（这不违反 no-cloning：克隆的是基矢标签而非叠加本身。）例如 $|\Psi_{SA}\rangle = \alpha|H\rangle\otimes|\text{探测器1雪崩}\rangle + \beta|V\rangle\otimes|\text{探测器2雪崩}\rangle$。若观察者 Alice 听到 click，她也加入纠缠：

$$|\Psi_{SAO}\rangle = \alpha|H\rangle|\text{雪崩1}\rangle|\text{Alice听到1}\rangle + \beta|V\rangle|\text{雪崩2}\rangle|\text{Alice听到2}\rangle$$

关键论点：**身处叠加之中的观察者原则上无法把自己投影到对角基**，因而无法察觉另一分支的存在——对她而言，塌缩"已经发生"、结果"随机"。**塌缩是主观现象**；客观上（量子理论的理论实在中）波函数从不塌缩、演化始终决定论——量子随机性是观察能力受限造成的错觉。实验室外尚未卷入纠缠的 Bob 理论上仍可通过对 photon+detector+Alice 整体做对角基测量验证叠加的存在（**Wigner's friend** 思想实验）。

### 2.4.2 Decoherence（退相干）

环境时刻进行着"无意的测量"。原子处于动量本征态（位置的叠加 $|\psi\rangle=\sum_i\psi_i|x_i\rangle$）时，与气体分子、光子的局域相互作用（如 Lennard-Jones 势 $\sim r^{-6}$）把位置信息刻入环境：

$$\sum_i \psi_i\,|x_i\rangle_{\text{atom}}\otimes|x_i\rangle_{\text{environment}}$$

观察者无法追踪环境 ⟹ 原子退化为位置本征态的**统计混合**。这种因与环境作用而丧失相干性的过程称 **decoherence / dephasing**。

**Decoherence-preferred basis**：在与环境的相互作用中不发生纠缠（因而不退相干）的基。

- 运动自由度：相互作用是位置局域的 ⟹ 偏好**位置基**（所以制备确定位置的物体容易、确定动量的难；所以猫的死活叠加瞬间退相干——环境不停"测量"猫各部位的位置）。
- 微观内部自由度：偏好**能量本征基**。依据 **adiabatic theorem（Box 2.4，Born & Fock 1928）**：Hamiltonian 变化足够缓慢（$\frac{d}{dt}E_n \ll \hbar\Delta^2$，$\Delta$ 为最小能级间距）时，系统保持在能量本征态。碰撞"平滑"⟹ 能量本征态被保留，但其量子相位被不可预测地扰动 ⟹ 本征态之间的相干性丢失。这是原子分子总被观测到处于能量本征态的原因。

### 2.4.3 量子力学的诠释

纠缠一旦产生便不可避免地扩张（仪器→观察者→空气分子→……），最终囊括整个宇宙，形成巨型叠加。

- **Many-worlds interpretation（Everett 1957）**：塌缩不存在，叠加的所有分支同样实在（每个随机事件的每种结局都有其"宇宙"）。是量子理论的逻辑推论，但多宇宙的存在不可实验验证（一旦身处叠加便无法表征它）。其成立前提是量子力学普适——目前最大的叠加对象是数千原子的有机分子，寻找量子力学适用性的边界是重要的开放问题。
- **Copenhagen interpretation**：当叠加宏观化到无法测量分支间相位时，认为态已塌缩（"shut up and calculate"，实用主义）。本书后续采用 Copenhagen 语言，必要时引用 many-worlds 以求更深的视角。
- **Box 2.5 Schrödinger's cat（1935 原文）**：猫与放射性原子构成**纠缠**态 $\frac{1}{\sqrt2}(|\text{原子未衰变}\rangle|\text{猫活}\rangle + |\text{原子衰变}\rangle|\text{猫死}\rangle)$。从猫的主观视角，纠缠形成之刻叠加即已"塌缩"。
- 在 many-worlds 图像下重审炸弹佯谬：光子确实与炸弹发生了纠缠演化，"无相互作用"只是 "−" 分支中观察者的主观结论。

### 2.4.4 The superposition tree*（选读）

用"叠加树"论证：观察者反复测量 $\alpha|H\rangle+\beta|V\rangle$ 的多份拷贝，$n$ 次测量后叠加含 $2^n$ 项（不等幅时用多重分支技巧 $\alpha=\sqrt{m_H/(m_H+m_V)}$ 等化幅度）；用 Stirling 公式证明**绝大多数分支**中 $H$ 出现频率 $k/n \approx |\alpha|^2$，偏差 $\sim1/\sqrt n$ ⟹ **Born's rule 在绝大多数"宇宙"中成立**——测量公设可视为 Hilbert 空间公设 + unitary 演化的推论；但因实用上无法计算"宇宙波函数"，仍保留测量公设。

## 2.5 Quantum computation（概览）

$n$ 个 qubit 的叠加态同时编码 $2^n$ 组取值（如 $\sum a_{ijk}|ijk\rangle$），一次逻辑运算作用于所有分量——指数并行。但读出叠加只随机得到一项 ⟹ 并行性只对特定问题有效（如大数分解——威胁 public-key 密码，Shor 算法背景）。最大技术障碍：多体纠缠态对 decoherence 极端敏感（任一 qubit 与环境作用即毁掉整体相干性）。光子的优势：单光子能量（2–4 eV）对应数万开尔文 $\gg$ 环境温度，几乎不与环境作用。

- 逻辑编码：$|0\rangle\equiv|H\rangle$，$|1\rangle\equiv|V\rangle$。
- 单 qubit 门：NOT = HWP@$3\pi/8$（即 67.5°）；**Hadamard gate** $\hat H \simeq \frac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$ = HWP@$\pi/8$（22.5°）。
- 通用量子计算 = 单 qubit 门 + 一种双 qubit 门：**c-not gate**（control 为 $|1\rangle$ 时翻转 target；真值表即 XOR）。
- 构造：c-not = $(\hat 1\otimes\hat H_{\mathrm{Had}})\cdot\text{c-phase}\cdot(\hat 1\otimes\hat H_{\mathrm{Had}})$，其中 **c-phase gate** 只把 $|11\rangle$ 乘以 $-1$。c-phase 可由 Hamiltonian $\hat H = \hbar\omega|VV\rangle\langle VV|$ 作用 $t=\pi/\omega$ 实现——要求一个光子的折射率依赖于另一个光子的偏振，即**单光子级的非线性光学**，极难实现（普通介质中光波互不相互作用）。
- c-not/c-phase 能从可分态产生纠缠态（Ex. 2.65）；c-not 本身就是 $N=M=2$ 的 von Neumann 测量纠缠（Ex. 2.64）；有 c-not 即可实现 Bell 基测量（Ex. 2.66）。

## 2.6 Quantum teleportation 及其应用

### 2.6.1 量子隐形传态

任务：Alice 持有**未知**态 $|\chi\rangle = \alpha|H\rangle+\beta|V\rangle$（通道 1），想传给 Bob，但无量子信道。资源：与 Bob 共享 $|\Psi^-\rangle$（通道 2、3）+ 经典信道。

原理：把三光子态 $|\chi\rangle_1\otimes|\Psi^-\rangle_{23}$ 按通道 1,2 的 **Bell 基**重新展开——四项等幅。Alice 对通道 1,2 做 **Bell 测量**（四种结果各 ¼），Bob 的光子被投影到与 $|\chi\rangle$ 至多差一个 Pauli 操作的态（Table 2.3）：

| Alice 测得 | Bob 处的态 | Bob 的局域操作 |
|---|---|---|
| $\|\Phi^+\rangle$ | $-\beta\|H\rangle+\alpha\|V\rangle$ | $\hat\sigma_z\hat\sigma_x = i\hat\sigma_y$ |
| $\|\Phi^-\rangle$ | $\beta\|H\rangle+\alpha\|V\rangle$ | $\hat\sigma_x$ |
| $\|\Psi^+\rangle$ | $-\alpha\|H\rangle+\beta\|V\rangle$ | $\hat\sigma_z$ |
| $\|\Psi^-\rangle$ | $-(\alpha\|H\rangle+\beta\|V\rangle)$ | 无 |

Alice 经典信道告知结果（2 bit），Bob 施加相应 Pauli 即得 $|\chi\rangle$（100% 概率、完美保真度）。要点：

- 传送的是**量子态**而非物体；原本在 Alice 的 Bell 测量中被销毁（与 no-cloning 一致）。
- 四种结果概率恒为 ¼、与 $\alpha,\beta$ 无关 ⟹ 双方都不获知态的任何信息——这是完美传输的前提（若能边传边获取信息，结合 Ex. 2.44 将导致超光速通信）。
- 必需经典通信 ⟹ 不超光速。
- 实际困难：完整 Bell 测量与 c-not 同样困难；线性光学只能区分 4 个 Bell 态中的 2 个（Fig. 2.9 方案：PBS 交汇 + 双侧 diagonal 基测量，$|\Phi^\pm\rangle$ 由同侧两探测器同响并比较同/异区分，$|\Psi^\pm\rangle$ 落在同一盒中不可分）。

### Entanglement swapping（纠缠交换）

四光子初态 $|\Psi^-\rangle_{12}\otimes|\Psi^-\rangle_{34}$，对通道 2,3 做 Bell 测量 ⟹ 通道 1,4 变为纠缠态（具体是哪个 Bell 态取决于测量结果，Ex. 2.69）——**从未相遇的两个光子纠缠起来**（等价于把纠缠本身 teleport 出去）。

### 2.6.2 Quantum repeater（量子中继器）

目的：克服 Beer's law 指数损耗对 QKD 距离的限制（经典中继器需测量-再发送，等价于窃听者，不可用）。两块基石：**entanglement swapping + quantum memory**。

方案（Fig. 2.11）：把总距离分为若干段（每段几十 km）。每段两端各有一个 quantum memory cell：段内两个纠缠源各发一对光子，一个存入记忆、另一个送到段中央做 Bell 测量 ⟹ swapping 成功后该段两端记忆单元纠缠。**某段失败只需重试该段**，不破坏其他段已建立的纠缠（记忆保存）。所有段就绪后，对相邻记忆单元逐级做 Bell 测量，把纠缠交换至全线两端 ⟹ Alice–Bob 共享纠缠对，再用于 teleportation/QKD。直接传输要求光子全程不丢失（概率随距离指数衰减），repeater 的成功概率随距离衰减慢得多——数量级的优势。技术瓶颈：高性能量子光学存储器（长寿命、高保真读出）。

**第 2 章一句话**：纠缠 = 不可分解为张量积的非局域叠加；它使局域实在论破产（Bell：$|\langle S\rangle|=2\sqrt2>2$；GHZ：每次测量都矛盾），却因"局域统计不变"与因果律和平共处；测量本身就是纠缠的扩散（von Neumann 模型 + decoherence）；纠缠同时是 dense coding、teleportation、量子计算与量子中继的资源。

---

# 第 3 章 One-dimensional Motion，§3.1–3.3

把第 1 章的公理从离散基翻译到连续基——"把 mechanics 装回 quantum mechanics"。一维点粒子模型直接适用于原子中的电子等，是第 4 章三维运动的基础。

## 3.1 Continuous observables（连续可观测量）

位置 $\hat x$、动量 $\hat p$：本征态连续分布且彼此正交 ⟹ Hilbert 空间无穷维。

**Delta-normalization（核心新约定）**：

$$\langle x|x'\rangle = \delta(x-x'),\qquad \langle p|p'\rangle = \delta(p-p')$$

$\langle x|x\rangle = \delta(0) = \infty$ 与公设"物理态 norm=1"的矛盾如此化解：**连续可观测量的本征态是非物理的**——不可能把粒子置于绝对精确的位置或速度，$|x\rangle,|p\rangle$ 只是数学抽象；一切物理可实现的态都有位置和动量的展宽、norm 为 1。（Box 3.1：若改用有限维规则 $\langle x|x'\rangle=\delta_{xx'}$，则一切波函数恒为零——必须用 delta。严格处理需 rigged Hilbert space。）

**离散 → 连续翻译表（Table 3.1）**：

| | 离散基 $\{\|v_i\rangle\}$ | 连续基 $\{\|x\rangle\}$ |
|---|---|---|
| 正交归一 | $\langle v_i\|v_j\rangle=\delta_{ij}$ | $\langle x\|x'\rangle=\delta(x-x')$ |
| 态的分解 | $\|\psi\rangle=\sum_i\psi_i\|v_i\rangle$，$\psi_i=\langle v_i\|\psi\rangle$ | $\|\psi\rangle=\int_{-\infty}^{+\infty}\psi(x)\|x\rangle\,dx$，$\psi(x)=\langle x\|\psi\rangle$ |
| 测量公设 | $\mathrm{pr}_i=\|\langle v_i\|\psi\rangle\|^2$（概率） | $\mathrm{pr}(x)=\|\langle x\|\psi\rangle\|^2$（概率**密度**） |
| 算符分解 | $A_{ij}=\langle v_i\|\hat A\|v_j\rangle$ | $A(x,x')=\langle x\|\hat A\|x'\rangle$，$\hat A=\iint A(x,x')\|x\rangle\langle x'\|\,dx\,dx'$ |
| 单位算符 | $\hat 1=\sum_i\|v_i\rangle\langle v_i\|$ | $\hat 1=\int\|x\rangle\langle x\|\,dx$ |
| 算符乘积 | $(AB)_{ij}=\sum_k A_{ik}B_{kj}$ | $(AB)(x,x')=\int A(x,x'')B(x'',x')\,dx''$ |

- **Wavefunction（波函数）** $\psi(x) = \langle x|\psi\rangle$ 就是态向量在位置基下的"列向量"——没有更神秘的含义；$\langle\psi|$ 的波函数是 $\psi^*(x)$。
- 内积：$\langle\psi_1|\psi_2\rangle = \int_{-\infty}^{+\infty}\psi_1^*(x)\,\psi_2(x)\,dx$；物理态归一化 $\int|\psi(x)|^2dx = 1$。
- 算符：$\hat x = \int x\,|x\rangle\langle x|\,dx$；算符函数 $f(\hat x) = \int f(x)\,|x\rangle\langle x|\,dx$；$\hat x|x\rangle = x|x\rangle$。
- 作用规则：$\langle x|\hat A|\psi\rangle = \int A(x,x')\psi(x')\,dx'$；$(A^\dagger)(x,x') = A^*(x',x)$；$\langle\psi|f(\hat x)|\psi\rangle = \int|\psi(x)|^2 f(x)\,dx$。

**测量公设（连续版，Born's rule）**：单点概率无穷小，合法的概率度量是**概率密度**

$$\mathrm{pr}(x) = |\psi(x)|^2,\qquad \mathrm{pr}_{[x',x'']} = \int_{x'}^{x''} \mathrm{pr}(x)\,dx$$

（比例系数 1 由 $\int\mathrm{pr}(x)dx=1$ 与 $\langle\psi|\psi\rangle=1$ 比较确定。）期望与方差：

$$\langle x\rangle = \langle\psi|\hat x|\psi\rangle,\qquad \big\langle\Delta x^2\big\rangle = \langle\psi|\hat x^2|\psi\rangle - \langle\psi|\hat x|\psi\rangle^2$$

测后塌缩到严格 $|x\rangle$ 是非物理的理想化；现实装置使态塌缩到 $x$ 邻域内的窄分布。

## 3.2 De Broglie wave（德布罗意波）

**新公设**（不可由已有公设导出；源自 Planck→Einstein→Compton→de Broglie 的实验-理论链条）：

$$\boxed{\;\langle x|p\rangle = \frac{1}{\sqrt{2\pi\hbar}}\,e^{\,ipx/\hbar}\;}$$

动量本征态的波函数是无限延展的平面波——**de Broglie wave**。波粒二象性由此进入公理体系。

- **De Broglie 波长**：$\lambda_{dB} = \dfrac{2\pi\hbar}{p}$ ——与光子的 $p = 2\pi\hbar/\lambda$ 完全同形。
- 基的互相展开：
  $$|p\rangle = \frac{1}{\sqrt{2\pi\hbar}}\int_{-\infty}^{+\infty} e^{\,ipx/\hbar}\,|x\rangle\,dx,\qquad
  |x\rangle = \frac{1}{\sqrt{2\pi\hbar}}\int_{-\infty}^{+\infty} e^{-ipx/\hbar}\,|p\rangle\,dp$$
- 归一化因子 $1/\sqrt{2\pi\hbar}$ 由 $\langle p|p'\rangle = \delta(p-p')$ 固定（利用 $\int e^{i(p'-p)x/\hbar}dx = 2\pi\hbar\,\delta(p-p')$）。
- $|\langle x|p\rangle|^2 = 1/2\pi\hbar$ 处处相同：动量完全确定 ⟹ 位置完全不确定（不确定性原理的极限情形）；对全空间积分发散，再次说明 $|p\rangle$ 非物理。现实的态是动量本征态的叠加（波包），位置不确定度有限。
- **Wavenumber（波数）形式**：$k = p/\hbar$。由 $\delta(k-k') = \hbar\,\delta(p-p')$ 得
  $$|k\rangle = \sqrt{\hbar}\,|p=\hbar k\rangle,\qquad \langle x|k\rangle = \frac{1}{\sqrt{2\pi}}\,e^{ikx}$$
  （同一物理态、不同 norm——delta 归一化的又一副作用。）

**Box 3.2 历史**：Bohr（1913）量子化条件 $L=n\hbar$ 纯属经验；de Broglie（1924）把 $E=\hbar\omega$ 普适化到一切物质，并由 $2\pi r = n\lambda_{dB}$（轨道上驻波相长干涉）重新导出 Bohr 模型、给出与实验一致的原子光谱；Davisson–Germer（1927）镍晶格电子衍射直接证实电子的波动性。

## 3.3 Position and momentum bases（位置基与动量基）

### 3.3.1 基间转换

工具：单位算符分解 $\hat 1 = \int|x\rangle\langle x|\,dx = \int|p\rangle\langle p|\,dp$ 插入任意内积。**位置/动量表象互为 Fourier 变换**：

$$\psi(x) = \frac{1}{\sqrt{2\pi\hbar}}\int_{-\infty}^{+\infty} \tilde\psi(p)\,e^{\,ipx/\hbar}\,dp,\qquad
\tilde\psi(p) = \frac{1}{\sqrt{2\pi\hbar}}\int_{-\infty}^{+\infty} \psi(x)\,e^{-ipx/\hbar}\,dx$$

（波浪号表示动量/波数表象；波数版 $\psi(x) \leftrightarrow \tilde\psi(k)$ 正是标准 Fourier 变换对，且 $\tilde\psi(p) = \tilde\psi(k)/\sqrt\hbar$，$p=k\hbar$。）内积与表象无关：$\int\psi^*\varphi\,dx = \int\tilde\psi^*\tilde\varphi\,dp$（Parseval）。实波函数 $\psi(x)$ ⟹ $\mathrm{pr}(p) = \mathrm{pr}(-p)$、$\langle p\rangle = 0$。

**$\hat p = -i\hbar\,d/dx$ 的严格含义**：算符作用在态向量上、不作用在数（波函数）上。正确的陈述是（Ex. 3.19–3.22）：

$$\langle x|\hat p|x'\rangle = -i\hbar\,\frac{d}{dx}\,\delta(x-x'),\qquad
\langle x|\hat p|\psi\rangle = -i\hbar\,\frac{d}{dx}\psi(x),\qquad
\langle x|\hat p^2|\psi\rangle = -\hbar^2\,\frac{d^2}{dx^2}\psi(x)$$

即：态 $\hat p|\psi\rangle$ 的位置波函数是 $-i\hbar\,\psi'(x)$。对称地，在动量表象 $\langle p|\hat x|\psi\rangle = i\hbar\,\dfrac{d}{dp}\tilde\psi(p)$。位置算符函数在位置基是乘法算符：$V(x,x') = V(x)\,\delta(x-x')$；其动量表象 $V(p,p') = \frac{1}{2\pi\hbar}\int e^{\,i(p'-p)x/\hbar}\,V(x)\,dx$。

### 3.3.2 位置–动量不确定性

用微分表示直接计算（Ex. 3.23）：$\langle x|\hat x\hat p|\psi\rangle = -i\hbar x\psi'(x)$，$\langle x|\hat p\hat x|\psi\rangle = -i\hbar x\psi'(x) - i\hbar\psi(x)$，相减得

$$\boxed{\;[\hat x,\hat p] = i\hbar\;}$$

代入第 1 章的不确定性关系（对易子 $\propto\hat 1$ ⟹ 下界对一切态成立）：

$$\boxed{\;\big\langle\Delta x^2\big\rangle\big\langle\Delta p^2\big\rangle \ge \frac{\hbar^2}{4}\;}$$

——不可能制备位置与动量同时精确的粒子态。

**Gaussian wavepacket（标杆例子，Ex. 3.25）**：

$$\psi(x) = \frac{1}{(\pi d^2)^{1/4}}\,e^{\,ip_0x/\hbar}\,e^{-\frac{(x-a)^2}{2d^2}}
\;\xrightarrow{\ \mathcal F\ }\;
\tilde\psi(p) = \left(\frac{d^2}{\pi\hbar^2}\right)^{1/4} e^{-\frac{i(p-p_0)a}{\hbar}}\,e^{-\frac{(p-p_0)^2 d^2}{2\hbar^2}}$$

$$\langle x\rangle = a,\quad \langle p\rangle = p_0,\quad \big\langle\Delta x^2\big\rangle = \frac{d^2}{2},\quad \big\langle\Delta p^2\big\rangle = \frac{\hbar^2}{2d^2}
\;\Rightarrow\; \big\langle\Delta x^2\big\rangle\big\langle\Delta p^2\big\rangle = \frac{\hbar^2}{4}$$

Gaussian 恰好**饱和**不确定性下界，且是唯一饱和的态（Ex. 3.26）。直观：Fourier 变换下，位置波函数越窄，动量波函数越宽。但量子不确定性原理比 Fourier 性质更普遍——适用于任意不对易可观测量对。

**Box 3.3 位置与动量能"同时知道"吗？** Heisenberg 原始表述（"位置测得越准，动量知道得越不准"）有漏洞：制备 $|x=0\rangle$、自由演化 $t_0$ 后测位置得 $x_0$，则测量前瞬间的动量必为 $p_0 = Mx_0/t_0$——位置与动量**事后（post factum）同时确知**。这不与式 $(3.50)$ 矛盾：不确定性原理说的是测量结果的**随机性**（$x_0,p_0$ 事先完全不可预测），不禁止结果之间的**关联**；被禁止的是**事先制备**位置动量都确定的态。也不与 1.9.3 矛盾：那里说的是不存在对**每个**态都给出两个不对易可观测量信息的装置；这里只是对一个特意构造的态事后推断。

### 3.3.3 原版 Einstein–Podolsky–Rosen 佯谬（1935）

两粒子纠缠态（忽略归一化）：

$$\Psi(x_A,x_B) = \delta(x_A - x_B)
\quad\xrightarrow{\ \text{动量表象}\ }\quad
\tilde\Psi(p_A,p_B) = \delta(p_A + p_B)$$

两粒子位置严格相同（具体值完全随机）、动量严格相反。于是：

- Alice 测**位置**得 $x_0$ ⟹ Bob 的粒子被远程制备到 $|x_0\rangle$（位置确定、动量完全不定）；
- Alice 测**动量**得 $p_0$ ⟹ Bob 的粒子被制备到 $|-p_0\rangle$（动量确定、位置完全不定）。

Alice 通过选择测量类型，隔空在 Bob 处实现两种**互不相容的实在**之一——这正是 2.3.1 节 Bohm 版（$\hat\sigma_z$ vs $\hat\sigma_x$）的原型。$\delta$ 态非物理，但可用 Gaussian 态（位置近乎完全关联、动量近乎完全反关联）物理地逼近（3.10.3 的 two-mode squeezing 实现）。

**重要辨析**：原版 EPR **不**像 Bell 实验那样证明非局域性。对不相信不确定性原理的人，观测到的关联可以用局域隐变量解释："每对粒子产生时就带有相同（但随机）的位置和相反（但随机）的动量"。即原版 EPR 实验存在局域隐变量模型；真正排除局域实在论必须依靠 Bell 不等式的违反。

**§3.1–3.3 一句话**：连续基用 $\delta$ 归一化（本征态非物理）；波函数 $\psi(x)=\langle x|\psi\rangle$ 是态在位置基的坐标，$|\psi(x)|^2$ 是概率密度；公设 $\langle x|p\rangle = e^{ipx/\hbar}/\sqrt{2\pi\hbar}$ 把两个表象联成 Fourier 变换对，由此得 $[\hat x,\hat p]=i\hbar$ 与 $\Delta x\,\Delta p \ge \hbar/2$（Gaussian 饱和），并可写出连续版 EPR 态 $\delta(x_A-x_B)$。

---

## 三章总览

| | 第 1 章 | 第 2 章 | 第 3 章（§3.1–3.3） |
|---|---|---|---|
| 空间 | 2 维（偏振 qubit） | $2\times2=4$ 维（张量积） | 连续无穷维 |
| 核心公设 | Hilbert 空间、测量（Born rule）、演化（$e^{-i\hat Ht/\hbar}$） | （公设的张量积推广） | $\delta$ 归一化、$\langle x\|p\rangle\propto e^{ipx/\hbar}$ |
| 关键概念 | 叠加、相位、互补性、observable、不确定性原理 | 纠缠、局域测量、Bell/GHZ、decoherence、teleportation | 波函数、de Broglie 波、$[\hat x,\hat p]=i\hbar$、原版 EPR |
| 应用 | BB84 量子密码 | dense coding、量子计算、quantum repeater | （为 3.4 起的 Schrödinger 方程、势阱、谐振子铺路） |
