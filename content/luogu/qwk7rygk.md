蛮有意思的模拟题。

题意十分混乱，一会儿出现 $gladiator$，一会儿出现 $weapon$。

不如把它们归类，把与 $atk$ 有关的统称为 $atk$，把与 $def$ 有关的统称为 $def$，把与 $res$ 有关的统称为 $res$。

注意，题目中提到居民不可以出现在外面，所以如果居民人数等于所有物品的总容量，那就不可以交换居民的位置。反之，只要有一个空缺的位置，那么就可以任意分配居民的位置。

当没有空缺的时候，我们只用枚举最多的物品就行了。

如果有空缺，贪心的寻找那种物品可以达到最大的价值。

然后还有一个坑点，最后的情况一定是能够容纳所有居民的，所以我们如果一个物品的容量还有多的，就可以把一个无关的居民加入到这个物品中，这样一定更优。

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long
#define i64 long long
#define ull unsigned long long
#define ldb long double
#define db double
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define lc k<<1
#define rc k<<1|1
#define fi first
#define se second
#define endl '\n'

const int N=2e5+100,M=1e6+100;
const int mod=1e9+7;
const int inf=0x3f3f3f3f;
const ull uinf=1e18+14;

int n,m;
struct node{
    string name,type;
    int atk,def,res,siz;
}a[N];
struct people{
    string name,type;
    int bonus;
    string home;
}p[N];
int sumsiz;
bool vis[N];
signed main(){
    ios_base::sync_with_stdio(0);cin.tie(0);cout.tie(0);
    cin>>n;
    up(i,1,n){
        cin>>a[i].name>>a[i].type>>a[i].atk>>a[i].def>>a[i].res>>a[i].siz;
        if(a[i].type=="weapon")a[i].type="atk";
        else if(a[i].type=="armor")a[i].type="def";
        else if(a[i].type=="orb")a[i].type="res";
        sumsiz+=a[i].siz;
    }
    cin>>m;
    up(i,1,m){
        cin>>p[i].name>>p[i].type>>p[i].bonus>>p[i].home;
        if(p[i].type=="gladiator")p[i].type="atk";
        else if(p[i].type=="sentry")p[i].type="def";
        else if(p[i].type=="physician")p[i].type="res";
    }
    if(sumsiz==m){
        int posatk=0,posdef=0,posres=0,maxatk=-inf,maxdef=-inf,maxres=-inf;
        up(i,1,n){
            if(a[i].type=="atk"){
                int atk=a[i].atk;
                up(j,1,m)if(p[j].home==a[i].name&&p[j].type=="atk")atk+=p[j].bonus;
                if(atk>maxatk){
                    posatk=i;
                    maxatk=atk;
                }
            }
            if(a[i].type=="def"){
                int def=a[i].def;
                up(j,1,m)if(p[j].home==a[i].name&&p[j].type=="def")def+=p[j].bonus;                
                if(def>maxdef){
                    posdef=i;
                    maxdef=def;
                }
            }
            if(a[i].type=="res"){
                int res=a[i].res;
                up(j,1,m)if(p[j].home==a[i].name&&p[j].type=="res")res+=p[j].bonus;
                if(res>maxres){
                    posres=i;
                    maxres=res;
                }
            }
        }
        int numatk=0,numres=0,numdef=0;
        up(j,1,m)if(p[j].home==a[posatk].name)numatk++;
        cout<<a[posatk].name<<" "<<numatk<<" ";
        up(j,1,m)if(p[j].home==a[posatk].name)cout<<p[j].name<<" ";cout<<endl;
        up(j,1,m)if(p[j].home==a[posdef].name)numdef++;
        cout<<a[posdef].name<<" "<<numdef<<" ";
        up(j,1,m)if(p[j].home==a[posdef].name)cout<<p[j].name<<" ";cout<<endl;
        up(j,1,m)if(p[j].home==a[posres].name)numres++;
        cout<<a[posres].name<<" "<<numres<<" ";
        up(j,1,m)if(p[j].home==a[posres].name)cout<<p[j].name<<" ";cout<<endl;
        return 0;
    } 
    vector<pii>atk,def,res;
    up(i,1,m){
        if(p[i].type=="atk")atk.push_back({p[i].bonus,i});
        if(p[i].type=="def")def.push_back({p[i].bonus,i});
        if(p[i].type=="res")res.push_back({p[i].bonus,i});
    }
    sort(atk.rbegin(),atk.rend());
    sort(def.rbegin(),def.rend());
    sort(res.rbegin(),res.rend());
    int posatk=0,posdef=0,posres=0,maxatk=-inf,maxdef=-inf,maxres=-inf;
    up(i,1,n){
        if(a[i].type=="atk"){
            int atkw=a[i].atk;
            up(j,0,min(a[i].siz,(int)atk.size())-1)atkw+=atk[j].first;
            if(atkw>maxatk){
                posatk=i;
                maxatk=atkw;
            }
        }
        if(a[i].type=="def"){
            int defw=a[i].def;
            up(j,0,min(a[i].siz,(int)def.size())-1)defw+=def[j].first;     
            if(defw>maxdef){
                posdef=i;
                maxdef=defw;
            }
        }
        if(a[i].type=="res"){
            int resw=a[i].res;
            up(j,0,min(a[i].siz,(int)res.size())-1)resw+=res[j].first;
            if(resw>maxres){
                posres=i;
                maxres=resw;
            }
        }
    }
    vector<int>atkpos,defpos,respos;
    up(i,0,min(a[posatk].siz,(int)atk.size())-1)atkpos.push_back(atk[i].second),vis[atk[i].second]=1;
    up(i,0,min(a[posdef].siz,(int)def.size())-1)defpos.push_back(def[i].second),vis[def[i].second]=1;
    up(i,0,min(a[posres].siz,(int)res.size())-1)respos.push_back(res[i].second),vis[res[i].second]=1;
    up(i,1,m){
        if(vis[i])continue;
        if(atkpos.size()<a[posatk].siz)atkpos.push_back(i),vis[i]=1;;
    }
    cout<<a[posatk].name<<" "<<atkpos.size()<<" ";
    for(auto v:atkpos)cout<<p[v].name<<" ";cout<<endl;
    up(i,1,m){
        if(vis[i])continue;
        if(defpos.size()<a[posdef].siz)defpos.push_back(i),vis[i]=1;;
    }
    cout<<a[posdef].name<<" "<<defpos.size()<<" ";
    for(auto v:defpos)cout<<p[v].name<<" ";cout<<endl;
    up(i,1,m){
        if(vis[i])continue;
        if(respos.size()<a[posres].siz)respos.push_back(i),vis[i]=1;;
    }
    cout<<a[posres].name<<" "<<respos.size()<<" ";
    for(auto v:respos)cout<<p[v].name<<" ";cout<<endl;
    return 0;
}
```


