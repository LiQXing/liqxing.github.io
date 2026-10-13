难点：预处理,  $dp$；

技巧：

$1.$数位拆解

$2.$建树

------------
# [题目1](http://ybt.ssoier.cn:8088/problem_show.php?pid=1585)

### 分析：

分析一下题意，即将$[X,Y]$中的数化为$b$进制下的数字，求数字在$b$进制下有$k$个1的
数字有几个；

![分析](https://cdn.luogu.com.cn/upload/image_hosting/lyn494ka.png)

```cpp

#include<bits/stdc++.h>
using namespace std;
#define int long long
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int f[50][50];
int k,b;
void init(){//预处理
	for(int i=0;i<=40;i++){
		for(int j=0;j<=i;j++){
			if(!j)f[i][j]=1;
			else f[i][j]=f[i-1][j]+f[i-1][j-1];//组合数
		}
	}
}
int dp(int n){
	if(!n)return 0;
	vector<int>nums;
	while(n)nums.push_back(n%b),n/=b;//把n转化为b进制
	int res=0;
	int last=0;//记录上一个x
	for(int i=nums.size()-1;i>=0;i--){
		int x=nums[i];
		if(x){
			res+=f[i][k-last];
			if(x>1){
				if(k-last-1>=0)res+=f[i][k-last-1];
				break;
			}
			else{
				last++;
				if(last>k)break;
			}
		}
		if(!i&&last==k)res++;	
	}
	return res;
}
signed main(){
	int n,m;
	n=read();m=read();
	k=read();b=read();
	init();
	printf("%lld",dp(m)-dp(n-1));
    return 0;
}
```
# [题目2](http://ybt.ssoier.cn:8088/problem_show.php?pid=1586)

------------
分析：首先进行预处理，一位数都是不降数，从此进行$DP$，预处理；


![分析](https://cdn.luogu.com.cn/upload/image_hosting/y787iab4.png)

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int f[50][50];
int k,b;
void init(){
	for(int i=0;i<=9;i++)f[1][i]=1;
	for(int i=2;i<=20;i++){
		for(int j=0;j<=9;j++){
			for(int k=j;k<=9;k++){
				f[i][j]+=f[i-1][k];
			}
		}
	}
}

int dp(int n){
	if(!n)return 1;
	vector<int>nums;
	while(n)nums.push_back(n%10),n/=10;
	int res=0;
	int last=0;
	for(int i=nums.size()-1;i>=0;i--){
		int x=nums[i];
		for(int j=last;j<x;j++){
			res+=f[i+1][j];//因为最低位是1，所以需要+1；
		}
		if(x<last)break;
		last=x;
		if(!i)res++;//树最右边的情况	
	}
	return res;
}
signed main(){
	int l,r;
	init();
	while(cin>>l>>r){
		cout<<dp(r)-dp(l-1)<<endl;
	}
    return 0;
}
```
------------
# [题目3](https://www.luogu.com.cn/problem/P2657)

分析：无，与前题相似；

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
------------
# [题目4](http://ybt.ssoier.cn:8088/problem_show.php?pid=1588)

分析：因为是求各位数字之和，所以要将数组扩展一维，$f[i,j,k]$表示 $i$ 位，第 $i$ 位是 $j$ ，尾部之和 $mod N=k$；


![分析](https://cdn.luogu.com.cn/upload/image_hosting/p2gtq2gd.png)

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int f[150][150][150];//数组范围要注意
int m;
int mod(int x,int y){
	return (x%y+y)%y;
}
void init(){
	memset(f,0,sizeof f);
	for(int i=0;i<=9;i++)f[1][i][i%m]++;
	
	for(int i=2;i<=20;i++){
		for(int j=0;j<=9;j++){
			for(int k=0;k<m;k++){
				for(int x=0;x<=9;x++){
					f[i][j][k]+=f[i-1][x][mod(k-j,m)];	
				}
			}
		}
	}
}

int dp(int n){
	if(!n)return 1;
	vector<int>nums;
	while(n)nums.push_back(n%10),n/=10;
	int res=0;int last=0;
	for(int i=nums.size()-1;i>=0;i--){
		int x=nums[i];
		for(int j=0;j<x;j++){
			res+=f[i+1][j][mod(-last,m)];
		}
		last+=x;
		if(!i&&last%m==0)res++;	
	}
	return res;
}
signed main(){
	int l,r;
	while(cin>>l>>r>>m&&l&&r){
		init();
		cout<<dp(r)-dp(l-1)<<endl;
	}
    return 0;
}
```

------------

