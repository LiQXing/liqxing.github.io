$T1$

其实这个题目之前见过类似的。

[上帝与集合的正确用法](https://www.luogu.com.cn/problem/P4139)

都需要用到扩展欧拉定理。

$$a^b\equiv\begin{cases}
a^{b \mod \phi(m)}, & \gcd(a,m)=1 \\
a^b, & b<\phi(m) \\
a^{(b\mod \phi(m))+\phi(m)},& \gcd(a,m)\neq 1 ,b\ge\phi(m)\\
\end{cases}\mod m$$

如果 $b<\phi(m)$,这个东西就不能降幂了，其实在这两道题里欧拉定理就是用来降幂的。

在本题中，因为 $p$ 无穷多。

所以一定有$a^b\equiv a^{(b\mod \phi(m))+\phi(m)}\mod m$。

题目求 $p^{p^{p^{p...}}}$.

在一层层的递归中，$p $ 一遍遍的被求其 $\phi$ 值，最终必定会降到 1。

这就是本题的解决方法。

另外提一点关于 $euler$ 函数的证明。

$\phi(n)=n(1-\dfrac{1}{p_1})(1-\dfrac{1}{p_2})....(1-\dfrac{1}{p_k})$。

```cpp
int p,m,fac=1;
inline int euler(int x){
    int ans=x;
    up(i,2,sqrt(x)){
        if(x%i==0){
            ans=ans/i*(i-1);
            while(x%i==0)x/=i;
        }
    }
    if(ans>1)ans=ans/x*(x-1);
    return ans;
}
inline int ksm(int a,int b,int mod){
    i128 res=1;
    i128 ia=a;
    while(b){
        if(b&1)res=(res*ia)%mod;
        ia=ia*ia%mod;
        b>>=1;
    }
    return res;
}
inline int dfs(int a,int mod){
    if(mod==1)return 0;
    int phi=euler(mod);
    return ksm(a,phi,mod)*ksm(a,dfs(a,phi),mod)%mod;
}
signed main(){
    p=read();m=read();
    up(i,2,m)fac*=i;
    write(dfs(p,fac)%fac,1);
    return 0;
}
```

$T2$

有一个奇妙的结论。

$\begin{vmatrix} \gcd(a_1,a_1),\gcd(a_1,a_2),...\gcd(a_1,a_n)\\\gcd(a_2,a_1),\gcd(a_2,a_2),...\gcd(a_2,a_n)\\
...\\
\gcd(a_n,a_1),\gcd(a_n,a_2),...\gcd(a_n,a_n)\end{vmatrix}=\phi(a_1)\phi(a_2)...\phi(a_n)$

code
:

```cpp
inline int euler(int x){
    int ans=x;
    up(i,2,sqrt(x+0.5)){
        if(x%i==0){
            ans=ans/i*(i-1);
            while(x%i==0)x/=i;
        }
    }
    if(x>1)ans=ans/x*(x-1);
    return ans;
}
int n;
signed main(){
    while(scanf("%lld",&n)==1){
        int ans=1,x;
        up(i,1,n){
            x=read();
            ans*=euler(x);
            ans%=mod;
        }
        write(ans,1);
    }
    return 0;
}

```

$T3$

```cpp
鸽
```

[$T4$](https://www.luogu.com.cn/problem/P1397)


$$\begin{aligned}
F[1, 1] &= 1 \\
F[i, j] &=a\times F[i, j-1]+b, &j\neq 1 \\
F[i, 1] &=c\times F[i-1, m]+d, &i\neq 1 \\
\end{aligned}$$

看到这里以为是个非常简单的题，直到看见数据范围。

$1 \le n,m \le 10^{1\,000\,000}$，$1 \le a,b,c,d \le 10^9$ 。

被这个数据范围创死了（悲）。

首先，这个题看着就像矩阵快速幂。

构造 

$F(n)=[f(n),f(n+1)] $

$F(n+1)=[f(n+1),f(n+2)]$

$F(n)\times A=F(n+1)$

$F(1)= \begin{matrix} 1,1\end{matrix}$

初始矩阵为

所以 

$A_1=\begin{bmatrix} 0,b\\1,a\end{bmatrix}$

同样的,

$A_2=\begin{bmatrix} 0,d\\1,c\end{bmatrix}$

到最后 $F(1)\times A_1^{m-1}(A_2A_1^{m-1})^{n-1}$

又有欧拉定理

$$a^{n \mod  \phi(p)}\equiv 1 (\mod p)$$

来读入 $n,m$。

注意当 $a=1$ 时并不成立。

[$T5$](https://www.luogu.com.cn/problem/CF687B)

已知：

$$\begin{cases} x \equiv b_1\ ({\rm mod}\ a_1) \\ x\equiv b_2\ ({\rm mod}\ a_2) \\ ... \\ x \equiv b_n\ ({\rm mod}\ a_n)\end{cases}$$

看起来是非常困难的 excrt，然鹅，题目只让你求能否推出$x\mod k$。

这就肥肠简单了。

判断 $\lcm$能否被k整除就行了。

(代码太简单所以就不放了)。

[$T6$](https://www.luogu.com.cn/problem/CF906D)

一眼看过去，肥肠典型的欧拉降幂。

再看一眼，时间是 $O(n^2)$，会炸掉。

于是考虑用 map 把每一个 $\phi$ 都存下来。

最大的重点

这里要注意，如果中途出现了$\ge \mod$的情况我们要加上$\mod$，以满足欧拉降幂的公式


```cpp
int n,p,m;
unordered_map<int,int>phy;
inline int euler(int x){
    int t=x;
    if(phy.find(x)!=phy.end())return phy[x];
    int ans=x;
    up(i,2,sqrt(x)){
        if(x%i==0){
            while(x%i==0)x/=i;
            ans=ans/i*(i-1);
        }
    }
    if(x>1)ans=ans/x*(x-1);
    phy[t]=ans;
    return ans;
}
inline int mo(int x,int mod){
	return x<mod?x:(x%mod+mod);
}
inline int ksm(int a,int b,int mod){
	int ret=1;
	while(b){
		if(b&1) ret=mo(ret*a,mod);
		a=mo(a*a,mod);b>>=1;
	}
	return ret;
}
int a[N];
inline int dfs(int l,int r,int mod){
    if(l==r||mod==1)return mo(a[l],mod);
    int phi=euler(mod);
    return ksm(a[l],dfs(l+1,r,phi),mod);
}
signed main(){
    n=read();p=read();
    up(i,1,n)a[i]=read();
    m=read();
    int l,r;
    while(m--){
        l=read();r=read();
        write(dfs(l,r,p)%p,1);
    }
    return 0;
}
```
$T7$
```cpp
inline int ksm(int a,int b){
    int res=1;
    while(b){
        if(b&1)res=(res*a)%mod;
        a=(a*a)%mod;
        b>>=1;
    }
    return res;
}
int p[30],k[30];
inline void clear(){
    memset(p,0,sizeof p);
    memset(k,0,sizeof k);
}
signed main(){
    int T=read();
    while(T--){
        clear();
        n=read();
        up(i,1,n){
            p[i]=read();
            k[i]=read();
        }
        int ans=1;
        up(i,1,n){
            int t=ksm(p[i],k[i]-1);
            ans=ans*t%mod;
            t=(p[i]+p[i]*k[i]%mod-k[i]%mod+mod)%mod;
            ans=ans*t%mod;
        }
        write(ans,1);
    }
    return 0;
}
```
$T8$
```cpp
int n,k;
int a[N];
signed main(){
    n=read();k=read();
    up(i,1,n)a[i]=read();
    int m=a[1];
	up(i,2,n){
		if(m==1)break;
		if(a[i]>m)m=__gcd(a[i],m);
		else m=__gcd(m,a[i]);
	}
	if(m>k)m=__gcd(m,k);
	else m=gcd(k,m);
	int ans=k/m;
	printf("%lld\n",ans);
	for(int i=0;i<ans;i++){
		printf("%lld ",i*m);
	}
    return 0;
}
```