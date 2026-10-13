
林语堂曾说过：“绅士写题解当如淑女迷你裙，短为佳。”

----

## [P4933](https://www.luogu.com.cn/problem/P4933)

$$dp[i][a[i]-a[j]]=\sum dp[j][a[i]-a[j]]$$

## [P2758](https://www.luogu.com.cn/problem/P2758)

```cpp
		if(a[i-1]==b[j-1])f[i][j]=f[i-1][j-1];
        else f[i][j]=min(min(f[i-1][j],f[i][j-1]),f[i-1][j-1])+1;
```
## [P1544](https://www.luogu.com.cn/problem/P1544)

$$f[i][j][k]=\max(\max(f[i-1][j-1][k]+a[i][j],f[i-1][j][k]+a[i][j]),\max(f[i-1][j-1][k-1]+3*a[i][j],f[i-1][j][k-1]+3*a[i][j]))$$

记得全部变成最小值。

## [P3205](https://www.luogu.com.cn/problem/P3205)

显然是区间 DP。

默认当一个人的时候是从左侧进入。

考虑当前状态的前一个人时在子区间的左边还是右边。

```cpp
if(a[i]<a[i+1])f[i][j][0]+=f[i+1][j][0];
if(a[i]<a[j])f[i][j][0]+=f[i+1][j][1];
if(a[j]>a[i])f[i][j][1]+=f[i][j-1][0];
if(a[j]>a[j-1])f[i][j][1]+=f[i][j-1][1];
```

## [P1107](https://www.luogu.com.cn/problem/P1107)

$$dp[i][j]=\max(dp[i-1][j]​,dp[i−delta][j]​)$$

## [P1651](https://www.luogu.com.cn/problem/P1651)

另 $dp[i][j]$ 表示到了第 $i$ 块木头，左边比右边高 $j$。

```cpp
	up(i,1,n){
        up(j,0,sum){
            dp[i][j]=max(dp[i-1][j],dp[i-1][j+a[i]]);
            if(j>=a[i]) dp[i][j]=max(dp[i][j],dp[i-1][j-a[i]]+a[i]);
            else dp[i][j]=max(dp[i][j],dp[i-1][a[i]-j]+j);
        }
    }
    if(dp[n][0])  cout<<dp[n][0]<<endl;
```

## [P1489](https://www.luogu.com.cn/problem/P1489)

暴力二维背包，  $x$ 个人 $y$ 点血是否可行。

## [P1373](https://www.luogu.com.cn/problem/P1373)

直接暴力递推。

有一点卡空间。

```cpp
for(int i=1;i<=n;i++){
		for(int j=1;j<=m;j++){
			for(int h=0;h<=k;h++){
				dp[i][j][h][0]=(dp[i][j][h][0]+dp[i-1][j][(h-a[i][j]+k)%k][1])%mod;
				dp[i][j][h][0]=(dp[i][j][h][0]+dp[i][j-1][(h-a[i][j]+k)%k][1])%mod;
				dp[i][j][h][1]=(dp[i][j][h][1]+dp[i-1][j][(h+a[i][j])%k][0])%mod;
				dp[i][j][h][1]=(dp[i][j][h][1]+dp[i][j-1][(h+a[i][j])%k][0])%mod;
			}
		}
	}
```

## [P2339](https://www.luogu.com.cn/problem/P2339)

区间DP。

```cpp
f[1][C][0] = max(a[1].x,a[1].t);
	f[1][C][1] = max(a[C].x,a[C].t);
	for(int i = 1; i <= C; i++){
		for(int j = C; j >= i; j--){
			f[i][j][0] = min(f[i][j][0], max(f[i - 1][j][0] + a[i].x - a[i - 1].x, a[i].t) );
			f[i][j][0] = min(f[i][j][0], max(f[i][j + 1][1] + a[j + 1].x - a[i].x, a[i].t) );
			f[i][j][1] = min(f[i][j][1], max(f[i][j + 1][1] + a[j + 1].x - a[j].x, a[j].t) );
			f[i][j][1] = min(f[i][j][1], max(f[i - 1][j][0] + a[j].x - a[i - 1].x, a[j].t) );
		}
	}

```

## [P2851](https://www.luogu.com.cn/problem/P2851)

比较好像的DP。

店主是完全背包，john 是组合背包。

## [P3080](https://www.luogu.com.cn/problem/P3080)

与关路灯这道题相似。

定义$f[i][j][0/1]$表示当前已经套完了 $i$ 到 $j$ 的牛，然后 第三维表示在左边还是在右边。

```cpp
			f[i][j][0] = min(f[i + 1][j][0] + (d[i + 1] - d[i]) * (i + n - j),
                             f[i + 1][j][1] + (d[j] - d[i]) * (i + n - j));
            f[i][j][1] = min(f[i][j - 1][0] + (d[j] - d[i]) * (i + n - j),
                             f[i][j - 1][1] + (d[j] - d[j - 1]) * (i + n - j));
```