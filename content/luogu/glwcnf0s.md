# 背包

~~~
void zobag(int wi, int pi) {
  for (int i = v; i >= wi; i--) {
    f[i] = max(f[i], f[i - wi] + pi);
  }
  return;
}
void combag(int wi, int pi) {
  for (int i = wi; i <= v; i++) {
    f[i] = max(f[i], f[i - wi] + pi);
  }
  return;
}
void perfectbag(int wi, int pi, int ti) {
  if (ti == 0) return;
  if (ti * wi >= v) {
    combag(wi, pi);
    return;
  }
  for (int i = 1; i <= ti; i <<= 1) {
    zobag(wi * i, pi * i);
    ti -= i;
  }
  if (ti > 0) zobag(wi * ti, pi * ti);
  return;
}




