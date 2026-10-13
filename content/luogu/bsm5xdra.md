## $1.$分治

$1.$平面内最近点对

[题目](https://www.luogu.com.cn/problem/P1429)

```cpp
#include <bits/stdc++.h>
#define int long long
using namespace std;
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,temp[250000];
struct node{
	int x,y;
}a[500500];
bool cmp(node l,node r){
	if(l.x==r.x)return l.y<r.y;
	return l.x<r.x;
}
double dis(int l,int r){
	return sqrt((a[l].x-a[r].x)*(a[l].x-a[r].x)+(a[l].y-a[r].y)*(a[l].y-a[r].y));
}
bool cmp2(int x,int y){
	return a[x].y<a[y].y;
}
double merge(int l,int r){
	double d;
	if(l==r){return 1e9;}
	if(l==r-1){
		return dis(l,r);
	}
	int mid=(l+r)>>1;
	double d1=merge(l,mid);
	double d2=merge(mid+1,r);
	d=min(d1,d2);
	int k=0;
	for(int i=l;i<=r;i++){
		if(fabs(a[mid].x-a[i].x)<d) 
            temp[k++]=i;
	}
    sort(temp,temp+k,cmp2);
    for(int i=0;i<k;i++){
    	for(int j = i + 1;j<k&&a[temp[j]].y-a[temp[i]].y<d;j++){
            double d3=dis(temp[i],temp[j]);
            if(d > d3)d=d3;
        }	
    }
    return d;
}
signed main() {
	n=read();
	for(int i=1;i<=n;i++){
		a[i].x=read();
		a[i].y=read();
	}
	sort(a+1,a+1+n,cmp);
	double k=merge(1,n);
	printf("%.4lf",k);
	return 0;
}
```

$2.$矩形内的分治

[题目](https://www.luogu.com.cn/problem/CF364E)

思路：按行分治，再按列分治，交次进行；

$up[0][k]$表示在$mid$上方，满足矩形$sum(i,j,up[0][i],mid)<k$的最小纵（横）坐标，$up[1][k]$为最大纵(横）坐标，答案可化为：
$$ans=\sum_{i=0}^{k}(up[0][i]-up[0][i+1])*(up[1][k-i+1]-up[1][k-i])$$
```cpp
#include <bits/stdc++.h>
using namespace std;
//#define int long long 
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
long long n,m,k,ans;
long long a[2530][2530],up[5][2534];
int sum(int x1,int x2,int y1,int y2){
	return a[x2][y2]-a[x1][y2]-a[x2][y1]+a[x1][y1];
}
void merge(int x1,int x2,int y1,int y2,int kind){
	if(x1==x2||y1==y2)return;
	if(x1+1==x2&&y1+1==y2){
		if(sum(x1,x2,y1,y2)==k)ans++;
		return;
	}
	//行分治
	if(kind==1){
		int mid=(x1+x2)>>1;
		merge(x1,mid,y1,y2,0);
		merge(mid,x2,y1,y2,0);
		for(int i=y1;i<y2;i++){
			up[0][0]=up[1][0]=mid;
			for(int j=1;j<=k+1;j++){
				up[0][j]=x1;
				up[1][j]=x2;	
			}
			for(int j=i+1;j<=y2;j++){
				for(int l=1;l<=k+1;l++){
					while(sum(up[0][l],mid,i,j)>=l)up[0][l]++;
					while(sum(mid,up[1][l],i,j)>=l)up[1][l]--;
				}
				for(int l=0;l<=k;l++){
					ans+=(up[0][l]-up[0][l+1])*(up[1][k-l+1]-up[1][k-l]);
				}
			}
		}
	}
	//列分治
	if(kind==0){
		int mid=(y1+y2)>>1;
		merge(x1,x2,y1,mid,1);
		merge(x1,x2,mid,y2,1);
		for(int i=x1;i<x2;i++){
			up[0][0]=up[1][0]=mid;
			for(int j=1;j<=k+1;j++){
				up[0][j]=y1;
				up[1][j]=y2;
			}
			for(int j=i+1;j<=x2;j++){
				for(int l=1;l<=k+1;l++){
					while(sum(i,j,up[0][l],mid)>=l)up[0][l]++;
					while(sum(i,j,mid,up[1][l])>=l)up[1][l]--;
				}
				for(int l=0;l<=k;l++){
					ans+=(up[0][l]-up[0][l+1])*(up[1][k-l+1]-up[1][k-l]);
				}
			}
		}
	}
	return;
}
signed main(){
	n=read();m=read();k=read();
	for(int i=1;i<=n;i++){
		for(int j=1;j<=m;j++){
			scanf("%1lld",&a[i][j]);
			a[i][j]+=a[i-1][j]+a[i][j-1]-a[i-1][j-1];	
		}
	}
	merge(0,n,0,m,0);
	cout<<ans;
	return 0;
}
```

$3.$分治练习题

题目：有$n$个物品第$i$个物品重量是$w_i$,价值是$v_i$,要最大化价值和。对每个$i$,询问假设第$i $个物品消失此时价值和最大是多少？

$1.$分治 空间$O(Wlogn)$, 时间$O(nWlogn)$;

```cpp
鸽
```

$2.$合并前后缀：空间$O(nW)$,时间$O(nW)$;

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,m,w[250],v[250],W,f1[50050],f2[50050];
signed main(){
	n=read();W=read();
	for(int i=1;i<=n;i++){
		w[i]=read();
		v[i]=read();
	}
	for(int i=1;i<=n;i++){
		for(int j=W;j>=w[i];j--){
			f1[j]=max(f1[j],f1[j-w[i]]+v[i]);
		}
	}
	for(int i=n;i>=1;i--){
		for(int j=W;j>=w[i];j--){
			f2[j]=max(f2[j],f2[j-w[i]]+v[i]);
		}
	}
	int ans=0;
	for(int i=1;i<=n;i++){
		ans=max(f1[i-1]+f2[i+1],ans);
	}
	cout<<ans;
	return 0;
}

```


------------
## 二分

$1.$求序列中第$k$小子串的平均值。$N\le10^5$

·误差不超过$10^{-6}$


提示：原式=$\sum_{i=l}^r(a_i-mid)\le0$

```cpp
鸽
```

$2.$给定一个序列，求所有区间$gcd$的和。$N\le10^5,a_i\le10^9$;

```cpp
鸽
```
## 倍增

$1.$环上有$n$段弧，选出尽量多的弧使两两没有相交。$N\le10^5$;
```cpp
鸽
```

## 贪心

[题目](https://www.luogu.com.cn/problem/CF875F)

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,m,sum;
int fa[500500],a[500500];
struct node{
	int u,v,w;
}e[500500];
bool cmp(node x,node y){return x.w>y.w;}
int find(int x){
	if(x==fa[x])return x;
	return fa[x]=find(fa[x]);
}
void krus(){
	for(int i=0;i<=n;i++){
		fa[i]=i;
		a[i]=1;	
	}
	for(int i=1;i<=m;i++){
		int x=find(e[i].u),y=find(e[i].v);
		if(x!=y&&(a[x]||a[y])){
			fa[x]=y;
			sum+=e[i].w;
			a[y]=a[x]&a[y];
		}                                          
		else if(x==y&&a[x]){
			a[x]=0;
			sum+=e[i].w;
		} 
	}
}
signed main(){
	n=read();m=read();
	for(int i=1;i<=m;i++){
		e[i].u=read();
		e[i].v=read();
		e[i].w=read();
	}
	sort(e+1,e+1+m,cmp);
	krus();
	printf("%lld",sum);
	return 0;
}

```
完结撒花


