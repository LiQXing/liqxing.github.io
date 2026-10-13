$T1$

简单的一道模拟,判断每一列出现次数大于$50%$的是$0$还是$1$

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
int n;
string a[1200],ans;
signed main(){
	n=read();
	for(int i=1;i<=n;i++){
		cin>>a[i];
	}
	int len=a[1].size();
	for(int i=0;i<len;i++){
		int res=0;
		for(int j=1;j<=n;j++){
			if(a[j][i]=='1')res++;
		}
		if(res*2<=n)ans+="0";
		else ans+="1";
	}
	cout<<ans;
	return 0;
}

```

$T2$

困难的一道$DP$

因为是求满足条件的情况下最小，显然是二分

但是二分里的$check（）$函数该怎么写

第一反应是贪心，判断

```cpp
inline bool check(int mid){
	r=rl;g=gl;
	memset(vis,0,sizeof vis);
	for(int i=1;i<=n;i++){
		if(vis[i])continue;
		int lu=0,re=0,tg=0;
		if(r<=0&&g<=0)break;
		else if(r>=2&&g>=1){
			for(int j=i;a[j]<=a[i]+2*mid-1&&j<=n;j++){
				vis[j]=1;
				lu++;
			}
			for(int j=i;a[j]<=a[i]+mid-1&&j<=n;j++){
				vis[j]=1;
				tg=j;
				re++;
			}
			for(int j=tg+1;a[j]<=a[tg+1]+mid-1&&j<=n;j++){
				vis[j]=1;
				re++;
			}
			if(re>lu)r-=2;
			else g--;
		}
		else if(r==1&&g>=1){
			for(int j=i;a[j]<=a[i]+mid-1&&j<=n;j++){
				vis[j]=1;
				re++;
			}
			for(int j=i;a[j]<=a[i]+2*mid-1&&j<=n;j++){
				vis[j]=1;
				lu++;
			}
			if(re==lu)r--;
			else g--;
		}
		else if(r==0&&g>=1){
			for(int j=i;a[j]<=a[i]+2*mid-1&&j<=n;j++){
				vis[j]=1;
				lu++;
			}
			g--;
		}
		else if(r>=1&&g==0){
			for(int j=i;a[j]<=a[i]+mid-1&&j<=n;j++){
				vis[j]=1;
			}
			r--;
		}
		if(vis[n]==1)return 1;
	}
	if(vis[n]==1)return 1;
	return 0;
}
```

这个贪心能拿$70pts$，不过显然这是错误的

随便构造一组数据,就会出错

```cpp
10 2 2
916526569
503972985
998944188
975448395
504413758
653166758
600020646
874687154
634208146
844992066

```

事实上这是一个$DP$,

二维，一个是$r$,一个是$g$，

两个辅助数组一个是判断红光，一个是绿光

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
int n,r,g,a[5005],rl,gl;
int dp[2500][2500],p[2500],q[2500];
inline bool check(int mid){
	memset(dp,0,sizeof dp);
	memset(p,0,sizeof p);
	memset(q,0,sizeof q);
	for(int i=1;i<=n;i++){
		for(int j=i;j<=n;j++){
			if(a[j]-a[i]+1<=mid)p[i]=j;
			if(a[j]-a[i]+1<=2*mid)q[i]=j;
		}
	}
	p[n+1]=q[n+1]=n;
	for(int i=0;i<=r;i++){
		for (int j=0;j<=g;j++){
	    	if(i>0)dp[i][j]=max(dp[i][j],p[dp[i-1][j]+1]);
	    	if(j>0)dp[i][j]=max(dp[i][j],q[dp[i][j-1]+1]);
	    }
	}
	return dp[r][g]==n;
}
signed main(){
	n=read();r=read();g=read();
	for(int i=1;i<=n;i++)a[i]=read();
	sort(a+1,a+1+n);
	if(r+g>=n){printf("1\n");return 0;}
	int l=1,r=1e9+10;
	while(l<r){
		int mid=(l+r)>>1;
		if(check(mid))r=mid;
		else l=mid+1;
	}
	printf("%lld",l);
	return 0;
}
```

$T3$

求次短路，用一个$dis2$保存,然后三种更新方式

```cpp
if(dis[v]<dis[u]+w)dis2[v]=min(dis2[v],dis[u]+w);
dis2[v]=min(dis2[v],dis2[u]+w);
if(dis[v]>dis[u]+w)
   dis2[v]=min(dis2[v],dis[v]);
```
发现只能拿$80pts$

不过我们发挥人类智慧

感觉是

```cpp
dis2[v]=min(dis2[v],dis2[u]+w);
```
没有更新完

所以我们跑两边spfa

轻松跑过
```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

const int mod=1e9+7;

inline int read(){
    int u=0,f=1;char ch=getchar();
    while (ch<'0'||ch>'9'){if(ch=='-') f=-1;ch=getchar();}
    while (ch>='0'&&ch<='9'){u=u*10+ch-48;ch=getchar();}
    return u*f;
}
int n,m;
queue<int>q;
vector<pair<int,int> >vec[500500];
int dis[500500],dis2[500500];
bool vis[500500];
inline void spfa(){
    memset(dis,0x3f,sizeof dis);
    memset(dis2,0x3f,sizeof dis2);
    q.push(1);
    vis[1]=1;
    dis[1]=0;
    while(q.size()){
        int u=q.front();q.pop();
        vis[u]=0;
        for(auto i:vec[u]){
            int v=i.first,w=i.second;
            if(dis[v]<dis[u]+w){
                dis2[v]=min(dis2[v],dis[u]+w);
                //cout<<v<<" "<<dis2[v]<<endl;
            }
            dis2[v]=min(dis2[v],dis2[u]+w);
            if(dis[v]>dis[u]+w){
                dis2[v]=min(dis2[v],dis[v]);
                //cout<<v<<" "<<dis2[v]<<endl;
                dis[v]=dis[u]+w;
                if(!vis[v]){
                    vis[v]=1;
                    q.push(v);
                }
            }
        }
    }
    memset(dis,0x3f,sizeof dis);
    q.push(1);
    vis[1]=1;
    dis[1]=0;
    while(q.size()){
        int u=q.front();q.pop();
        vis[u]=0;
        for(auto i:vec[u]){
            int v=i.first,w=i.second;
            if(dis[v]<dis[u]+w)dis2[v]=min(dis2[v],dis[u]+w);
            dis2[v]=min(dis2[v],dis2[u]+w);
            if(dis[v]>dis[u]+w){
                dis2[v]=min(dis2[v],dis[v]);
                dis[v]=dis[u]+w;
                if(!vis[v]){
                    vis[v]=1;
                    q.push(v);
                }
            }
        }
    }
}
signed main(){
    n=read();m=read();
    for(int i=1,u,v,w;i<=m;i++){
        u=read();v=read();w=read();
        vec[u].push_back({v,w});
        vec[v].push_back({u,w});
    }
    spfa();
    cout<<dis2[n]<<endl;
    return 0;
}
```