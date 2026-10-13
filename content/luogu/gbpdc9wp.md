
我服了我自己$! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !$

又交错了题$! ! ! ! ! ! ! ! ! ! !$

再交一次忘了写$freopen$



------------

$T1$

题意：
给你两个序列
各从其中抽取几个数，使得两个序列选出的数和相同
且选的数的个数最小 


非常$"$简单$"$的背包，可是我没想到
原题可见砝码称重,把能取到的值标记

最后遍历一遍，找出最小步骤


```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

const int mod=998244353;

inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,m,sumn,summ,a[500500],b[500500],f1[1500500],f2[1500500];
signed main(){
	n=read();
	for(int i=1;i<=n;i++){
		a[i]=read();
		sumn+=a[i];
	}
	memset(f1,0x3f,sizeof f1);
	f1[0]=0;
	
	for(int i=1;i<=n;i++){
		for(int j=sumn;j>=a[i];j--){
			f1[j]=min(f1[j],f1[j-a[i]]+1);
		}
	}
	m=read();
	for(int i=1;i<=m;i++){
		b[i]=read();
		summ+=b[i];
	}
	memset(f2,0x3f,sizeof f2);
	f2[0]=0;
	for(int i=1;i<=m;i++){
		for(int j=summ;j>=b[i];j--){
			f2[j]=min(f2[j],f2[j-b[i]]+1);
		}
	}
	int ans=0x3f3f3f3f;
	for (int i=1;i<=min(summ,sumn);i++){
		if (f1[i]<=0x3f3f3f3f&&f2[i]<=0x3f3f3f3f){
			ans=min(f1[i]+f2[i],ans);
		}
	}
	if (ans==0x3f3f3f3f)cout<<"impossible";
	else cout<<ans;
    return 0;
}
```

$T2$

照着题意模拟，我们可以预处理出每个鸟离探测器的距离范围，再用差分求和

判定点与圆的位置关系

可以把每一个矩形到这个顶点的最近和最远曼哈顿距离求出来

然后对于每一个询问，如果听到信号的距离是在这俩距离之间

就是有交点嘛,在数轴上这个区间 $l$ 加一, $r+1$ 减一，

数据范围 $x,y\le10^6$

轻松过

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long
#define inf 0x3f3f3f3f

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,q,x,y,f[5005000];
inline int dis(int x1,int y1,int x2,int y2){
	return abs(x1-x2)+abs(y1-y2);
}
inline int calamin(int i,int xa,int ya,int xb,int yb){
	if(x<=xa&&x>=xb&&y<=ya&&y>=yb)return 0;
	if(x<=xa&&x>=xb)return min(abs(y-ya),abs(y-yb));
	if(y<=ya&&y>=yb)return min(abs(x-xa),abs(x-xb));
	int q,w,e,r;
	q=dis(x,y,xa,ya);w=dis(x,y,xb,yb);
	e=dis(x,y,xa,yb);r=dis(x,y,xb,ya);
	return min(min(q,w),min(e,r));
}
inline int calamax(int i,int xa,int ya,int xb,int yb){
	int q,w,e,r;
	q=dis(x,y,xa,ya);w=dis(x,y,xb,yb);
	e=dis(x,y,xa,yb);r=dis(x,y,xb,ya);
	return max(max(q,w),max(e,r));
}
signed main(){
	freopen("bird.in","r",stdin);
	freopen("bird.out","w",stdout);
	n=read();q=read();
	x=read();y=read();
	int l,r,xa,ya,xb,yb,maxl=0;
	for(int i=1,q,w,e,r;i<=n;i++){
		q=read();w=read();e=read();r=read();
		xa=max(q,e);ya=max(w,r);
        xb=min(q,e);yb=min(w,r);
		l=calamin(i,xa,ya,xb,yb)
        ;r=calamax(i,xa,ya,xb,yb);
		//maxl=max(r,maxl);
		//cout<<l<<" "<<r<<endl;
		f[l]++;f[r+1]--;
	}
	for(int i=1;i<=2100000;i++){
		f[i]+=f[i-1];
	}
	int ask;
	while(q--){
		ask=read();
		printf("%lld\n",f[ask]);
	}
	return 0;
}
```

$T3$
题意：$n$  种卡片(每种长$l$​ 高 $h$​ 有 $num$ 个)塞进 $k$ 个信封

一种卡片浪费的空间就是它所在信封的面积减去他自己的面积

问浪费的空间最小是多少.

看一眼数据范围

$$N\le 15$$

可以很快的联想到状压$DP$

思考一下推出方程

$f[i][j]=c1,c2⊆i,c1∩c2=∅,c1⊔c2=imin​(f[c1][j−1]+f[c2][1])$

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

const int mod=998244353;

inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int maxl,maxr,k;
int a[500],b[500],c[500],cost[1<<15|1],l[1<<15|1],r[1<<15|1],num[1<<15|1];
int n,f[1<<15|1][20];
signed main(){
	n=read();k=read();
	for(int i=1;i<=n;i++){
		a[i]=read();
		b[i]=read();
		c[i]=read();		
	}
	int all=(1<<n)-1;
	for(int i=0;i<=all;i++){
		for(int j=1;j<=n;j++){
			if(!(i&1<<(j-1))){
				l[i|1<<(j-1)]=max(l[i],a[j]);
				r[i|1<<(j-1)]=max(r[i],b[j]);
				num[i|1<<(j-1)]=num[i]+c[j];
				cost[i|1<<(j-1)]=cost[i]+a[j]*b[j]*c[j];
			}
		} 
	}
	for(int i=0;i<=all;i++) cost[i]=num[i]*l[i]*r[i]-cost[i];
	memset(f,0x3f,sizeof f);
	for(int i=1;i<=all;i++)f[i][1]=cost[i];
	for(int i=1;i<=all;i++){
		for(int j=1;j<k;j++){
			for(int hh=i;hh;hh=(hh-1)&i){
				f[i][j+1]=min(f[i][j+1],cost[i^hh]+f[hh][j]);
			}
		}
	}  
	printf("%lld\n",f[all][k]);
    return 0;
}
```

