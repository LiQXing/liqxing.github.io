$T1$

结论题：最优情况一定只有两个点

证明：假设有一点对，从这点对延伸出去的一条边可以使点权与边权的比变大；

设原先点的边权为$a$，点权为$ka$，比值为$k$，则延伸后比值为$k+d$，边值为$a+l$，则点权为（$a+l)$*（$k+d$）=$ak+ad+lk+ld$，增加点权为 $ad+lk+ld$ 则延伸边的比为($k+d+ad/l$）>
$k+d$ 

$Qed;$

当然，推出结论并没有神么用

如

```cpp
ans=max(ans,(double)a[i]+a[v]/w);
```
手残一下少 $40pts$

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long
#define pii pair<int,int>

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,m,a[150050];double ans=0;
bool vis[500500];
vector<pii>vec[500500];
void main1();
signed main(){
	//freopen("graph.in","r",stdin);
	//freopen("graph.out","w",stdout);
	n=read();m=read();
	for(int i=1;i<=n;i++)a[i]=read();
	for(int i=1,u,v,w;i<=m;i++){
		u=read();v=read();w=read();
		vec[u].push_back({v,w});
		vec[v].push_back({u,w});
	}
	if(m==0){printf("0");return 0;}
	if(n==2){main1();return 0;}
	for(int i=1;i<=n;i++){
		for(auto j:vec[i]){
			int v=j.first,w=j.second;
			ans=max(ans,(double)(a[i]+a[v])/w);
		}
	}
	if(ans==0)printf("0");
	else printf("%.2lf",ans);
	return 0;
}
void main1(){
	int w=vec[1][0].second;
	double dian=a[1]+a[2];
	printf("%.2lf",dian/w);
}
```

$T2$

$n$的数据范围为$1e8$，背包显然会炸，考虑到个数比较小，可以用双向搜索，把$ab$,$cd$分开枚举，不过如果硬枚举的话，空间会炸，优化空间时间会炸

如
```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,an,bn,cn,dn,m,ans;
int a[8005],b[8005],c[8005],d[8005];
int ab[25005000],cd[25000500],cishu[25000500];
signed main(){
	//freopen("eat.in","r",stdin);
	//freopen("eat.out","w",stdout);
	n=read();an=read();bn=read();cn=read();dn=read();
	for(int i=1;i<=an;i++)a[i]=read();
	for(int i=1;i<=bn;i++)b[i]=read();
	for(int i=1;i<=cn;i++)c[i]=read();
	for(int i=1;i<=dn;i++)d[i]=read();
	int len=0,t;
	for(int i=1;i<=an;i++){
		for(int j=1;j<=bn;j++){
			ab[++len]=a[i]+b[j];
		}
	}
	//sort(ab+1,ab+1+len);
	m=len;len=0;
	for(int i=1;i<=cn;i++){
		for(int j=1;j<=dn;j++){
			cd[++len]=c[i]+d[j];
		}
	}
	sort(cd+1,cd+1+len);
	for(int i=1;i<=len;i++)cishu[i]=cishu[i-1]+1;
	int low=0,upp=0;
	int key;
	for(int i=1;i<=m;i++){
		upp=(upper_bound(cd+1,cd+1+len,n-ab[i])-cd);
		//if(low==upp)continue;
		ans+=cishu[upp-1];
	}
	cout<<ans;
	return 0;
}
```
你谷上能拿$70pts$，所以还是要搜索

```cpp
#include<bits/stdc++.h>

using namespace std;

//#define int long long

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,m;
int a[5][6000],cnt[5];
int f[100000500];
long long ans;
void dfsab(int step,int sum){
	if(step>2){
		f[sum]++;
		return;
	}
	for(int i=1;i<=cnt[step];i++){
		if(sum+a[step][i]<=n) {
			dfsab(step + 1, sum + a[step][i]);
		}
	}
}
void dfs(int step,int sum){
	if(step>4){
		ans+=f[n-sum];
		return;
	}
	for(int i=1;i<=cnt[step];i++){
		if(sum+a[step][i]<=n) {
			dfs(step+1,sum+a[step][i]);
		}
	}
}
signed main(){
	//freopen("eat.in","r",stdin);
	//freopen("eat.out","w",stdout);
	n=read();cnt[1]=read();cnt[2]=read();cnt[3]=read();cnt[4]=read();
	for(int i=1;i<=4;i++){
		for(int j=1;j<=cnt[i];j++){
			a[i][j]=read();
		}
	}
	dfsab(1,0);
	for(int i=1;i<=n;i++)f[i]+=f[i-1];
	dfs(3,0);
	cout<<ans;
	return 0;
}
```

$T3$

题意比较简单，想出暴力应该不难画出函数图像，当距离最小时，一定是速度最快的豹与一个豹的交点；

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,maxv,vi,ti;
double maxt;
struct node{
	double t,v;
}a[100050];
inline bool cmp(node l,node r){
	if(l.v==r.v)return l.t>r.t;
	return l.v<r.v;
}
inline double clac(int i,int j){
	return (double)(a[i].v*a[i].t-a[j].v*a[j].t)/(a[i].v-a[j].v);
}
signed main(){
	//freopen("chase.in","r",stdin);
	//freopen("chase.out","w",stdout);
	n=read();
	for(int i=1;i<=n;i++){
		a[i].t=read();
		a[i].v=read();
		maxt=max(a[i].t,maxt);
	}
	sort(a+1,a+1+n,cmp);
	double ans=0,maxl,minl=1e14;
	for(int i=1;i<=n;i++){
		maxl=max(maxl,a[i].v*(maxt-a[i].t));
		minl=min(minl,a[i].v*(maxt-a[i].t));
	}
	ans=maxl-minl;
	for(int l=1;l<n;l++){
		double jx=clac(n,l);
		if(jx<maxt)continue;
		maxl=0;minl=1e14;
		for(int i=1;i<=n;i++){
			maxl=max(maxl,a[i].v*jx-a[i].v*a[i].t);
			minl=min(minl,a[i].v*jx-a[i].v*a[i].t);
		}
		if(maxl==a[n].v*jx-a[n].v*a[n].t)break;
		if(minl==1e14)continue;
		ans=min(ans,maxl-minl);
	}
	printf("%.2lf",ans);
	return 0;
}

```

此代码能拿$80pts$

在进一步分析，最大距离其实是一个单峰函数，在某一点后只会上升

所以只用三分法求定点

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

const double eps=1e-8;

inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
struct node{
	int t,v;
}a[500500];
int n;
double l=0;
double check(double mid){
	double minn,maxx,temp;
	minn=maxx=(mid-a[1].t)*a[1].v;
	for(int i=2;i<=n;i++){
		temp=(mid-a[i].t)*a[i].v;	
		minn=min(minn,temp);
		maxx=max(maxx,temp);
	}
	return maxx-minn;
}
signed main(){
	n=read();
	for(int i=1;i<=n;i++){
		a[i].t=read();
		a[i].v=read();
		l=max(l,(double)a[i].t);
	}
	double r=1e15,lmid,rmid;
	while(r-l>eps){
		lmid=l+(r-l)/3;
		rmid=r-(r-l)/3;
		if(check(lmid)<check(rmid))r=rmid;
		else l=lmid;
	}
	printf("%.2lf",check(l));
    return 0;
}
```