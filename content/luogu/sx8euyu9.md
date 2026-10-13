##  T1

就是求 $\phi$。
```cpp
int n;
inline int get_phi(int x){
	int res=x,tmp=x;
	if(x==1)return 1;
	for(int i = 2; i * i<=x; i ++) {
		if(tmp % i == 0) {
			res = res / i * (i - 1);
			while(tmp % i == 0) tmp /= i;
		}
	}
	if(tmp > 1) res = res / tmp * (tmp - 1);
	return res;
}
signed main(){
    freopen("letter.in","r",stdin);
    freopen("letter.out","w",stdout);
	n=read();
	cout<<get_phi(n);
	return 0;
}
```

## T2

枚举质因子个数。

简单 $dfs$，不要看错数据。

```cpp
int n;
int val[]={0,2,3,5,7,11,13,17,19,23};
inline int ksm(int a,int b){
    int res=1;
    while(b){
        if(b&1)res=res*a;
        a=a*a;
        b>>=1;
    }
    return res;
}
int ans;
int maxl;
inline void dfs(int u,int now,int lim,int tt){
    if(now>n)return;
    if(u==10){
        if(ans<=tt){
            if(ans==tt)maxl=min(maxl,now);
            else {
                ans=tt;
                maxl=now;
            }
        }
        return;
    }
    up(i,0,lim){
        dfs(u+1,now*ksm(val[u],i),min(i,lim),tt*(i+1));
    }
}
signed main(){
    n=read();
    dfs(1,1,6,1);
    cout<<maxl;
    return 0;
}
```
## T3

简单01tire

数组要开够大。

```cpp
int n;
inline int ksm(int a,int b){
   int res=1;
   while(b){
      if(b&1)res=res*a%mod;
      a=a*a%mod;
      b>>=1;
   }
   return res;
}
int a[N];
int tr[N][2];
int cnt;
inline void insert(int x){
   int p=0;
   for(int i=24;i>=0;i--){
      int ch=(x>>i)&1;;
      if(!tr[p][ch])tr[p][ch]=++cnt;
      p=tr[p][ch];
   }
}
inline int ask(int x){
   int p=0,res=0;
   for(int i=24;i>=0;i--){
      int ch=(x>>i)&1;
      if(!tr[p][ch^1])p=tr[p][ch];
      else p=tr[p][ch^1],res+=(1<<i);
   }
   return res;
}
int k,b,p;
signed main(){
    //freopen("friend.in","r",stdin);
    //freopen("friend.out","w",stdout);
   n=read();
   k=read();b=read();p=read();
   a[1]=p;
   insert(a[1]);
   up(i,2,n){
      a[i]=(k*a[i-1]+b)%mod;
      insert(a[i]);
   }
   int ans=0;
   up(i,1,n){
      ans=(ask(a[i])*ksm(3,i-1)%mod+ans)%mod;
   }
   cout<<ans;
	return 0;
}
```