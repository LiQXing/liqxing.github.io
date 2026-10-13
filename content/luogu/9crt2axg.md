## [Greg and Graph](https://www.luogu.com.cn/problem/CF295B)
  
正向思路是按照题意每次删除点$x_i$​，但 Floyd 不支持删除点，并且这样做会很麻烦：每到一个点 $x_i$​就要做一次复杂度为$O(n^3)$ 的 Floyd，整体复杂度为$O(n^4)$，也会超时。

我们可以反过来想：每次加入一个点，求出加入后每一对点最短路权值的和。
具体来说，我们倒着枚举删除的点，用这个点来松弛其他的点，然后统计目前存在的点的答案。
为什么是正确的呢？因为 Floyd 对松弛点的顺序没有要求。

```cpp
int f[N][N];
int del[N];
bool tag[N];
int  ans[N];
int n;
signed main(){
    n=read();
	up(i,1,n){
		up(j,1,n){
			f[i][j]=read();
		}
	}
	up(i,1,n)del[i]=read();
    dn(p,n,1){
        int k = del[p];
        tag[k] = true;
        up(i,1,n){
            up(j,1,n){
                f[i][j]=min(f[i][j],f[i][k] + f[k][j]);
                if(tag[i] && tag[j]) ans[p] += f[i][j];
            }
        }
    }
   	up(i,1,n)cout<<ans[i]<<" ";
    return 0;
}
```
## [Rectangle Puzzle II](https://www.luogu.com.cn/problem/CF303B)

  
像KMP 那样，造一个 nxt 数组，然后再弄一个 cnt 数组。

其中 $cnt_i$​ 表示从 $c_i$​ 开始匹配，把 $a$ 串扫一遍有几组匹配， $nxt_i$​ 表示 $c_i$​ 匹配完一个 $a$ 到了 $c$ 的哪一位。

然后从 1 到 $b$ ，每次跳 $nxt$ ， $ans+=cnt$ 即可。

##  [Jeff and Furik](https://www.luogu.com.cn/problem/CF351B)

一个人一次操作减少一个逆序对，一个人二分之一概率减少一个逆序对。

考虑将Jeff和Fruik当成一整轮一起操作，那么一轮操作中又 $0.5$的概率减少两个逆序对，$0.5$ 的概率使逆序对个数不变。

当前是 $dp[i]=dp[i-1]+1$,不然$dp[i]=\dfrac{1}{2}(dp[i-1]+1)+\dfrac{1}{2}(dp[i]+2)$

$$dp[i]=dp[i-1]+3$$

 ## [Book of Evil](https://www.luogu.com.cn/problem/CF337D)
只用求出有鬼的直径就行了。

## [Apple Tree](https://www.luogu.com.cn/problem/CF348B)

1.  对于一个结点，它的值是它的所有子树的值的和，又由于题目要求子树所含的苹果数相同，所以，结点的值**必须为子树的个数的倍数或者 0**。
2.  为了保证这个结点的子树的合法，此结点的值必须保证**为其子结点所需要的倍数的倍数或者 0**。
3.  由于叶子结点的苹果数只能加不能减，所以每一个结点的最大值为**子结点的最小值乘以子结点的个数。**
## [Lucky Common Subsequence](https://www.luogu.com.cn/problem/CF346B)

暴力DP
-   使用 KMP 预处理出 $S$ 串的 $nxt$ 数组
-   我们知道，$nxt[i]$ 表示$S$ 串的**前 $i$ 个字符**的**最长前后缀**长度。
-   根据 $nxt$ 数组，用 $KMP$ 处理出 $arr[i][ch]$，代表目前已经和 $S$ 串匹配了 $i$ 位，如果下一个字符是 $ch$，那么加上这个字符后，将会和 $S$ 串匹配多少位。
```cpp
string a,b,c,dp[111][111][111],ans;
int f[111];
inline void change(string &a,string b){
    if(a.size()<b.size()) a=b;
}
signed main(){
    cin>>a>>b>>c;
    int la=a.size(),lb=b.size(),lc=c.size();
    int j=0;
    for(int i=1;i<lc;i++){
        while(j>0&&c[i]!=c[j]) j=f[j-1];
        if(c[i]==c[j]) f[i]=++j;
    }
    for(int i=1;i<=la;i++)
        for(int j=1;j<=lb;j++)
            for(int k=0;k<lc;k++){
                if(a[i-1]==b[j-1]){
                    char tmp=a[i-1];
                    int t=k;
                    while(t>0&&tmp!=c[t]) t=f[t-1];
                    if(tmp==c[t]) t++;
                    change(dp[i][j][t],dp[i-1][j-1][k]+tmp);
                }
                change(dp[i][j][k],dp[i-1][j][k]);
                change(dp[i][j][k],dp[i][j-1][k]);
            }
    for(int i=0;i<lc;i++) change(ans,dp[la][lb][i]);
    if(ans.size()==0) puts("0");
    else cout<<ans;
    return 0;
}
```

