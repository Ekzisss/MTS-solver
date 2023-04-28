import matplotlib.pyplot as plt
import numpy as np
import math as mt
import csv
import json
import os

#данные

if (os.path.exists('data.json') and os.stat('data.json').st_size != 0):
  f = open('data.json')
  data = json.load(f)
  print(type(data))
  Rho_1, Rho_2, Rho_3, st_H, st_L, H1, L1, Fi1, Fi2, T1, Q, M = data
  Rho_1 = int(Rho_1)
  Rho_2 = int(Rho_2)
  Rho_3 = int(Rho_3)
  st_H = int(st_H)
  st_L = int(st_L)
  H1 = int(H1)
  L1 = int(L1)
  Fi1 = float(Fi1)
  Fi2 = float(Fi2)
  T1 = float(T1)
  Q = float(Q)

  N = int(H1)

  M = int(M)
else:
  Rho_1= 100
  Rho_2= 300
  Rho_3= 500
  st_H=500 #шаг в глубину
  st_L=500 #шаг в длинну
  H1 =15 #глубина 
  L1 = 15 #длина
  Fi1 =22.5
  Fi2 =22.5

  N = H1 # число слоев
  T1 = 0.001 #начальный период
  Q = 2 #геометричкский шаг по периоду
  M = 20 #число периодов

#генератор
#запалнение матрицы ро2
mat=np.empty([H1,L1],dtype=int)
for i in range (H1):
    for j in range(L1):
        mat[i,j]=Rho_2
#запись матрицы

#создание вектора глубины
deep_1=[]
de1=0
for i in range (H1):

    deep_1.append(de1)
    de1 = de1+st_H

# создание вектора длинны
long=[]
lg1=0
for i in range (L1):

    long.append(lg1)
    lg1 = lg1 + st_L


# запалнение матрицы ро1
temp = mt.tan(mt.radians(Fi1))
for i in range (L1):
    de2=temp * (long[i] + long[1]) * (H1/L1)
    for q in range(H1):
        if de2 >= deep_1[q]:
            mat[q,i]=Rho_1


# запалнение матрицы ро3
deep_2=[]
deep_2=deep_1[::-1]
temp = mt.tan(mt.radians(Fi2))
for i in range (L1):
    de3 = temp * (long[i] + long[1]) * (H1/L1)
    for q in range(H1):
        if de3 >= deep_2[q]:
            mat[q,i]=Rho_3

import csv
with open('matrix.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(mat)

#визуализация разреза

plt.style.use('dark_background')

fig=plt.figure()
ax=fig.add_subplot()
gr=ax.imshow(np.log10(mat),cmap='jet',interpolation='bilinear',aspect='auto')
clbr = plt.colorbar(gr)
clbr.set_label(r'lg($\rho$[Ом·м])',fontsize=20, color="w")
ax.set_xlabel('Y, км', color="w")
ax.set_ylabel('Z, км', color="w")
# posy=np.arange(L1)
# posz=np.arange(H1)
# ax.set_xticks(posy, color="r")
# ax.set_yticks(posz, color="r")
ax.tick_params(labelcolor='tab:orange')
plt.style.use('dark_background')

# plt.savefig('img/heatmap.png', dpi=150, transparent=True)
# plt.savefig('resources/app/img/heatmap.png', dpi=150, transparent=True)
# plt.show()

#расчет графиков

Rk_all=np.empty([M,L1],dtype=float)
T=np.array([Q**i*T1 for i  in range(M)])
Omega=np.array((2*np.pi)/T)
Fi_all=np.empty([M,L1],dtype=float)
#расчет ПЗ в каждой точке

print(T)

u = 4 * np.pi * 10 ** (-7)
for temp in range(L1):
    for i,w in enumerate(Omega):
        Rc=1
        for m in reversed(range(N-1)):

            K = np.sqrt((-1j  * w * u)/mat[m,temp])
            A = np.sqrt(mat[m,temp]/mat[m+1,temp])
            B = np.exp(-2*K*st_L)*((Rc-A)/(Rc+A))
            Rc= (1+B)/(1-B)

        Rk_all[i,temp]=np.abs(Rc)**2*mat[0,temp]
        Fi_all[i, temp] = mt.degrees(np.angle(Rc) - np.pi / 4)


# print(list(map(mt.degrees(Fi_all))))
# print(Fi_all)
#визуализация

fig = plt.figure(figsize=(9, 5))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
plt.subplots_adjust(
                    wspace=0.4,
                    hspace=0.4)
ax1.set_yscale('log')
ax1.set_xlim(0, long[L1-1])
ax2.set_xlim(0, long[L1-1])
for temp_2 in  range (len(Rk_all)):
    ax1.plot(long,Rk_all[temp_2,:], label=f'{temp_2}')
for temp_2 in  range (len(Fi_all)):
    ax2.plot(long,Fi_all[temp_2,:], label=f'{temp_2}')
ax1.grid()
ax2.grid()

ax1.set_xlabel(r'Y, м')
ax1.set_ylabel(r'$\rho_T$')

ax2.set_xlabel(r'Y, м')
ax2.set_ylabel(r'$\varphi_Z$')

pos = ax1.get_position()
ax1.set_position([pos.x0, pos.y0, pos.width * 0.8, pos.height])
pos = ax2.get_position()
ax2.set_position([pos.x0, pos.y0, pos.width * 0.8, pos.height])


plt.legend(title='Graph:',loc='center right', bbox_to_anchor=(1.35, 1.5), ncol=2)

# plt.legend(loc='center right',title='Graph:')


# plt.savefig('img/graphs.png', dpi=150, transparent=True)
# plt.savefig('resources/app/img/graphs.png', dpi=150, transparent=True)
# plt.show()


# heatmap rk

plt.style.use('dark_background')

fig=plt.figure()
ax=fig.add_subplot()
gr=ax.imshow(np.log10(Rk_all),cmap='jet',interpolation='bilinear',aspect='auto')
clbr = plt.colorbar(gr)
clbr.set_label(r'lg($\rho$[Ом·м])',fontsize=20, color="w")
ax.set_xlabel('Y, км', color="w")
ax.set_ylabel('T, с', color="w")

ax.tick_params(labelcolor='tab:orange')
plt.style.use('dark_background')

# plt.savefig('img/heatmap2.png', dpi=150, transparent=True)
# plt.savefig('resources/app/img/heatmap2.png', dpi=150, transparent=True)

# plt.show()

# heatmap fi

plt.style.use('dark_background')

fig=plt.figure()
ax=fig.add_subplot()
gr=ax.imshow(Fi_all,cmap='jet',interpolation='bilinear',aspect='auto')
clbr = plt.colorbar(gr)
clbr.set_label('Градусы',fontsize=20, color="w")
ax.set_xlabel('Y, км', color="w")
ax.set_ylabel('T, с', color="w")

ax.tick_params(labelcolor='tab:orange')
plt.style.use('dark_background')
ax.set_ylim(T[0], T[len(T)-1])

# plt.savefig('img/heatmap3.png', dpi=150, transparent=True)
# plt.savefig('resources/app/img/heatmap3.png', dpi=150, transparent=True)

plt.show()