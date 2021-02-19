
from weight_sizing import weight_sizing

# Check file for weight_sizing function
W_press = 8     # psia
H_tv = 0.0
AR = 1
B_w = 1
D = 1
H_tv = 1
L = 1
L_m = 1
L_n = 1
L_t = 1
N_eng = 1
N_l = 1
N_z = 1
q = 1
S_f = 1
S_ht = 1
S_vt = 1
S_w = 1
t_c = 1
W_dg = 1
W_eng = 1
W_fw = 1
W_l = 1
W_press = 1
W_uav = 1
Lamb = 1
Lamb_ht = 1
Lamb_vt = 1
lamb = 1
lamb_ht = 1
lamb_vt = 1

W_av, W_eng_total, W_f, W_fc, W_furnish, W_ht, W_lg, W_vt, W_w = weight_sizing(AR, B_w, D, H_tv, L, L_m, L_n, L_t, N_eng, N_l, N_z, q,
                  S_f, S_ht, S_vt, S_w, t_c, W_dg, W_eng, W_fw, W_l, W_press, W_uav,
                  Lamb, Lamb_ht, Lamb_vt, lamb, lamb_ht, lamb_vt)

W_total = W_av + W_eng_total + W_f + W_fc + W_furnish + W_ht + W_lg + W_vt + W_w

print(W_total)