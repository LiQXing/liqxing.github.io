$T1$

题意：给出两条线段（注意是线段！）求其最短距离。

注意，以后这种题都要把所有$int$ 换成$double$,不然很可能出现一些SB的错误

比如

```cpp
inline double dist(int x1,int y1,int x2,int y2){
	return sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2));
}
```

注意细节。


```cpp
#include<bits/stdc++.h>
#include <iostream>

using namespace std;

//#define int long long
#define eps 1e-7

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch>'9'||ch<'0'){if(ch=='-')f=-1;ch=getchar();}
	while(ch<='9'&&ch>='0'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
struct node{
	double x,y;
}a[10];
double ans;
double lx1,rx1,lx2,rx2;
double k1,k2,b1,b2;
inline double dist(double x1,double y1,double x2,double y2){
	return sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2));
}
inline double check(int i){
	if(i==1||i==2){
		double k3=-1/k2,b3=a[i].y-k3*a[i].x;
		double x1=((b2-b3)/(k3-k2));
		double y1=k2*x1+b2;
		double dis=dist(a[i].x,a[i].y,x1,y1);
		if(k2==0&&a[1].x>=lx2&&a[1].x<=rx2)return dis;
		if(x1>lx2&&x1<rx2)return dis;
		else return 1e12;
	}
	if(i==3||i==4){
		double k3=-1/k1,b3=a[i].y-k3*a[i].x;
		double x1=((b1-b3)/(k3-k1));
		double y1=k1*x1+b1;
		double dis=dist(a[i].x,a[i].y,x1,y1);
		//cout<<dis<<endl;
		//if(x1==nan)return dis
		if(k1==0&&a[3].x>=lx1&&a[3].x<=rx1)return dis;
		if(x1>lx1&&x1<rx1)return dis;
		else return 1e12;
	}
	return 1e12;
}
signed main(){
	//ios_base::sync_with_stdio(false);cin.tie(0);cout.tie(0);
	for(int i=1;i<=4;i++){
		cin>>a[i].x>>a[i].y;
	}
	k1=(a[1].y-a[2].y)/(a[1].x-a[2].x);
	k2=(a[3].y-a[4].y)/(a[3].x-a[4].x);
	b1=a[1].y-a[1].x*k1;
	b2=a[3].y-a[3].x*k2;
	lx1=min(a[1].x,a[2].x);
	rx1=max(a[1].x,a[2].x);
	lx2=min(a[3].x,a[4].x);
	rx2=max(a[3].x,a[4].x);
	if(fabs(k1-k2)<eps&&fabs(b1-b2)<eps){
		cout<<"0.0000"<<endl;
		return 0;
	}
	double x0=(b2-b1)/(k1-k2);
	double y0=(k1*x0)+b1;
	if(x0>lx1&&x0>lx2&&x0<rx1&&x0<rx2){
		cout<<"0.0000"<<endl;
		return 0;
	}
	ans=min(min(dist(a[1].x,a[1].y,a[3].x,a[3].y),dist(a[2].x,a[2].y,a[4].x,a[4].y)),min(dist(a[1].x,a[1].y,a[4].x,a[4].y),dist(a[2].x,a[2].y,a[3].x,a[3].y)));
	for(int i=1;i<=4;i++){
        double t=check(i);
        ans=min(ans,t);
        //cout<<t<<endl;
    }
    
	printf("%.4lf",ans);
	return 0;
}

```

$T2$

二叉树+树上 $ DP$，

$d[u][x]$ 指 $ u $ 元件变为 $x $ 状态需要几步

如果原件是 &

则
```cpp
		d[u][1] = d[x][1] + d[y][1];
		d[u][0] = min(d[x][0], d[y][0]);
```
如果原件是|

则
```cpp
		d[u][0] = d[x][0] + d[y][0];
		d[u][1] = min(d[x][1], d[y][1]);
```
如果原件是^

则
```cpp
		d[u][0] = min(d[x][1] + d[y][1], d[x][0] + d[y][0]);
		d[u][1] = min(d[x][1] + d[y][0], d[x][0] + d[y][1]);	
```
```cpp
#include<bits/stdc++.h>

using namespace std;

//#define int long long
#define eps 1e-7

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch>'9'||ch<'0'){if(ch=='-')f=-1;ch=getchar();}
	while(ch<='9'&&ch>='0'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,m;
struct node{
	int son[2];
	int fa;
	int id;
}a[500500];
int d[500500][2];
inline void dfs(int u){
	if(a[u].son[0]) dfs(a[u].son[0]);
	if(a[u].son[1]) dfs(a[u].son[1]);
	int x = a[u].son[0], y = a[u].son[1];
	if(x == 0 && y == 0) return;
	if(a[u].id == 1) {
		d[u][1] = d[x][1] + d[y][1];
		d[u][0] = min(d[x][0], d[y][0]);
	}
	if(a[u].id == 2) {
		d[u][0] = d[x][0] + d[y][0];
		d[u][1] = min(d[x][1], d[y][1]);
	}
	if(a[u].id== 3) {
		d[u][0] = min(d[x][1] + d[y][1], d[x][0] + d[y][0]);
		d[u][1] = min(d[x][1] + d[y][0], d[x][0] + d[y][1]);	
	}
	return;
}
signed main(){
	n=read();m=read();
	int x;
	memset(d,0x3f,sizeof d);
	for(int i=1;i<=n;i++){
		a[i].son[0]=read();
		a[i].son[1]=read();
		a[i].fa=read();
		if(a[i].fa==0)x=i;
		a[i].id=read();
	}
	for(int i=1,u,v;i<=m;i++){
		u=read();v=read();
		d[u][v]=0;
		d[u][v^1]=1;
	}
	dfs(x);
	if(d[x][0])cout<<d[x][0]<<endl;
	else cout<<d[x][1]<<endl;
	return 0;
}

```

$T3$


首先是考试的时候想的大暴力（写挂了）

$AC$ 自动机+（$n=1$ 时 $kmp$ ）+ $dfs$ +输出大样例=$80pts $

```cpp
#include<bits/stdc++.h>

using namespace std;

//#define int long long
#define eps 1e-7

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch>'9'||ch<'0'){if(ch=='-')f=-1;ch=getchar();}
	while(ch<='9'&&ch>='0'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,l;
int val[50990];
struct node{
	int son[26];
	int ed;
}tr[550000];
int cnt,fail[100500];
inline void insert(string s,int x){
	int p=0;
	for(int i=0;i<s.size();i++){
		int ch=s[i]-'a';
		if(!tr[p].son[ch])tr[p].son[ch]=++cnt;
		p=tr[p].son[ch];
	}
	tr[p].ed+=x;
}
queue<int>q;
inline void getfail(){
	for(int i=0;i<26;i++){
		if(tr[0].son[i])q.push(tr[0].son[i]);
	}
	while(q.size()){
		int u=q.front();q.pop();
		for(int i=0;i<=25;i++){
			int v=tr[u].son[i];
			//cout<<v<<endl;
			if(v){
				fail[v]=tr[fail[u]].son[i];
           			tr[v].ed+=tr[tr[fail[u]].son[i]].ed;
           			q.push(v);
			}
			else tr[u].son[i]=tr[fail[u]].son[i];
		}
	}
}
int sum;
inline void dfs(int step,int ans,int u){
	if(step==l+1){
		sum=max(sum,ans);
		if(clock()>970000){
			cout<<sum;
			exit(0);
		}
		return;
	}
	for(int i=0;i<=25;i++){
		if(tr[u].son[i]){
			//cerr<<tr[tr[u].son[i]].ed<<endl;
			dfs(step+1,ans+tr[tr[u].son[i]].ed,tr[u].son[i]);
		}
	}
}
signed main(){
	ios_base::sync_with_stdio(false);cin.tie(0);cout.tie(0);
	cin>>n>>l;
	string a;
	for(int i=1;i<=n;i++){
		cin>>val[i];
	}
	for(int i=1;i<=n;i++){
		cin>>a;
		insert(a,val[i]);
	}
	getfail();
	dfs(1,0,0);
	cout<<sum;
	return 0;
}
```

$dfs$会超时，那么就写一个$dp$+滚动数组优化。

$dp[i][j]$指长度为i,最后一个字符节点为j的字符串的最大价值

易得转移方程

$$
dp[ cur+1 ][ tr[ k ].son [ j ] ]  = \max( dp[cur + 1][tr[k].son[j]], dp[cur][k] + tr[tr[k].son[j]].ed);
$$

```cpp
#include<bits/stdc++.h>

using namespace std;

//#define int long long
#define eps 1e-7
#define Inf -1e9

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch>'9'||ch<'0'){if(ch=='-')f=-1;ch=getchar();}
	while(ch<='9'&&ch>='0'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,l;
int val[50990];
struct node{
	int son[26];
	int ed;
}tr[550000];
int cnt,fail[100500],dp[2][500500];
inline void insert(string s,int x){
	int p=0;
	for(int i=0;i<s.size();i++){
		int ch=s[i]-'a';
		if(!tr[p].son[ch])tr[p].son[ch]=++cnt;
		p=tr[p].son[ch];
	}
	tr[p].ed+=x;
}
queue<int>q;
inline void getfail(){
	for(int i=0;i<26;i++){
		if(tr[0].son[i])q.push(tr[0].son[i]);
	}
	while(q.size()){
		int u=q.front();q.pop();
		for(int i=0;i<=25;i++){
			int v=tr[u].son[i];
			if(v){
				fail[v]=tr[fail[u]].son[i];
                tr[v].ed+=tr[tr[fail[u]].son[i]].ed;
                q.push(v);
			}
			else tr[u].son[i]=tr[fail[u]].son[i];
		}
	}
}
int sum;
inline void dpsolve(){
	int cur = 0;
	for(int i = 1; i <=cnt; i ++) dp[0][i] = dp[1][i] = Inf;
	dp[1][0] =Inf;
	for(int i = 1; i <=l;i ++) {
		for(int j=0;j<26;j++) {
			for(int k = 0; k <=cnt; k ++) {
				dp[cur^1][tr[k].son[j]] = max(dp[cur ^ 1][tr[k].son[j]], dp[cur][k] + tr[tr[k].son[j]].ed);
			}
		}
		for(int j = 0; j <=cnt; j ++)dp[cur][j] = Inf;
		cur ^= 1;
	} 
	int  res = 0;
	for(int i = 0; i <=cnt; i ++) res = max(res, dp[cur][i]);
	cout <<res <<endl;
	return;
}
signed main(){
	ios_base::sync_with_stdio(false);cin.tie(0);cout.tie(0);
	cin>>n>>l;
	string a;
	for(int i=1;i<=n;i++){
		cin>>val[i];
	}
	for(int i=1;i<=n;i++){
		cin>>a;
		insert(a,val[i]);
	}
	getfail();
	dpsolve();
	return 0;
}
```