# ��Ӱ�Ƽ���������վ�ĵ�Ӱ�Ƽ���ҳ��

GitHub Pages ��ڣ�<https://liqxing.github.io/movie-recommender/>��

�����ӵ��ƶ�Ӧ�ã�<https://liqxingappio-ijwrtfv4rdappamp4ns8pe.streamlit.app/>��

ҳ��ͨ�� iframe Ƕ�빫���� Streamlit Ӧ�á�GitHub Pages �ṩ��̬��ҳ�棬Python �Ƽ����������� Streamlit Community Cloud��������Ҫ�ֱ𷢲��������Ͳֿⲻ�ᴴ���ƶ� Python Ӧ�á�

## ��һ�β���

1. ��¼ <https://share.streamlit.io/>�������Լ��� GitHub �˺ţ���� **Create app**��ѡ������Ӧ�á�
2. ��д�ֿ� `LiQXing/liqxing.github.io`����֧ `main`������ļ� `movie-recommender/streamlit_app.py`��
3. �� Advanced settings ѡ�� **Python 3.13**��Ӧ������ secrets��Spark �� Java��
4. ��� Deploy���ȴ���װ�������״�����׼������Ӧ����Ϊ **����**������Ӧ�ã�ȷ�����Ƽ���Ӱ��
5. �����ɵ���ʵ `https://xxx.streamlit.app/` ��ַ����ͬĿ¼ `app-config.json` �� `appUrl`������ `{"appUrl":"https://���ʵ��������.streamlit.app/"}`���ύ�� main��
6. �� GitHub Pages ��ڣ����潫�Զ�Ƕ�롣��Ƕ��������������������ƣ�������������ڴ򿪡���

`appUrl` ������Ϊ�Ϸ����ƶ�Ӧ�õ�ַ���Ժ����Ӧ�õ�ַʱ���޸ĸ��ֶμ��ɣ���Ϊ null ʱҳ�����ʾ���ƶ�Ӧ�ô����𡱡�

## ����

- ���������û� ID������ Spark ALS ѵ���õ����û������͵�Ӱ�����������û�ȫ�������ֵ�Ӱ������ Top 10��δ֪�û�ʹ�����ŵ�Ӱ���ס�
- ѡ��ϲ���ĵ�Ӱ����ѡ����Ϊ 4.5 �֣��̶���Ӱ������ͨ��������С��������ʱƫ���������Ƽ���һ������֧�֡���һ����������ɸѡ��
- ����������ԭ���˶ԡ�CSV ���������ַ�����ģ�����������������������˹������ĳ�����Ӱ�����ౣ��ԭ����

## ���ݡ�ģ������Դ

�������� [GroupLens MovieLens 25M](https://grouplens.org/datasets/movielens/25m/)��ԭʼ����ʹ��������[�ٷ� README](https://files.grouplens.org/datasets/movielens/ml-25m-README.html)�����ֿ��ṩѵ���õ� ALS ����������Ӱ�ۺϵ�ͳ�ƺ�������������ϴ�ԭʼ���֡�������ӰĿ¼�����û���ʷ��

�״������� GroupLens �ٷ�����Լ 262 MB ZIP��У�� SHA256 `8b21cfb7eb1706b4ec0aac894368d90acf26ebdfb6aced3ebd4ad5bd1eb9c6aa`���ù̶��汾ԭʼ MD5 Ϊ `6b51fb2759a8657d3bfcbfc42b592ada`��������ʹ�� HTTPS ������֤����֤����Թٷ�����Դ�� InCommon/emSign ֤��������� [֤����Դ˵��](certificates/README.md)�������������������Ρ������ʽ����ȫ�� 25,000,095 �����ֵĽ�����ʷ�������Լ���ӰĿ¼�������������ʱĿ¼��CSV ��ÿ�� 250,000 �д����������������ֱ������ڴ棻��ɺ�ɾ������ ZIP������Լ 220 MB �������ݡ��������ƶ���ʱĿ¼���ú������Ҫ�������ء����������ƶ��ܹ����� GroupLens��

ԭʼѵ��ʵ��ʹ�� Windows��Spark 4.0.1��rank=16���ƶ�ֻ���� NumPy ��������ԭʼѵ��ʵ�黷����������Դ��չʾѵ��ʱ�����ã��������йܷ�����Ӳ����

��Ӧ�����ڿγ�ѧϰ���о���ʾ����������ҵ���ѹ��ܡ��������ݼ���ע����F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. ACM Transactions on Interactive Intelligent Systems 5, 4, Article 19. https://doi.org/10.1145/2827872��

## �������д˷�����

```powershell
python -m pip install -r movie-recommender/requirements.txt
python -m streamlit run movie-recommender/streamlit_app.py
```

�����״�����ͬ�������عٷ����ݡ�����ԭ��Ŀ�Կ�ʹ��ԭ�� `app.py`������Ķ���

�ο���[����Ӧ��](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)��[Ƕ�빫��Ӧ��](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app/embed-your-app)��
