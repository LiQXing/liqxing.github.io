## $T1$

sbsbsbsbsbsbsbsbsbsbsb。

最难的一道题。

因为边的权值小于 $30$。
所以可以暴力枚举最大的边权。

然后让这条边的次数尽可能的多。

把联通块分成多个，使得匹配最多。

另 $x=\max \{a_i\},s=\sum a_i$

如果 $x\times 2>s$，有 $s-x$ 个匹配。

否则,有 $s/2$ 个匹配。

那么就一次一次删点就完了。

```cpp
int n,m,k;
int ans;
inline int ksm(int a,int b){
    int res=1;
    while(b){
        if(b&1)res=res*a%mod;
        a=a*a%mod;
        b>>=1;
    }
    return res;
}
vector<pii>g[N];
vector<int>p[N];
bool vis[N];
int del[N],cnt,lim;
inline void dfs(int u){
    vis[u]=1;
    p[cnt].push_back(u);
    for(auto [v,w]:g[u]){
        if(vis[v]||del[v]||w>lim)continue;
        dfs(v);
    }
}
int ex;
signed main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);cout.tie(0);
    cin>>n;
    int u,v,w;
    up(i,1,n-1){
        cin>>u>>v>>w;
        g[u].push_back({v,w});
        g[v].push_back({u,w});
    }    
    dn(k,30,0){
        memset(vis,0,sizeof vis);
        cnt=0;lim=k-1;
        up(i,1,n){
            if(!del[i]&&!vis[i]){
                cnt++;
                p[cnt].clear();
                dfs(i);
            }
        }
        int maxl=0,pos=0,tot=0;
		up(i,1,cnt){
			int u=p[i].size();
			if(u>maxl){
				maxl=u;
                pos=i;
			}
			tot+=u;
		}
        if((maxl-ex)*2<=tot-ex){
			ans=(ans+ksm(n,k)*(tot-ex-1))%mod;
			break;
		}
		tot-=ex;
        maxl-=ex;
		ans=(ans+2*ksm(n,k)*(tot-maxl))%mod;
		up(i,1,cnt){
			if(i==pos) continue;
			for(auto u:p[i]){
				del[u]=1;
			}
		}
		ex+=tot-maxl;
    }
    cout<<ans;
    return 0;
}
```

## $T2$

sb 模拟。

```cpp
inline bool check(string a){
    string num1,num2,num3,op;
    int n1=0,n2=0,n3=0;
    up(i,0,a.size()-1){
        if(a[i]>='0'&&a[i]<='9'){
            num1+=a[i];
        }
        else break;
    }
    op=a[num1.size()];
    if(op[0]!='+'&&op[0]!='-'&&op[0]!='*'&&op[0]!='/'){
        //cerr<<"### 1"<<endl;
        return 0;
    }
    up(i,num1.size()+1,a.size()-1){
        if(a[i]>='0'&&a[i]<='9'){
            num2+=a[i];
        }
        else break;
    }
    if(a[num1.size()+num2.size()+1]!='='){
        //cerr<<"### 2"<<endl;
        return 0;
    }
    up(i,num1.size()+num2.size()+2,a.size()-1){
        if(a[i]>='0'&&a[i]<='9'){
            num3+=a[i];
        }
        else break;
    }
    if(num1.size()+num2.size()+num3.size()+2!=a.size()){
        //cerr<<"### 3"<<endl;
        return 0;
    }
    //cerr<<num1<<op<<num2<<"="<<num3<<endl;
    if(!num1.size()||!num2.size()||!num3.size()){
        return 0;
    }
    if(num1[0]=='0'||num2[0]=='0'||num3[0]=='0'){
        return 0;
    }
    if(num1.size()>9||num2.size()>9||num3.size()>9){
        return 0;
    }
    up(i,0,num1.size()-1){
        n1=n1*10+num1[i]-'0';
    }
    up(i,0,num2.size()-1){
        n2=n2*10+num2[i]-'0';
    }
    up(i,0,num3.size()-1){
        n3=n3*10+num3[i]-'0';
    }
    //cerr<<n1<<" "<<n2<<" "<<n3<<endl;
    if(op[0]=='+'){
        if(n1+n2==n3){
            return 1;
        }
    }
    if(op[0]=='-'){
        if(n1-n2==n3){
            return 1;
        }
    }
    if(op[0]=='*'){
        if(n1*n2==n3){
            return 1;
        }
    }
    if(op[0]=='/'){
        if(n1/n2==n3&&__gcd(n1,n2)==n2){
            return 1;
        }
    }
    return 0;
}
string a,num1,num2,num3,op;
int n1,n2,n3;
inline void corr(){
    up(i,0,a.size()-1){
        if(a[i]>='0'&&a[i]<='9'){
            num1+=a[i];
        }
        else break;
    }
    op=a[num1.size()];
    if(op[0]!='+'&&op[0]!='-'&&op[0]!='*'&&op[0]!='/'){
        //cout<<"### 1"<<endl;
        cout<<"Format Error"<<endl;
        exit(0);
    }
    up(i,num1.size()+1,a.size()-1){
        if(a[i]>='0'&&a[i]<='9'){
            num2+=a[i];
        }
        else break;
    }
    if(a[num1.size()+num2.size()+1]!='='){
        //cout<<"### 2"<<endl;
        cout<<"Format Error"<<endl;
        exit(0);
    }
    up(i,num1.size()+num2.size()+2,a.size()-1){
        if(a[i]>='0'&&a[i]<='9'){
            num3+=a[i];
        }
        else break;
    }
    if(num1.size()+num2.size()+num3.size()+2!=a.size()){
        //cout<<"### 3"<<endl;
        cout<<"Format Error"<<endl;
        exit(0);
    }
    //cout<<num1<<op<<num2<<"="<<num3<<endl;
    if(!num1.size()||!num2.size()||!num3.size()){
        cout<<"Format Error"<<endl;
        exit(0);
    }
    if(num1[0]=='0'||num2[0]=='0'||num3[0]=='0'){
        cout<<"Format Error"<<endl;
        exit(0);
    }
    if(num1.size()>9||num2.size()>9||num3.size()>9){
        cout<<"Format Error"<<endl;
        exit(0);
    }
    up(i,0,num1.size()-1){
        n1=n1*10+num1[i]-'0';
    }
    up(i,0,num2.size()-1){
        n2=n2*10+num2[i]-'0';
    }
    up(i,0,num3.size()-1){
        n3=n3*10+num3[i]-'0';
    }
    //cout<<n1<<" "<<n2<<" "<<n3<<endl;
    if(op[0]=='+'){
        if(n1+n2==n3){
            cout<<"Correct"<<endl;
            exit(0);
        }
    }
    if(op[0]=='-'){
        if(n1-n2==n3){
            cout<<"Correct"<<endl;
            exit(0);
        }
    }
    if(op[0]=='*'){
        if(n1*n2==n3){
            cout<<"Correct"<<endl;
            exit(0);
        }
    }
    if(op[0]=='/'){
        if(n1/n2==n3&&__gcd(n1,n2)==n2){
            cout<<"Correct"<<endl;
            exit(0);
        }
    }
}
char d[]={'0','1','2','3','4','5','6','7','8','9','+','-','*','/','='};
string ans="~~~~~~~~~~~~";
inline void change2(){
    up(i,0,a.size()-1){
        up(j,0,14){
            up(k,i+1,a.size()-1){
                up(l,0,14){
                    string b=a;
                    b[i]=d[j];
                    b[k]=d[l];
                    if(check(b))ans=min(ans,b);
                }
            }
        }
    }
}
signed main() {
   
    ios_base::sync_with_stdio(0);
    cin.tie(0);cout.tie(0);
    cin>>a;
    corr();
    change2();
    if(ans[0]=='~'){
        cout<<"Math Error"<<endl;
    }
    else{
        cout<<"Typo: "<<a<<" instead of "<<ans;
    }
    return 0;
}
```

## $T3$

有意思的一道题。

首先如果是`| ^` 那么一定是把所有祖先都选上。

`|`是显然的，对于`^`，有 $a\oplus c=a\oplus b\oplus b\oplus c\le a\oplus b+b\oplus c$

至于`&`

可以枚举最高位 $1$ 为 $k$ 的数，只用考虑最近的点就行了，有点像树上背包。

```cpp
int n,w[N];
string a;
int fa[N];
vector<int>g[N];
int f[N],nxt[35];
inline void dfs(int u){
    int tmp[35];
	memcpy(tmp, nxt, sizeof tmp);
    for (int j=0;j<31; j ++) {
		if (nxt[j])f[u]=max(f[u],f[nxt[j]]+(w[nxt[j]]&w[u]));
		if ((w[u]>>j)&1)nxt[j]=u;
	}
	for (auto v:g[u]){
		dfs(v);
	}
    memcpy(nxt, tmp, sizeof nxt);
}
int ans;
inline void dfs2(int u,int from){
    ans=(ans+u*(f[u]+w[u]))%mod;
    for(auto v:g[u]){
        if(a=="OR")f[v]=(f[u]+(w[u]|w[v]))%mod; 
		if(a=="XOR")f[v]=(f[u]+(w[u]^w[v]))%mod;
        dfs2(v,u);
    }
}
signed main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);cout.tie(0);
    cin>>n>>a;
    up(i,1,n)cin>>w[i];
    up(i,2,n){
        cin>>fa[i];
        g[fa[i]].push_back(i);
    }
    if(a=="AND"){
        dfs(1);
        up(i,1,n){
            ans=(ans+i*((f[i]+w[i])%mod)%mod)%mod; 
        }
        cout<<ans;
        return 0;
    }
    dfs2(1,0);
    cout<<ans;
    return 0;
}

```
## $T4$

$f[i][j]$ 表示 $i$ 个数，和为 $j$。
显然：

$f[i][j]=f[i-1][j-i]+f[i-1][j-1]$

设  $a_i$ 出现了 $x$ 次。

贡献为 $a_i^m\times f[i-x][n-x\times a_i]$ 

```cpp
int n,m,k;
int ans;
inline int ksm(int a,int b){
    int res=1;
    while(b){
        if(b&1)res=res*a%mod;
        a=a*a%mod;
        b>>=1;
    }
    return res;
}
int f[5050][5050];
signed main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);cout.tie(0);
    cin>>n>>k>>m;
    f[0][0]=1;
    up(i,1,k){
        up(j,i,n){
            f[i][j]=(f[i][j-i]+f[i-1][j-1])%mod;
        }
    }
    int ans=0;
	up(i,1,n) {
		int s=0;
		for (int j=1;j<=k&&j*i<=n;j++)s=(s+f[k-j][n-i*j])%mod;
		ans=(ans+s*ksm(i,m)%mod)%mod;
	}
	cout<<ans;
    return 0;
}

```