$T1$

不好评价，题目数据有锅，虽然说 “保证长度没有重合的”，但是第二三个点都有重合

不过如果按题意来，其实很简单,直接按照题意模拟

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch>'9'||ch<'0'){if(ch=='-')f=-1;ch=getchar();}
	while(ch<='9'&&ch>='0'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int s,n,ans;
signed main(){
	freopen("china.in","r",stdin);
	freopen("china.out","w",stdout);
	s=read();n=read();
	ans=s;
	for(int i=1,a,b,t;i<=n;i++){
		a=read();b=read();t=read();
		ans+=(b-a+1)*(t-1);
	}
	printf("%lld",ans);
	return 0;
}

```

$T2$

一道单调栈的题，

首先可以$n^2$暴力

```cpp
	for(int i=1;i<=n;i++){
		int l=i,r=i;
		while(l>=1&&a[l]>=a[i])l--;
		while(r<=n&&a[r]>=a[i])r++;
		//cout<<l<<' '<<r<<endl;
		t=(r-l-1)*a[i];
		maxl=t>maxl?t:maxl;
	}
```

不过我们可以用一个栈来存后面个比现在小的数，使复杂度到$O(n)$

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch>'9'||ch<'0'){if(ch=='-')f=-1;ch=getchar();}
	while(ch<='9'&&ch>='0'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,a[200000],maxl,sta[200000],ans;
signed main(){
	//freopen("england.in","r",stdin);
	//freopen("england.out","w",stdout);
	n=read();
	for(int i=1;i<=n;i++){
		a[i]=read();
	}
	int t;
	int rr=0;
	for(int i=1;i<=n;i++){
		while(a[sta[rr]]>=a[i]&&rr>0) rr --;
		sta[++rr]=i;
		for(int j = 1; j <= rr; j ++) {
			ans=max(ans,a[sta[j]]*(sta[rr]-sta[j - 1]));
		}	
	}
	printf("%lld",ans);
	return 0;
}

```
$T3$

虽然题不难，但是坑却很多；

首先，不能通过只求两点解析式来判断是否可行

比如足球流氓在解析式上但是其$x$大于两点最大，

此时是可以传球的；

然后解析式有k不存在的情况，要记得考虑，

排除掉坑点，就只需要用因为$m$小于$300$，所以弗洛伊德求最短路就行了


```cpp
#include<bits/stdc++.h>

using namespace std;

//#define int long long
#define inf 1e7
#define eps 1e-5

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch>'9'||ch<'0'){if(ch=='-')f=-1;ch=getchar();}
	while(ch<='9'&&ch>='0'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,m;
struct node{
	int x,y;
}zz[5005],lm[5005];
double dis[500][500];
bool vis[500];
inline double check(int i,int j){
	 double k=(double)(zz[i].y-zz[j].y)/(zz[i].x-zz[j].x);
	 if(zz[i].x-zz[j].x<=eps)return inf;
	 double b=(double)zz[i].y-zz[i].x*k;
	 for(int l=1;l<=m;l++){
	 	if(lm[l].x>max(zz[i].x,zz[j].x)||lm[i].x<min(zz[i].x,zz[j].x))continue;
	 	if(lm[l].x*k+b-lm[l].y<=eps){
	 		//if(i==1&&j==3)cout<<l<<endl;
	 		return inf;
	 	}
	 }
	 return sqrt((zz[i].x-zz[j].x)*(zz[i].x-zz[j].x)+(zz[i].y-zz[j].y)*(zz[i].y-zz[j].y));
}
signed main(){
	//freopen("brazil.in","r",stdin);
	//freopen("brazil.out","w",stdout);
	zz[0].x=read();zz[0].y=read();n=read();m=read();
	for(int i=1;i<=n;i++){
		zz[i].x=read();
		zz[i].y=read();
	}
	for(int i=1;i<=m;i++){
		lm[i].x=read();
		lm[i].y=read();
	}
	for(int i=0;i<=n;i++){
		for(int j=i+1;j<=n;j++){
			if(i==0){
				dis[i][j]=inf;
				dis[j][i]=2*sqrt((zz[i].x-zz[j].x)*(zz[i].x-zz[j].x)+(zz[i].y-zz[j].y)*(zz[i].y-zz[j].y));
			}
			else{
				dis[i][j]=dis[j][i]=check(i,j);
			}
		}	
	}
	/*for(int i=1;i<=n;i++){
		for(int j=1;j<=n;j++){
			printf("%.4lf ",dis[i][j]);
		}
		printf("\n");
	}*/
	for(int k=1;k<=n;k++){
		for(int i=1;i<=n;i++){
			for(int j=1;j<=n;j++){
				dis[i][j]=min(dis[i][j],dis[i][k]+dis[k][j]);
			}
		}
	}
	double ans=inf;
	for(int i=1;i<=n;i++){
		ans=min(ans,dis[i][0]+dis[1][i]);
	}
	int t=ans*10;
	if(t%10>=5)printf("%d",t/10+1);
	else printf("%d",t/10);
	return 0;
}


```
$T4$

给出一个金字塔，让你求出最快从（$1$,$1$,$1$）到达顶点的路程

因为题目会给出到每个点的花费，以及所有暗道的位置，

所以我们可以大力建图，然后用$spfa$跑最短路；

$spf$a基本是模板，所以我们只需要注意如何建图就行了

```cpp
int dx[]={0, 1,-1,0,0, 0,-1,0,-1},dy[]={0, 0,0,1,-1, 0,0,-1,-1},dz[]={0,0,0,0,0,1,1,1,1};

for(int k=1;k<=8;k++)
	int tx=i+dx[k],ty=j+dy[k],tz=l+dz[k];
```
注意判断每个点是否可达

再加上暗道，

具体代码如下；

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

const int mod=1000;

inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,m,cnt;
int vis[500500],dis[500500];
int g[102][102][102];
vector<pair<int,int> >vec[500500];
int mp[102][102][102];
int dx[]={0, 1,-1,0,0, 0,-1,0,-1},dy[]={0, 0,0,1,-1, 0,0,-1,-1},dz[]={0,0,0,0,0,1,1,1,1};
queue<int>q;
void spfa(){
	memset(dis,0x3f, sizeof(dis));
	q.push(1);
	dis[1]=0;
	vis[1]=1;
	while (!q.empty()){
		int u=q.front();q.pop();
		vis[u]=false;
		for (auto i:vec[u]){
			int v =i.first,w=i.second;
			if (dis[v]>dis[u] + w){
				dis[v]=dis[u] + w;
				if (!vis[v]){
					q.push(v);
					vis[v]=1;
				}
			}
		}
	}
}
signed main(){
	n=read();m=read();
	for(int l=1;l<=n;l++){
		for(int i=1;i<=n-l+1;i++){
			for(int j=1;j<=n-l+1;j++){
				g[i][j][l]=read();
				mp[i][j][l]=++cnt;
			}
		}
	}
	for(int l=1;l<=n;l++){
		for(int i=1;i<=n-l+1;i++){
			for(int j=1;j<=n-l+1;j++){
				for(int k=1;k<=8;k++){
					int tx=i+dx[k],ty=j+dy[k],tz=l+dz[k];
					if(tx>(n-tz+1)||ty>(n-tz+1))continue;
					if(tx<=0||ty<=0||tz<=0)continue;
					if(tz>n)continue;
					vec[mp[i][j][l]].push_back({mp[tx][ty][tz],g[tx][ty][tz]});
				}
			}
		}
	}
	for(int i=1,a1,b1,c1,a2,b2,c2,t;i<=m;i++){
		a1=read();b1=read();c1=read();
		a2=read();b2=read();c2=read();
		t=read();
		vec[mp[b1][c1][a1]].push_back({mp[b2][c2][a2],t+g[b2][c2][a2]});
	}
	spfa();
	cout<<dis[cnt]+g[1][1][1];
	return 0;
}
		
```