# 动态规划

### 性质：
$1.$无后效性

$2.$最优子结构

$3.$有向图

$4.$重叠子问题

### 步骤：

$1.$阶段划分

$2.$状态设计

$3.$转移方程

$4.$初值

### 状态设计

最简单的方法就是把搜索记录的所有信息全放在状态里，再来考虑优化

$problem.1$

给出一个正整数序列$x_1,x_2,...x_n$要求将其分为若干连续段，设每一段的x_i 的和分别为$s_1,s_2,...s_m$，要求最小化$\sum_{i=1}^m(as_i^2+bs_i+c)$

$n\le2000,1<x_i\le100,1\le a\le5,|b|,|c|\le10^8$

$1.O(n^2)$

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
#define inf 1e14
#define mod 1000000007
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,m,x[500500],a,b,c,sum[500500],f[500500];
signed main() {
	n=read();m=read();
	a=read();b=read();c=read();
	for(int i=1;i<=n;i++){
		x[i]=read();
		sum[i]=sum[i-1]+x[i];	
	}
	memset(f,0x3f,sizeof f);
	for(int i=1;i<=n;i++){
		for(int j=0;j<=i-1;j++){
			f[i]=min(f[i],f[i]+a*(sum[i]-sum[j])*(sum[i]-sum[j])+b*(sum[i]-sum[j])+c);
		}
	}
	cout<<f[n]<<endl;
	return 0;
}
```

$2.O(nlogn)$

```cpp
鸽
```

## 区间DP

[$problem.2$](https://www.luogu.com.cn/problem/P1880)

1.$O(n^3)$

```cpp
#include <bits/stdc++.h>
using namespace std;
int a, s[10050], f[5005][5050],g[1000][1000],num[1000];
int main() {
	int n;
	//memset(f, 127 / 3, sizeof(f));
	scanf("%d", &n);
	for (int i = 1; i <= 2*n; i++) {
		scanf("%d", &num[i]);
		num[i+n]=num[i];
		s[i] = s[i - 1] + num[i];
	}
	for (int i = 1; i <= n; i++) {
		f[i][i] = 0;
	}
	for (int l = 1; l < n; l++) {
		for (int i = 1, j = i + l; i < n*2 && j <2*n; i++, j = i + l) {
			f[i][j] = 0x3f3f3f3f;
			for (int k = i; k < j; k++) {
				f[i][j] = min(f[i][j], f[i][k] + f[k + 1][j] + s[j] - s[i - 1]);
				g[i][j]=max(g[i][j],g[i][k]+g[k+1][j]+s[j]-s[i-1]);	
			}
		}
	}
	int maxl,minl=0x3f3f3f3f;
	for(int i=1;i<=n;i++){
		maxl=max(maxl,g[i][i+n-1]);
		minl=min(minl,f[i][i+n-1]);
	}
	printf("%d\n%d", minl,maxl);
	return 0;
}
```
四边形不等式优化：$O(n^2)$

```cpp
鸽
```

[$problem.3$](https://www.luogu.com.cn/problem/P1040)

提示：以$x$为根的子树在中序遍历中显然是连续的，设为$[l,r]$,且若左子
树有$k$个点，则左子树在中序遍历中的位置为$[l,l+k-1]$，则右
子树为 $[l+k+1,,r]$，x为中序遍历第l+k个点

即$f_{l,r}=\max_{k=l}^{k\le r}({f_{l,k-1}* f{_{k+1,r}+d_{k}}})$

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
#define inf 1e14
#define mod 1000000007
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,tr[2077][2077],path[2077][2077];
void showpath(int l,int r){
	if(l > r)return;
	printf("%lld ", path[l][r]);
	if (l == r)return;
	showpath(l,path[l][r] - 1);
	showpath(path[l][r]+1,r);
}
signed main(){
	n=read();
	for(int i=1;i<=n;i++){
		tr[i][i]=read();
		tr[i][i-1]=1;
		path[i][i]=i;
	}
	for(int len=1;len<n;len++) {
		for(int l=1;l+len<=n;l++) {
			int r = l + len;
			tr[l][r] = tr[l + 1][r] + tr[l][l];
			path[l][r]=l;
			for (int k=l+1;k<r;k++) {
				if (tr[l][r] < tr[l][k - 1] * tr[k + 1][r] + tr[k][k]) {
					tr[l][r] = tr[l][k - 1] * tr[k + 1][r] + tr[k][k];
					path[l][r]=k;
				}
			}
		}
	}
	cout<<tr[1][n]<<endl;
	showpath(1,n);
	return 0;
}
```
[$problem.4$](https://www.luogu.com.cn/problem/P6419)

```cpp
鸽
```

完结撒花