
## T1

简单题，猜结论，要么是 $Q$ 的因数，要么是 $L/Q\times Q$ 的因数。

```cpp
int L,R,Q;
vector<pii>fac;
inline void devide(int x){
    int t=x;
    for(int i=2;i<=sqrt(x);i++){
        if(t%i==0){
            int res=0;
            while(t%i==0){
                t/=i;
                res++;
            }   
            fac.push_back({i,res});
        }
    }
    if(t!=1)fac.push_back({t,1});
}
signed main() {
    cin>>L>>R>>Q;
    if(Q>R){
        cout<<"infinity"<<endl;
        return 0;
    }
    if(R/Q==L/Q){
        devide(L/Q*Q);
        int res=1;
        for(auto [a,b]:fac){
            res=res*(b+1);
        }
        cout<<res<<endl;
        return 0;
    }
    else{
        devide(Q);
        int res=1;
        for(auto [a,b]:fac){
            res=res*(b+1);
        }
        cout<<res<<endl;
        return 0;
    }
    return 0;
}
```

## T2

更简单题，先把所有点加入集合，再删点。

```cpp
int n,m,d,deg[N];
vector<int>g[N];
bool vis[N],inq[N];
inline void dfs(int u,int from,vector<int>&s){
    vis[u]=1;
    s.push_back(u);
    for(auto v:g[u]){
        if(vis[v])continue;
        dfs(v,u,s);
    }
}
int ans=0;
signed main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);cout.tie(0);
 
    cin>>n>>m>>d;
    int u,v;
    up(i,1,m){
        cin>>u>>v;
        g[u].push_back(v);
        g[v].push_back(u);
        deg[u]++,deg[v]++;
    }
    up(i,1,n){
        if(!vis[i]){
            vector<int>s;
            queue<int>q;
            dfs(i,0,s);
            int cnt=0;
            for(auto v:s){
                if(deg[v]<d)q.push(v),cnt++,inq[v]=1;
            }
            while(q.size()){
                int u=q.front();q.pop();
                for(auto v:g[u]){
                    if(!inq[v]){
                        deg[v]--;
                        if(deg[v]<d){
                            inq[v]=1;
                            q.push(v);
                            cnt++;
                        }
                    }
                }
            }
            ans=max(ans,(int)s.size()-cnt);
        }
    }
    cout<<ans;
    return 0;
}
```

## T3

转化一下，就是
$$\sum_{k=0}^{k\le \left\lfloor\frac{n}{2}\right\rfloor}\dbinom{n}{k}\times \dbinom{n-k}{k}$$

这个柿子，你会惊奇的发现它是 $(x^{-1}+x^0+x^1)^n$ 中 $x^0$ 的系数（鬼才能发现好吧）。

然后又有 $Lucas$ 定理的一个小推论：

当 $p$ 为质数时，


$$
\begin{aligned}

(a+b)^p &=\sum_{i=0}^{p}\dbinom{p}{i}a^ib^{p-i} \\

&\equiv \sum_{i=0}^p\ [i=0||i=p]a^ib^{p-i} \\

& \equiv a^p+b^p

\end{aligned}
$$


而且这个柿子在多项式的时候同样成立。

$n=q_kp^k+q_{k-1}p^{k-1}...+q_0p^0$

那么 
$$
\begin{aligned}

(x^{-1}+x^0+x^1)^n &=(x^{-1}+x^0+x^1)^{q_kp^k+q_{k-1}p^{k-1}...+q_0p^0}\\

&=(x^{-1}+x^0+x^1)^{q_kp^k+q_{k-1}p^{k-1}...+q_0p^0}\\

&=\prod_{i=0}^{k}(x^{-1}+x^0+x^1)^{q_ip^i}\\

&=\prod_{i=0}^{k}((x^{-1}+x^0+x^1)^{p^i})^{q_i}\\

&\equiv \prod_{i=0}^{k}(x^{-p^i}+1+x^{p^i})^{q_i}

\end{aligned}
$$

然后就可以愉快的暴算了。


```cpp
inline int ksm(int a,int b,int p){
    int res=1;
    while(b){
        if(b&1)res=res*a%p;
        a=a*a%p;
        b>>=1;
    }
    return res;
}
int fac[N],inv[N];
inline int C(int n,int m,int p){
	if(n<m) return 0;
	return fac[n]*inv[m]%p*inv[n-m]%p;
}
inline int lucas(int n,int m,int p){
	if(n<m) return 0;
	if(!n) return 1;
	return lucas(n/p,m/p,p)*C(n%p,m%p,p)%p;
}
int n,p;
inline void init(){
    fac[0]=inv[0]=1;
    up(i,1,p+10){
        fac[i]=fac[i-1]*i%p;
        inv[i]=ksm(fac[i],p-2,p);
    }
}
vector<int>num;
inline int calc (){
	for(;n;n/=p)num.push_back(n%p);
	int ret = 1,tmp;
	for(auto x:num){
		tmp=0;
		up(j,0,x/2) {
			tmp=(tmp+lucas(x,j,p)*lucas(x-j,j,p))%p;
		}
		ret=ret*tmp %p;
	}
	return ret;
}
signed main() {
    //freopen("vote.in","r",stdin);
    //freopen("vote.out","w",stdout);
    cin>>n>>p;
    int t=ksm(3,n,p);
    init();
    int res=calc();
    int ans=(t-res+p)*inv[2]%p;
    cout<<ans<<endl;
    return 0;
}
```

## T4



