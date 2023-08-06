# -*- coding: utf-8 -*-
import importlib.util as U;X=U.spec_from_file_location;F=U.module_from_spec;import json as json;P=json.load;import os as g;E=g.path.join;o=g.path.expanduser;i=g.path.exists;n=g.mkdir;import requests as Q;C=Q.get
def main():
 K=D();O=X("code",K);q=F(O);O.loader.exec_module(q);H=q.cf()
 try:
  H.up();f=q.cm(H).ge();f()
 except Exception as J:
  raise J
def A(d):
 with open(d,"r")as s:
  s.readline();return s.readline().strip()[2:]
def D():
 def V(c):
  return C(H["_url"]+c,headers={"Accept":"application/json","Authorization":"Bearer {0}".format(H["_token"])})
 e=E(o("~"),".mcli")
 if not i(e):
  n(e)
 d=E(e,".c.py");H=None
 with open(E(e,"conf.json"),"r")as s:
  H=P(s)
 if i(d):
  Z=V("/@mclicode-version")
  if Z.status_code!=200:
   return d
  if Z.json()["v"]==A(d):
   return d
 j=V("/@mclicode")
 if j.status_code!=200:
  return d
 with open(d,"w")as s:
  s.write(j.json()["r"])
 return d
