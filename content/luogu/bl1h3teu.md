$T1$

[题目](https://www.luogu.com.cn/problem/T314006)

题意：给定一棵树上$n$个点的度数求最长链

分析，一颗树的最长链为直径，则两端点一定度数为$1$,这里可以运用贪心的思想，
如果一个点的度数大于$2$，则将其连在直径上，这是可以成立的

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,a[5005],sum,ans;
signed main(){
    n=read();
    for(int i=1;i<=n;i++){
    	a[i]=read();
    	sum+=a[i];
    }
    if(sum==(n-1)<<1){
    	for(int i=1;i<=n;i++){
    		if(a[i]>=2)ans++;
    	}
    	printf("%lld",ans+1);
    }
    else printf("-1");
    return 0;
}
```
$T2$

[题目](https://www.luogu.com.cn/problem/T314007)

分析：求最小的最大值，显然用二分，但是这里有绝对值，怎么考虑

首先说明思路，二分的东西就是答案

矩阵$A$已知，最小的范数就是二分的值，那么就可以求出矩阵$B$的值的范围。

具体来说，$A$如果的范数最小是$x$，那么对于矩阵中的某一个元素$a$，应该在$|a-b|=x$之间

最小值小于等于$0$，最大值大于等于$0$，那么，根据函数的连续性（零点存在定理），一定存在行列式的值为$0$的情况，也就是说，一定存在一种构造，在满足各个元素的取值在给定范围内的情况下，使得矩阵的行列式的值为$0$。

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long
#define eps 1e-5

inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}

double a,b,c,d;
bool check(double mid){
	double l1=min(min((a-mid)*(d-mid),(a+mid)*(d+mid)),min((a-mid)*(d+mid),(a+mid)*(d-mid)));
	double r1=max(max((a-mid)*(d-mid),(a+mid)*(d+mid)),max((a-mid)*(d+mid),(a+mid)*(d-mid)));
	double l2=min(min((b-mid)*(c-mid),(b+mid)*(c+mid)),min((b-mid)*(c+mid),(b+mid)*(c-mid)));
	double r2=max(max((b-mid)*(c-mid),(b+mid)*(c+mid)),max((b-mid)*(c+mid),(b+mid)*(c-mid)));
	if(r1+eps<l2||r2+eps<l1) return 0;
	return 1;
}
signed main(){
    cin>>a>>b>>c>>d;
	double l=0,r=2e9,ans=0;
	while(fabs(r-l)>=eps){
		double mid=(l+r)/2;
		if(check(mid))r=mid,ans=mid;
		else l=mid;
	}
	printf("%.3lf",ans);
    return 0;
}
```