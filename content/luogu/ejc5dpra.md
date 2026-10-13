## 定义

离散对数是一个给定的整数满足以下方程

$$a^x\equiv b(\mod p)$$

记作 $x=\log_ab$。

通常情况下，我们把这个叫做阶，记作 $\operatorname{ind}_ab$。

当然，离散对数不一定存在，如  $2^x\equiv 3(\mod 7)$的$x$不存在。

## BSGS

当 $\gcd(a,p)=1$ 时，我们有欧拉定理 $a^{\phi(p)}\equiv 1(\mod p)$

所以 $a^k$ 最多只有$\phi(p)$ 种取值，即$a^{x}\equiv a^{x\mod \phi(p)}(\mod p)$。

令 $x=A\left\lceil\sqrt{p}\right\rceil-B$，其中$0\le A,B\le \left\lceil\sqrt{p}\right\rceil$。

$a^{A\left\lceil\sqrt{p}\right\rceil}\equiv ba^B(\mod p)$。

我们已知$a,b$，所以我们可以算出右边柿子的所有取值。

然后暴力枚举就行。

```cpp

inline int ksm(int a, int b, int m) {
    int res=1;
    for(;b;b>>=1,a=a*a%m)if(b&1)res=res*a%m;
    return res;
}
inline int exgcd(int a, int b, int &x, int &y) {
    if (b == 0) {
        x=1;y=0;
        return a;
    }
    int d=exgcd(b, a % b, y, x);
    y-=a/b*x;
    return d;
}
unordered_map<int,int> mp;
inline int bsgs(int a, int b, int p) {
    int len=sqrt(p)+1;
	mp.clear();
    int base=ksm(a,len,p),val=base;
    for (int i = len; i < p; i += len) {
        if (!mp.count(val))mp[val] = i;
        val=val*base%p;
    }
    int ret=0x7f7f7f7f7f7f7f7f;
    val=b;
    for (int i = 0;i<len;i++) {
        if (mp.count(val)){
            ret = min(ret, mp[val] - i);
        }
        val = val * a % p;
    }
    return ret;
}
```




## EXBSGS