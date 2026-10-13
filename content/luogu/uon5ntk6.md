# 什么是状压
一种利用计算机二进制的性质来描述状态的DP方式。以 一个数的二进制位数上的$1,0$表示该数的取与不取。状压DP通常复杂度都大于$O(2^n)$ , 所以题目数据 $n$ 一般要小于 $18$。

# 状压的灵魂——位运算

 1. 判断一个数字 $x$ 二进制下第 $i$ 位是不是等于 $1$
 
`if(((1<<(i−1))&x))`
  
  2.   将一个数字x二进制下第i位更改成1
` x=x|(1<<(i−1))`

3. 将一个数字x二进制下第i位更改成0

`x=x&(x−1)`

4. 把一个数字二进制下最靠右的第一个1去掉
`x=x&(x−1)`

好的，你现在已经会状压了，所以快来学习基于状压的插头DP吧！！(  * ^ ▽ ^ * )

# 插头DP
插头DP ,也就是一类基于连通性的状态压缩动态规划。

## T1
给你一个 $m  n$ 的棋盘，有的格子是障碍，问共有多少条回路使得经过每个 非障碍格子恰好一次．$m, n ≤ 12$。

先思考一下暴力，因为是求最大回路，考虑状压DP，像旅行商问题那样求解，时间复杂度
$O(n^2*2^{n^2})$,最劣复杂度为$144*2^{144}$,肯定超时。

于是我们考虑一下特殊性质，这是一个棋盘。

引入一个概念，插头：**对于一个 4 连 通的问题来说，它通常有上下左右 4 个插头，一个方向的插头存在表示这个格子 在这个方向可以与外面相连。**

观察可以发现所有的非障碍 格子一定是从一个格子进来，另一个格子出去，即 4 个插头恰好有 2 个插头存在， 共 6 种情况。

那么我们可以逐格转移。

以每格划分状态，当前遍历到`[i,j]`,则过该点画一条轮廓线。

以轮廓线上的插头来表示这个状态，有两种表示方法来记录连通块。

以下图为例
 1. 最小表示法：`102021`
 2. 括号表示法：`101022`(就是一个连通块的左端点表示 $1$，右端点表示 $0$，)

![输入图片说明](/imgs/2023-06-14/GWJJkh23DPicwhTh.png)

一般都是使用括号标示法，为了加速，采用四进制。

## 转移有八种情况：

 1. `g[i][j]`为障碍物，且该点的下插头和右插头都没有，则可以进行转移
```cpp
	if(!g[i][j]){
		if(!pr&&!pd)insert(cur,state,w);
	}
```
2.`g[i][j]`不为障碍物，且该点没有两个插头，则插头方式一定在下方和右方。
修改后两个位置都有插头了，就要对状态进行修改，而且修改后两个插头一定是一个连通块的两端，一个为 $1$ ,一个为 $2$。
还需要判断下方和右方是不是障碍才能进行转移。
```cpp
	else if(!pr&&!pd){
		if(g[i+1][j]&&g[i][j+1]){
			insert(cur,state+ste(j-1,1)+ste(j,2),w);
		}
	}
```
3.没有右插头，只有下插头。
此时有两种情况：
			1:下插头直接向下，`j-1`连上了，`j`没有连上
			2.下插头向右拐弯，则状态表示不变。
```cpp
	else if(!pr&&pd){
		if(g[i][j+1])insert(cur,state,w);
		if(g[i+1][j])insert(cur,state+ste(j-1,y)-ste(j,y),w);
	}
```
4.没有下插头，只有右插头。
同理
```cpp
	else if(!pd&&pr) {
        if(g[i][j + 1]) insert(cur,state-ste(j-1,pr)+ste(j,pr),w);
        if(g[i + 1][j]) insert(cur,state,w);
    }
```
5.下插头，右插头都是两个连通块的左端点。

转移后，两个左端点去掉，一个右端点变为左端点。
```cpp
		else if(pr==1&&pd==1){
	        int sum=1;
            up(pos,j+1,m){
          		int x=get(state,pos);
           		if(x==1)sum++;
           		else if(x==2){
          		if(--s==0){
    				insert(cur,state-ste(j-1,1)-ste(j,1)-ste(pos,1),w);
               		break;
				}
			}
        } 

```
6.下插头，右插头都是两个连通块的右端点。
同理：
```cpp
				else if(pr==2&&pd==2){
                	int sum=1;
                	dn(pos,j-2,0){
                		int x=get(state,pos);
                		if(x==2)sum++;
                		else if(x==1){
                			if(--s==0){
                				insert(cur,state-ste(j-1,2)-ste(j,2)+ste(pos,1),w);
                				break;
							}
						}
					}
                }
```

7.右插头为右端点，下插头为左端点。

连通块直接合在一起。
```cpp
		else if(pr==2&&pd==1) {
            insert(cur,state-ste(j-1,2)-ste(j, 1),w);
        }
```
8.右插头为右端点，下插头为左端点，只当进行到最后一个点时才可能出现。

统计答案。

## 细节

1.换行的时候，将上一行左移一位，因为是四进制，所以左移两位。

```cpp
	up(j,1,cnt[cur])h[cur][q[cur][j]]<<=2;
```
2.滚动数组的处理
```cpp
			int last=cur;cur^=1;
			cnt[cur]=0;
			memset(h[cur],-1,sizeof h[cur]);
```
3.取四进制的第 $k$位

```cpp
inline int get(int state,int k){
	return (state>>(k*2))&3;
}
```
4.第k位加一

```cpp
inline int ste(int k,int v){
	return v*(1<<(k*2));
}
```
5.hash
```cpp
inline int find(int cur,int x){
	int t=x%mod;
	while(h[cur][t]!=-1&&h[cur][t]!=x){
		if(++t==mod)t=0;
	}
	return t;
}
```
## code

```cpp

#include <bits/stdc++.h>

using namespace std;

#define int __int128
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define ls k<<1
#define rs k<<1|1

const int N=1e5+7;
const int mod=590027;

namespace IO{
	inline int read(){
		char c=getchar();int x=0,fh=0;
        while(c<'0'||c>'9'){fh|=c=='-';c=getchar();}
        while(c>='0'&&c<='9'){x=(x<<1)+(x<<3)+(c^48);c=getchar();}
        return fh?-x:x;
	}
	inline void wt(i128 x){
		if(x<0){x=-x;putchar('-');}
		if(x>9)wt(x/10);
		putchar((x%10)^48);
	}
	inline void write(i128 x,bool op){
		wt(x);
		putchar(op?'\n':' ');
	}
}using namespace IO;
int n,m,endx,endy;
char s[50][50];
int g[50][50],ans;
int h[2][N],cnt[2],q[2][N],dp[2][N];
inline int find(int cur,int x){
	int t=x%mod;
	while(h[cur][t]!=-1&&h[cur][t]!=x){
		if(++t==mod)t=0;
	}
	return t;
}
inline void insert(int cur,int state,int w){
	int t=find(cur,state);
	if(h[cur][t]==-1){
		h[cur][t]=state;
		dp[cur][t]=w;
		q[cur][++cnt[cur]]=t;
	}
	else dp[cur][t]+=w;
}
inline int get(int state,int k){
	return (state>>(k*2))&3;
}
inline int ste(int k,int v){
	return v*(1<<(k*2));
}
signed main(){
	n=read();m=read();
	up(i,1,n){
		scanf("%s",s[i]+1);
		up(j,1,m){
			if(s[i][j]=='.'){
				g[i][j]=1;
				endx=i;endy=j;	
			}
		}
	}
	int cur=0;
	memset(h,-1,sizeof h);
	insert(cur,0,1);
	up(i,1,n){
		up(j,1,cnt[cur])h[cur][q[cur][j]]<<=2;
		up(j,1,m){
			int last=cur;cur^=1;
			cnt[cur]=0;
			memset(h[cur],-1,sizeof h[cur]);
			up(k,1,cnt[last]){
				int state=h[last][q[last][k]],w=dp[last][q[last][k]];
				int pr=get(state,j-1),pd=get(state,j);
				if(!g[i][j]){
					if(!pr&&!pd)insert(cur,state,w);
				}
				else if(!pr&&!pd){
					if(g[i+1][j]&&g[i][j+1]){
						insert(cur,state+ste(j-1,1)+ste(j,2),w);
					}
				}
				else if(!pr&&pd){
					if(g[i][j+1])insert(cur,state,w);
					if(g[i+1][j])insert(cur,state+ste(j-1,pd)-ste(j,pd),w);
				}
                else if(!pd&&pr) {
                    if(g[i][j + 1]) insert(cur,state-ste(j-1,pr)+ste(j,pr),w);
                    if(g[i + 1][j]) insert(cur,state,w);
                }
                else if(pr==1&&pd==1){
                	int sum=1;
                	up(pos,j+1,m){
                		int x=get(state,pos);
                		if(x==1)sum++;
                		else if(x==2){
                			if(--sum==0){
                				insert(cur,state-ste(j-1,1)-ste(j,1)-ste(pos,1),w);
                				break;
							}
						}
					}
                }
				else if(pr==2&&pd==2){
                	int sum=1;
                	dn(pos,j-2,1){
                		int x=get(state,pos);
                		if(x==2)sum++;
                		else if(x==1){
                			if(--sum==0){
                				insert(cur,state-ste(j-1,2)-ste(j,2)+ste(pos,1),w);
                				break;
							}
						}
					}
                }
                else if(pr==2&&pd==1) {
                    insert(cur,state-ste(j-1,2)-ste(j, 1),w);
                }
                else if(i==endx&&j==endy){
                	ans+=w;
				}
			}
		}
	}
	write(ans,1);
	return 0;
}

/*
 ふわふわ♪
*/
```