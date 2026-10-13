### [You Are Given a WASD-string... ](https://www.luogu.com.cn/problem/CF1202C)

看到这道题 第一反应是行列减一。
原本面积是 $a\times b$,答案应该是 $(a-1)\times b,a\times(b-1)$.

然而这个结论是错误的。

但是考虑这样一个操作序列 `ADAD` 原本是 $1×2$，但任意添加操作之后并不能让权值变为$ 0×2$，甚至不能变为 $1×1$。

那么变化的位置只能是 **一个最值最后一次出现与另一个最值第一次出现** 之间。

```cpp
int n;
int sum[N],sum2[N];
inline bool check(int l,int r){
  for(int i=l+1;i<=r;++i)if(sum[i]!=sum[l])return true;
  return false;
}
inline bool check2(int l,int r){
  for(int i=l+1;i<=r;++i)if(sum2[i]!=sum2[l])return true;
  return false;
}
string s;
signed main() { 
	int T=read();
	while(T--){
		cin>>s;
		n=s.size();s=" "+s;
		int maxl=0,maxl2=0,minl=0,minl2=0;
		up(i,1,n){
      		sum[i]=sum[i-1];
      		if(s[i]=='A')--sum[i];
      		if(s[i]=='D')++sum[i];
      		maxl=max(maxl,sum[i]);minl=min(minl,sum[i]);
      		sum2[i]=sum2[i-1];
      		if(s[i]=='S')--sum2[i];
      		if(s[i]=='W')++sum2[i];
      		maxl2=max(maxl2,sum2[i]);minl2=min(minl2,sum2[i]);
		}
    	int l=1e14,r=-1e14,l2=1e14,r2=-1e14;
    	for(int i=0;i<=n;++i){
      		if(sum[i]==minl)l=min(l,i),r=max(r,i);
      		if(sum[i]==maxl)l2=min(l2,i),r2=max(r2,i);
    	}
    	int tot=(maxl2-minl2+1)*(maxl-minl+1),ans=tot;
    	if((l>r2||r<l2)&&(check(r2,l-1)||check(r,l2-1)))ans=min(ans,tot-(maxl2-minl2+1));
    	l=l2=1e14;r=r2=-1e14;
    	up(i,0,n) {
      		if(sum2[i]==minl2)l=min(l,i),r=max(r,i);
      		if(sum2[i]==maxl2)l2=min(l2,i),r2=max(r2,i);
    	}
    	if((l>r2||l2>r)&&(check2(r2,l-1)||check2(r,l2-1)))ans=min(ans,tot-(maxl-minl+1));
    	cout<<ans<<endl;
	}
    return 0;
}
```

### [String](https://www.luogu.com.cn/problem/CF128B)

蛮有意思的，本以为要用后缀数组等高级算法，没想到最大堆给艹过去了。

```cpp
string ss;
struct node{
    int l,r;
    bool operator<(const node &y)const{
        for(int k=0;k<=r-l;k++){
            int i=l+k,j=y.l+k;
            if(j>y.r) return 1;
            if(ss[i]!=ss[j]) return ss[i]>ss[j];
        }
        return 0;
    }
};
priority_queue<node> q;

int k;
signed main(){
    cin>>ss>>k;
    for(int i=0;i<ss.length();i++){
       q.push({i,i});
    }
    up(i,1,k-1){
        node u=q.top();q.pop();
        if(u.r<ss.length()-1){
          	u.r++;
            q.push(u);
        }
        if(q.empty()){
            printf("No such line.");
            return 0;
        }
    }
    for(int i=q.top().l;i<=q.top().r;i++)cout<<ss[i];
    return 0;
}
```

###  [Grime Zoo](https://www.luogu.com.cn/problem/CF1411D)

一个显然的结论，`?`中一定有一个分界点，在这个点之前全部填`1`,之后全部填`0`。

```cpp
int x,y,n;
char s[N];
int f[N], g[N], Pre[N], Suf[N];
signed main(){
	scanf("%s",s+1);
	x=read();y=read();
	n=strlen(s+1);
	if(x < y) {
		swap(x, y);
		up(i,1,n) s[i] ^= isdigit(s[i]);
	}
	up(i,1,n){
		if(s[i]=='0')f[i]=f[i-1]+y*Pre[i-1];
		else f[i]=f[i-1]+x*(i-1-Pre[i-1]);
		Pre[i]=Pre[i-1]+(s[i]!='0');
	}
	dn(i,n,1){
		if(s[i]=='1')g[i]=g[i+1]+y*Suf[i + 1];
		else g[i] = g[i + 1] + x * (n - i - Suf[i + 1]);
		Suf[i] = Suf[i + 1] + (s[i] != '1');
	}
	int res = 1e18;
	up(i,0,n)res=min(res,f[i] + g[i + 1] + x * (i - Pre[i]) * (n - i - Suf[i + 1])+ y * Pre[i] * Suf[i + 1]);
	printf("%lld\n", res);
	return 0;
}
```

### [Video Cards ](https://www.luogu.com.cn/problem/CF731F)

柿子化简：

$$\max_{k=1}^{n}\sum(a_i-a_i\mod a_k)=\max_{k=1}^{n}a_k\times\sum(a_i/a_k)$$

考虑枚举 $k$,然后快速算出 $\sum(a_i/a_k)$。

开个桶来维护前缀和。

```cpp

int n;
int a[N],b[N],maxl,ans;
bool vis[N];
signed main(){
	n=read();
    up(i,1,n)a[i]=read();
    sort(a+1,a+1+n);
    up(i,1,n)b[a[i]]++;
    maxl=a[n];
    up(i,1,maxl)b[i]+=b[i-1];
    up(i,1,n){
        if(vis[a[i]])continue;
        for(int j=a[i];j<=maxl;j+=a[i])vis[j]=1;
        int cnt=0;
        for(int j=a[i];j<=maxl-a[i];j+=a[i])cnt=cnt+(b[j+a[i]-1]-b[j-1])*j;
		cnt+=(b[maxl]-b[maxl/a[i]*a[i]-1])*(maxl/a[i])*a[i];
        ans=max(ans,cnt);
    }
    cout<<ans;
	return 0;
}
```
