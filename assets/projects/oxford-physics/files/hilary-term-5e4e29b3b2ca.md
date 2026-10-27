# 物理

## 1) 力学

这一块从 Lecture 11 开始，主线是：变量质量、非惯性系、带电粒子受力、角动量/力矩、中心力轨道、刚体转动、拉格朗日力学。

* **牛顿第二定律**：
  $$
  \mathbf F=\frac{d\mathbf p}{dt},\qquad \mathbf p=m\mathbf v
  $$
  质心运动只看外力：
  $$
  \mathbf r_{\rm cm}=\frac{\sum_i m_i\mathbf r_i}{\sum_i m_i},\qquad
  \mathbf v_{\rm cm}=\frac{\sum_i m_i\mathbf v_i}{\sum_i m_i}
  $$
  $$
  \sum_i m_i\mathbf a_i=\sum \mathbf F_{\rm ext}
  $$
  在质心系里，总动量为 0。

* **质心系动能分解**：
  $$
  T_{\rm lab}=T_{\rm CM}+\frac12 Mv_{\rm CM}^2
  $$
  其中 $M=\sum_i m_i$。

* **火箭/变质量**：
  讲义把“吸质量、喷质量、火箭方程、非惯性系”单独列成 Lecture 11–12。常用结果记成：
  $$
  \Delta v = w\ln\frac{m_i}{m_f}
  $$
  这里 $w$ 是喷气相对速度。

* **力矩与角动量**：
  $$
  \boldsymbol{\tau}=\mathbf r\times\mathbf F,\qquad
  \mathbf J=\mathbf r\times\mathbf p,\qquad
  \frac{d\mathbf J}{dt}=\boldsymbol{\tau}
  $$
  若是中心力，$\boldsymbol{\tau}=0$，所以角动量守恒。

* **碰撞**：
  动量守恒是主线；完全弹性碰撞在质心系里最简单，速度大小不变、方向反向。恢复系数
  $$
  e=\frac{|v_2-v_1|}{|u_1-u_2|}
  $$
  且讲义给出
  $$
  e=\sqrt{1-\frac{\Delta E}{T^{\rm i}_{\rm CM}}}
  $$
  完全非弹性时 $e=0$。

* **刚体转动**：
  $$
  I=\sum_i m_ir_i^2
  $$
  平行轴定理：
  $$
  I=I_{\rm CM}+Md^2
  $$
  垂直轴定理（薄平面物体）：
  $$
  I_z=I_x+I_y
  $$
  滚动不打滑：
  $$
  v=\omega R
  $$
  总能量常写成“平动 + 转动 + 重力势能”。

* **拉格朗日力学**：
  $$
  L=T-U
  $$
  欧拉–拉格朗日方程：
  $$
  \frac{d}{dt}\frac{\partial L}{\partial \dot q_i}-\frac{\partial L}{\partial q_i}=0
  $$
  循环坐标对应的共轭动量守恒；对称性对应守恒量。

## 2) 电磁学

电磁学整套结构是：静电 → 磁静 → 感应 → 电感/变压器 → 麦克斯韦方程。

* **电场与电势**：
  $$
  \mathbf E=\frac{\mathbf F}{q},\qquad
  \mathbf E=\frac{Q}{4\pi\varepsilon_0 r^2}\hat{\mathbf r}
  $$
  $$
  V(B)-V(A)=-\int_A^B \mathbf E\cdot d\mathbf l,\qquad
  \mathbf E=-\nabla V
  $$
  点电荷势：
  $$
  V=\frac{Q}{4\pi\varepsilon_0 r}
  $$
  叠加原理成立。

* **高斯定律**：
  $$
  \oint_S \mathbf E\cdot d\mathbf a=\frac{Q_{\rm encl}}{\varepsilon_0},
  \qquad
  \nabla\cdot\mathbf E=\frac{\rho}{\varepsilon_0}
  $$
  没有对称性就别乱硬套。

* **偶极子**：
  $$
  \mathbf p=q\mathbf d
  $$
  远场电势：
  $$
  V=\frac{\mathbf p\cdot\hat{\mathbf r}}{4\pi\varepsilon_0 r^2}
  =\frac{p\cos\theta}{4\pi\varepsilon_0 r^2}
  $$
  这是电多极展开最常见的一层。

* **磁场与安培定律**：
  $$
  d\mathbf B=\frac{\mu_0 I\,d\mathbf l\times\hat{\mathbf r}}{4\pi r^2}
  $$
  $$
  \oint \mathbf B\cdot d\mathbf l=\mu_0 I_{\rm encl},
  \qquad
  \nabla\cdot\mathbf B=0
  $$
  磁单极子不存在。

* **洛伦兹力**：
  $$
  \mathbf F=q(\mathbf E+\mathbf v\times\mathbf B)
  $$
  纯磁场不做功，只有改变方向，不改速率。

* **法拉第定律与楞次定律**：
  $$
  \mathcal E=-\frac{d\Phi}{dt},\qquad
  \Phi=\int_S \mathbf B\cdot d\mathbf a
  $$
  微分形式：
  $$
  \nabla\times\mathbf E=-\frac{\partial\mathbf B}{\partial t}
  $$
  感应方向总是反抗磁通变化。

* **自感/互感**：
  $$
  \mathcal E=-L\frac{dI}{dt},\qquad
  U=\frac12 LI^2
  $$
  $$
  M_{12}=M_{21},\qquad
  \mathcal E_2=-M\frac{dI_1}{dt}
  $$
  变压器理想关系：
  $$
  \frac{V_S}{V_P}=k\frac{N_S}{N_P},\qquad
  V_P I_P=V_S I_S\ (\text{理想})
  $$

* **麦克斯韦方程（真空/静态版本最该背）**：
  $$
  \nabla\cdot\mathbf E=\frac{\rho}{\varepsilon_0},\quad
  \nabla\cdot\mathbf B=0,\quad
  \nabla\times\mathbf E=-\frac{\partial\mathbf B}{\partial t},\quad
  \nabla\times\mathbf B=\mu_0\mathbf J+\mu_0\varepsilon_0\frac{\partial\mathbf E}{\partial t}
  $$
  这是整门电磁学的总纲。



---

# 数学

**一、波动 / 正常模：先背这组骨架**
简谐振动是底层模板：$\ddot x+\omega^2 x=0$，解写成 $x=A\cos(\omega t+\phi)$ 或 $x=A\sin(\omega t+\phi)$。波里最常见的单色平面波写法是 $y(x,t)=A\cos(\omega t-kx)$；其中 $k=2\pi/\lambda$、$\omega=2\pi/T$、$\nu=1/T$，相速度 $v_p=\omega/k=\nu\lambda$。这是整套波动题的起点。

**二、驻波 / 模态：固定端一定要会**
固定两端的弦，正常模写成
$$
y_n(x,t)=A_n\sin\left(\frac{n\pi x}{L}\right)\cos\left(\frac{n\pi vt}{L}\right),
\qquad
\omega_n=\frac{n\pi v}{L}.
$$
单个模态的能量也要记：
$$
E_n=K_n+U_n=\frac{\rho L A_n^2\omega_n^2}{4}.
$$
如果题目问“为什么只有离散频率”，答案就是边界条件把波长锁死了。

**三、反射 / 阻抗 / 透射：三条最常考**
传输线和波的边界问题里，特征阻抗 $Z_0$ 和终端阻抗 $Z_T$ 很关键，反射系数
$$
r=\frac{A_0}{A}=\frac{Z_T-Z_0}{Z_T+Z_0}.
$$
三个极限要秒反应：$Z_T\to 0\Rightarrow r=-1$（固定端，反相）；$Z_T=Z_0\Rightarrow r=0$（无反射，完全匹配）；$Z_T\to\infty\Rightarrow r=1$（自由端，同相）。

**四、色散 / 群速度：分清“谁在跑”**
相速度是单个正弦波的速度：
$$
v_p=\frac{\omega}{k}.
$$
群速度是波包、也就是信息包络的速度：
$$
v_g=\frac{d\omega}{dk}.
$$
有色散时，波包会展宽，$v_g$ 和 $v_p$ 一般不一样。考试里只要看到 wave packet / dispersion / information transfer，先把这两条写出来。

**五、光学波动如果也一起考：只背一个衍射栅公式**
波动光学提纲里，最常见的是“两波干涉、N 波干涉、衍射”。如果题目落到光栅，主极大条件直接记：
$$
\sin\theta=\frac{m\lambda}{a},\qquad m\in\mathbb N.
$$
另外，光在介质中的相速度和折射率关系是
$$
n=\frac{c}{v},\qquad n=\frac{\lambda_0}{\lambda}.
$$
这两组就够你应付大多数基础光学波动题。

**六、数学：偏导 / 全微分 / 链式法则**
多元函数先抓偏导：把别的变量当常数。全微分写成
$$
df=\frac{\partial f}{\partial x}dx+\frac{\partial f}{\partial y}dy+\cdots
$$
链式法则在换变量题里必出；Jacobian 是换元时的面积/体积缩放因子，做多重积分时一定会出现。讲义的主线就是：多元函数、极限与连续、偏导、方向导数、全微分、链式法则、Jacobian。

**七、数学：grad / div / curl 这组三件套**
三维向量分析最重要的三条是
$$
\nabla f=\text{grad }f,\qquad
\nabla\cdot \mathbf A=\text{div }\mathbf A,\qquad
\nabla\times \mathbf A=\text{curl }\mathbf A.
$$
必须背的恒等式：
$$
\nabla\times(\nabla f)=0,\qquad
\nabla\cdot(\nabla\times \mathbf A)=0.
$$
直觉上：grad 指向增长最快方向，div 看源汇，curl 看旋转。这个在电磁学里也会直接用到。

**八、数学：高斯定理和斯托克斯定理，背边界关系**
你只要记住两句：
$$
\iiint_V (\nabla\cdot \mathbf A)\,dV=\iint_{\partial V}\mathbf A\cdot d\mathbf S
$$
和
$$
\iint_S (\nabla\times \mathbf A)\cdot d\mathbf S=\oint_{\partial S}\mathbf A\cdot d\mathbf l.
$$
一句话概括：**散度管体积通量，旋度管边界环流**。这两条是电磁学积分形式的骨架。
