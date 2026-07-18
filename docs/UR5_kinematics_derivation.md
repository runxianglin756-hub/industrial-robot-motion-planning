1. UR5 DH Parameters
| Joint | a   | alpha | d  | theta |
| ----- | --- | ----- | -- | ----- |
| 1     | 0   | π/2   | d1 | q1    |
| 2     | -a2 | 0     | 0  | q2    |
| 3     | -a3 | 0     | 0  | q3    |
| 4     | 0   | π/2   | d4 | q4    |
| 5     | 0   | -π/2  | d5 | q5    |
| 6     | 0   | 0     | d6 | q6    |

2. Forward Kinematics

A_i = Rot(z,theta_i)
      Trans(z,d_i)
      Trans(x,a_i)
      Rot(x,alpha_i)

T06=A1A2A3A4A5A6

3. Inverse Kinematics

Jacobian pseudo inverse method
q(k+1)=q(k)+J⁺(xd-x)

其中：

J⁺为Jacobian伪逆

停止条件：

||xd-x|| < ε
