import numpy as np
import matplotlib.pyplot as plt

# === 输入数据 ===
W = np.array([0.000043,
0.000054,
0.000102,
0.0001501,
0.0002796
])
V_over_sqrtF = np.array([
    14.03386093,
    19.3035452,
    28.88135837,
    50.71613195,
    141.1731262
])

# === 一百分之一误差 (5%)，用于绘制 y 方向误差条 ===
yerr = 0.05 * W  # 5% of each W

# --- 无权拟合（ordinary least squares） ---
m_unw, b_unw = np.polyfit(V_over_sqrtF, W, 1)
y_pred_unw = m_unw * V_over_sqrtF + b_unw

# R^2 （基于无权残差）
ss_res = np.sum((W - y_pred_unw)**2)
ss_tot = np.sum((W - np.mean(W))**2)
R2_unw = 1 - ss_res/ss_tot

# --- 加权拟合（使用 1/sigma 权重）；并取得协方差以估计参数不确定度 ---
weights = 1.0 / yerr  # np.polyfit 的 w 参数是权重（越大表示该点越重要）
try:
    coeffs_w, cov = np.polyfit(V_over_sqrtF, W, 1, w=weights, cov=True)
    m_w, b_w = coeffs_w
    slope_err = np.sqrt(cov[0,0])
    intercept_err = np.sqrt(cov[1,1])
except TypeError:
    # 兼容性回退（若 numpy 版本不支持 cov=True）
    coeffs_w = np.polyfit(V_over_sqrtF, W, 1, w=weights)
    m_w, b_w = coeffs_w
    cov = None
    slope_err = np.nan
    intercept_err = np.nan

xs = np.linspace(V_over_sqrtF.min(), V_over_sqrtF.max(), 500)
ys_unw = m_unw * xs + b_unw
ys_w = m_w * xs + b_w

# === 绘图：带误差条 & 两条拟合线 ===
plt.figure(figsize=(8,5))
plt.errorbar(V_over_sqrtF, W, yerr=yerr, fmt='o', capsize=4, label='data (5% error bars)', zorder=3)
plt.plot(xs, ys_unw, '-', label=f'OLS fit: W = {m_unw:.3e}·x + {b_unw:.3e}\n$R^2$={R2_unw:.4f}', zorder=2)
if not np.isnan(slope_err):
    plt.plot(xs, ys_w, '--', label=f'Weighted fit: W = {m_w:.3e}·x + {b_w:.3e}\n slope={m_w:.3e}±{slope_err:.3e}', zorder=2)
else:
    plt.plot(xs, ys_w, '--', label=f'Weighted fit: W = {m_w:.3e}·x + {b_w:.3e}', zorder=2)

plt.xlabel("1/D-1/D+L  (m^-1)")
plt.ylabel("Fc / N")
plt.title("Fc vs Fc / 1/D-1/D+L with 5% error bars and fits")
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend()
plt.tight_layout()
plt.show()
