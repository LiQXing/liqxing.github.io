~~最~~小丑的一回（好像并不是）

[$My\;blog$](https://www.cnblogs.com/LiQXing/p/17794328.html)

T1 是个简单题，只要会高中基础几何就行了。

T2 看上去是个暴力，然后我也写了个暴力，结果跑大样例 dfs 进行到两万多层的时候 RE 了，完全不知道为什么，然后调调调调了一个多小时，到了十点放弃 T2 开始干 T3。

T3 看起来是个数学题，然后退式子，推推推大概半个小时过去了，有了点眉目，然后比对小样例，死活对不上答案，啊，原来是我题目看错了，那没事了。然后就死活推不出来。写了个 $k=1$ 的情况就滚去 T4。

T4 先看暴力 $n\le100$，$C_n^5$，那不是 $10^{10}$ 的复杂度吗（智慧的眼神），于是直接冲正解。看起来就非常二分，但是 check 函数不会，于是写了个很假的贪心，不出所料挂成了 $0$，部分分是一分都没有拿到，关键是部分分还贼多，心痛。

T2 考后发现 dev-c 栈爆了所以死活过不了大样例，写的做法被特殊性质卡了，wtm~。

## T1

```cpp
inline f96 dist(int x,int y,int xx,int yy){
	return (f96)sqrt((int)(x-xx)*(x-xx)+(y-yy)*(y-yy));
}
inline void solve(){
	int jwjx=read(),jwjy=read(),
	bqx=read(),bqy=read(),
	pqx=read(),pqy=read(),r=read();
	f96 ansjwj=max(dist(pqx,pqy,jwjx,jwjy),dist(pqx,pqy,bqx,bqy))+r;
	f96 a,b,c,ansbq;
	if(jwjx-bqx!=0){
		a=(f96)1.0*(jwjy-bqy)/(jwjx-bqx);
		b=-1;
		c=jwjy-jwjx*a;
		ansbq=1.0*abs((a*pqx+b*pqy+c))/(sqrtl(a*a+b*b))-r;
	}
	else{
		ansbq=abs(pqx-bqx)-r;
	}
	printf("%.2Lf %.2Lf\n",ansbq,ansjwj);
}
signed main(){
	int T=read();
	while(T--){
		solve();
	}
	return 0;
}
```

## T2

写法和题解略有不同，用一个 map 储存所有状态，记忆化搜索，当然，这样只能拿 $70$，题解的优化感觉很麻烦，我的优化反正就是求一个后缀 $lcm$，如果满足的话就直接跳，这个奇怪的优化可以增加 $30$。

ps：其实不知道这个优化优化了哪里，但他就是能过。
```cpp
int n,m; 
int a[N];
unordered_map<int,int>mp[N];
int gd[N];
inline int dfs(int t,int i){
	if(i==m+1)return t;
	if(t%gd[i]==0)return t;
	if(t%a[i]==0)return dfs(t,i+1);
	int res=t/a[i]+1;
	if(mp[i].count(res)>=1)return mp[i][res];
	return mp[i][res]=dfs(res*a[i],i+1);
}
signed main(){
	n=read();m=read();
	up(i,1,m)a[i]=read();
	gd[m]=a[m];
	dn(i,m-1,1)gd[i]=a[i]*gd[i+1]/__gcd(a[i],gd[i+1]);
	up(i,1,n)printf("%d ",dfs(i,1));
	return 0;
}

```

## T3
毒瘤的数学题。

已知：
$F_0(S)=[(\sum_{x\in S}x)=M]$

$F_k(S)=\sum_{T\subseteq S} F_{k-1}(T)$

不知道怎么推的，有公式 

$$F_k(S)=\sum_{T\subseteq S} F_{0}(T)\times k^{|S|-|T|}$$

可以归纳证明。

你手摸一下，大概是对的。

有了这个式子，题目就变得轻松起来了。

考虑优化一下状态设计：设 $f(i,w)$ 表示 ${a_1,a_2...a_i}$ 的所有和为 $w$ 的子集的贡献之和。 同样考虑最后一个数选不选： 

 - 如果没有选 $a_i$，那么相当于式 $S$ 中的大小增加了，因此 $f(i,w)$ 的指数也会加一。 
 -  原封不动加进来就行了。 

$$f(i,w)=f(i-1,w)\times k+f(i-1,w-a_i)$$

```cpp
inline void solve(){
	n=read();m=read();k=read();
	up(i,1,n)a[i]=read();
	f[0][0]=1;
	up(i,1,n){
		 up(j,0,m){
			f[i][j]=f[i-1][j]*k%mod;
			if(j>=a[i])f[i][j]=(f[i][j]+f[i-1][j-a[i]])%mod;
		}
	}
	cout<<f[n][m]<<endl;
}
```

## T4

佛怒火莲！

很显然的二分，但是如何 判断答案的合法性呢？

看到 $k\le 5$，一看就很状压。但是 $a_i\le n$ 怎么办呢，有一个非常暴力的做法，把这个序列 $n$ 映射到 $1-5$ 上，冲突的概率很小，同样操作两百遍后，相同的概率几乎为 $0$。

有 $dp_{i,sta}=max(dp_{j,pre})$

其实只用这个 DP，如果你够欧，你能拿满分。

另一种做法，把每一个点对应的存在离散化后的点里面。

随机打乱数组，直接 dp 判断，同样能过。

```cpp

struct node{int a,b;}p[N];
vector<int>pos[N],col;
int n,k,type,minum[5],dp[N];
inline bool check(int mid){
    int tmp=700;
    while(tmp--){
        shuffle(col.begin(),col.end(),rng);
        for(int i=1;i<k;++i) minum[i]=inf;
        minum[0]=-inf;
        for(auto x:col){
            for(auto i:pos[x]){
                dp[i]=upper_bound(minum,minum+k,p[i].b-mid)-minum;
                if(dp[i]==k) return 1;
            }
            for(auto i:pos[x])minum[dp[i]]=min(minum[dp[i]],p[i].b);
        }
    }
    return 0;
}
signed main(){
    int T;
    cin>>T;
    while(T--){
        n=read();m=read();type=read();
        col.clear();
        up(i,1,n) pos[i].clear();
        for(int i=1;i<=n;++i) scanf("%d %d",&p[i].a,&p[i].b),pos[p[i].a].push_back(i),col.push_back(p[i].a);
        sort(col.begin(),col.end());
        col.erase(unique(col.begin(),col.end()),col.end());
        int l=1,r=1e6,ans=0;
        while(l<=r){
            int mid=(l+r)>>1;
            if(check(mid)) ans=mid,l=mid+1;
            else r=mid-1;
        }
        printf("%d\n",ans);
    }
    return 0;
}
```













