# 笔记

------------
## $1. $折半搜索

[题目](https://www.luogu.com.cn/problem/P5691)

```cpp
#include <bits/stdc++.h>
#define mod 5000007
using namespace std;
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n, m, k[7], p[7], P[152][7], ans, table[mod], t[mod];
int Hash(int x) {
	int v = x % mod;
	if(v < 0) v += mod;
    while(t[v] && table[v] != x) {
	    v++;
		if(v == mod) v = 0;
	}
	return v;
}
inline void dfs1(int dep, int sum) {
	if(dep > (n >> 1)) {
		int v = Hash(sum); t[v]++, table[v] = sum; return;
	}
	for(int i = 1; i <= m; ++i) dfs1(dep + 1, sum + k[dep] * P[i][p[dep]]);
}
inline void dfs2(int dep, int sum) {
	if(dep > n) {
		ans += t[Hash(sum)]; return;
	}
	for(int i = 1; i <= m; ++i) dfs2(dep + 1, sum - k[dep] * P[i][p[dep]]);
}
int main() {
	n=read();m=read();
	ans = 0;
	for(int i = 1; i <= m; ++i) for(int j = 0; j <= 4; ++j) P[i][j] = j ? P[i][j - 1] * i : 1;
	for(int i = 1; i <= n; ++i) k[i]=read(),p[i]=read();
	dfs1(1, 0); dfs2((n >> 1) + 1, 0); printf("%d\n", ans);
	return 0;
}
```


------------
## $2.IDA*$

[题目](https://www.luogu.com.cn/problem/P1763#submit)
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
int len,ans;
bool flag;
bool vis[1000000];
int num[1011], tot[1011];
void dfs(int step,int n,int m,int limit,int limit2){
	if(step==limit+1){
		if(n==0){
			flag=true;
    		if(num[limit]<tot[limit]){
    			for(int i=1;i<=limit;i++)tot[i]=num[i];
				ans=num[limit];
			}
    	}
    	return;
	}
	if((m*(limit+1-step))/n>ans||num[step]>ans)return;
	for(int i=max(limit2,m/n);i<=m*(limit+1-step)/n;i++){
    	num[step]=i;
        dfs(step+1,n*i-m,m*i,limit,i+1);
    }
}
signed main() {
	int n,m;
	n=read();m=read();
	int limt;
	for(limt=1;;limt++){
		tot[limt]=0x3f3f3f3f;
    	ans=0x3f3f3f3f;
    	dfs(1,n,m,limt,1);
    	//cout<<limt<<endl;
    	if(flag)break;
	}
	for(int i=1;i<=limt;i++)cout<<tot[i]<<" ";
	return 0;
}
```
## $3.A*$(虽然我是暴力过的)

[题目](https://www.luogu.com.cn/problem/P1379)

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int dx[]={0,0,1,-1},dy[]={1,-1,0,0},g[5][5],x,y;
queue<int>q;
map<int,int>Map;
void filled(int n){
	for(int i=3;i>=1;i--){
		for(int j=3;j>=1;j--){
			g[i][j]=n%10;n/=10;
			if(g[i][j]==0)x=i,y=j;
		}
	}
}
int out(){
	int res=0;
	for(int i=1;i<=3;i++){
		for(int j=1;j<=3;j++){
			res=res*10+g[i][j];
		}
	}
	return res;
}
signed main(){
	int n;
	n=read();
	Map[n]=0;
	q.push(n);
	while(q.size()){
		int u=q.front(),k;q.pop();
		if(u==123804765) break;
		filled(u);
		for(int i=0;i<4;i++){
			int xx=x+dx[i],yy=y+dy[i];
			if(xx<=0||yy<=0||xx>3||yy>3)continue;
			swap(g[xx][yy],g[x][y]);
			k=out();
			if(Map.count(k)==0){
                Map[k]=Map[u]+1;
                //cout<<k<<" "<<Map[k]<<endl;
                q.push(k);
            }
			swap(g[xx][yy],g[x][y]);
		}
	}
	cout<<Map[123804765];
    return 0;
}

```
### 枚举技巧

$$Σi-j+k(i<j<k)$$

$1.$ 用前缀和优化,复杂度$ O n^2$

$2.$前缀和优化+改变枚举顺序，复杂度$O n$;

$3.$DP

$4.$推式子，复杂度,$On$
