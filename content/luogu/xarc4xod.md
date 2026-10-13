[$problem.1$](https://www.luogu.com.cn/problem/P3177)

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
int n,m,k,siz[500500],f[2500][2500];
vector<pair<int,int> >vec[500500];
void dfs(int u, int from) {
	siz[u]=1;f[u][0]=f[u][1]=0;
	for (auto i:vec[u]){
		int v=i.first,w=i.second;
		if (v==from)continue;
		dfs(v,u);siz[u]+=siz[v];
		for (int j=min(m, siz[u]);~j;j--) 
			for (int k=0;k<=min(j,siz[v]);k++) {
				if (!(~f[u][j - k])) continue;
				int tmp =w*k*(m-k)+w*(siz[v]-k)*(n-m-siz[v]+ k);
				f[u][j] = max(f[u][j], f[u][j - k] + f[v][k] + tmp);
			}
	}
	return;
}
signed main(){
	n=read();m=read();
	int u,v,w;
	for(int i=1;i<n;i++){
		u=read();v=read();w=read();
		vec[u].push_back({v,w});
		vec[v].push_back({u,w});
	}
	memset(f,-1,sizeof f);
	dfs(1,0);
	printf("%lld",f[1][m]);
	return 0;
}
```

[$problem.2$](https://www.luogu.com.cn/problem/P2279)

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long 
inline int read(){
	register int u=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){u=u*10+ch-48;ch=getchar();}
	return u*f;
}
int n,dp[560050][6];
vector<int>vec[500500];
void dfs(int u,int from){
	int sum2 = 0, sum3 = 0,tot;
    for(auto v:vec[u]){
    	 if(v!=from) {
            dfs(v,u);
            sum2+=dp[v][2],sum3+= dp[v][3];
            tot++;
        }	
    }
	if(!tot){
        dp[u][0]=dp[u][1]=dp[u][2]=1;
        return;
    }
    dp[u][0]=1,dp[u][1]=dp[u][2]=0x3f3f3f3f;
    for (auto v:vec[u]){
    	if (v!= from) {
            dp[u][0]+=dp[v][4];
            dp[u][1]=min(dp[u][1], dp[v][0] + sum3 - dp[v][3]);
            dp[u][2]=min(dp[u][2], dp[v][1] + sum2 - dp[v][2]);
            dp[u][3]+=dp[v][2];
            dp[u][4]+=dp[v][3];
        }	
    }
    for (int i = 1; i<=4;i++) dp[u][i]=min(dp[u][i],dp[u][i-1]);
}
signed main(){
    n=read();
    int u;
    
    for(int i=1;i<n;i++){
    	u=read();
    	vec[u].push_back(i+1);
    	vec[i+1].push_back(u);
    }
    dfs(1,0);
    printf("%lld",dp[1][2]);
    return 0;
}
```

[$problem.3$](https://www.luogu.com.cn/problem/P3899)

```cpp
鸽
```

[$problem.4$](https://www.luogu.com.cn/problem/P2607)


```cpp
鸽
```

## 数位DP
[$problem.4$](https://www.luogu.com.cn/problem/P2657)
```cpp
#include<bits/stdc++.h>

using namespace std;

int f[250][250]; 

void init(){
	for(int i=0;i<=9;i++)f[1][i]=1;
	for(int i=2;i<=15;i++){
		for(int j=0;j<=9;j++){
			for(int k=0;k<=9;k++){
				if(abs(k-j)<2)continue;
				f[i][j]+=f[i-1][k];	
			}
		}
	}
}

int dp(int n){
	if(!n) return 0;
	vector<int>nums;
	while(n) nums.push_back(n%10),n/=10;
	int res=0,last=13;
	for(int i=nums.size()-1;i>=0;i--){
		int x=nums[i];
		for(int j= i==nums.size()-1;j<x;j++){
			if(abs(j-last)<2)continue;
			res+=f[i+1][j];
		}
		if(abs(x-last)>=2) last=x;
		else break;
		if(!i) res++;
	}
	for(int i=1;i<nums.size();i++){
		for(int j=1;j<=9;j++){
			res+=f[i][j];
		}
	}
	return res;
}
signed main(){
    ios::sync_with_stdio(false);
	cin.tie(nullptr);cout.tie(nullptr);
	init();
	int n,m;
	cin>>n>>m;
	cout<<dp(m)-dp(n-1)<<endl;
    return 0;
}
```
## 状压DP

[$problem.5$](https://www.luogu.com.cn/problem/P1896)

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long 
inline int read(){
	int u=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){u=u*10+ch-48;ch=getchar();}
	return u*f;
}
int n,m,f[15][200][100],cnt,all,s[500],sum[500];
bool check(int a,int b){
	if((a&b)||((a>>1)&b)||((a<<1)&b)) return 0;
	return 1;
}
void dp(){
	f[0][1][0]=1;
	for(int i=1;i<=n;i++){
		for(int j=1;j<=cnt;j++){
			for(int k=0;k<=m;k++){
				if(sum[j]>k) continue;
				for(int p=1; p<=cnt; p++)
					if(check(s[p],s[j]))
						f[i][j][k]+=f[i-1][p][k-sum[j]];
			}
		}
	} 
}
signed main(){
	n=read();m=read();
	all=(1<<n)-1;
	for(int i=0;i<=all;i++){
		if(!(i&(i<<1))){
			s[++cnt]=i;
			sum[cnt]=__builtin_popcount(i);
		}
	}
	dp();
	int ans=0;
	for(int i=1;i<=cnt;i++) ans+=f[n][i][m];
	printf("%lld",ans);
    return 0;
}
```
[$problem.6$](https://www.luogu.com.cn/problem/P2157)

```cpp
鸽
```


