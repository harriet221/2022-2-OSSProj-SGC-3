import firebase_admin 
from firebase_admin import credentials, firestore
import pyautogui as pg

from register import db
from Defs import *

def item_buy(user,item):
  
  if coin_buy(user,item)!=0: 
    db.collection("User").document(user).update({"item":firestore.ArrayUnion([item])})
    print(pg.alert(text=Content.buy_msg.value, title=Content.buy_msgtitle.value))
  else:
    print(pg.alert(text=Content.cannotBuy_msg.value, title=Content.cannotBuy_msgtitle.value))

def item_buyList_get(user):
  itemList=db.collection("User").document(user).get().to_dict()
  return itemList["item"]

def item_apply(user,item):
  db.collection("User").document(user).update({"item_apply":item})


def item_apply_get(user):
  field=db.collection("User").document(user).get().to_dict()
  return field["item_apply"]

def coin_set(user,new_coin):
  db.collection("User").document(user).update({"coin":firestore.Increment(new_coin)})

def coin_get(user):
  field=db.collection("User").document(user).get().to_dict()
  return field["coin"]

def coin_buy(user,item):
  if coin_get(user)>=Item.coin_10k.value and item=="bullets":
    db.collection("User").document(user).update({"coin":firestore.Increment(-Item.coin_10k.value)})
  elif coin_get(user)>=Item.coin_50k.value and item=="missile":
    db.collection("User").document(user).update({"coin":firestore.Increment(-Item.coin_50k.value)})
  elif coin_get(user)>=Item.coin_100k.value and item=="missile2":
    db.collection("User").document(user).update({"coin":firestore.Increment(-Item.coin_100k.value)})
  elif coin_get(user)>=Item.coin_1000k.value and item=="dagger":
    db.collection("User").document(user).update({"coin":firestore.Increment(-Item.coin_1000k.value)})
  else:
    return 0

def coin_give(user,friend,coin):
  coin=int(coin)
  db.collection("User").document(friend).update({"coin":firestore.Increment(coin)})
  coin_set(user,-coin)

def rank_set(user,new_coin): #랭킹 DB 저장
  field=db.collection("User").document(user).get().to_dict()
  current_rank=field["rank"]
  if new_coin>current_rank:
    db.collection("User").document(user).update({"rank":new_coin})

def rank_get(user):
  field=db.collection("User").document(user).get().to_dict()
  return field["rank"]

def rank(user,score): # 높은 점수를 랭킹에 저장
    current_rank = rank_get(user)
    if current_rank < score:
        rank_set(user,score)

def rankList_get():
  users_ref = db.collection('User')
  docs = users_ref.stream()
  rank_list=[]
  for doc in docs:
    doc=doc.to_dict()
    rank_list.append([doc["email"],doc["rank"]])
  rank_list.sort(key=lambda x:-x[1])
  for i , rank in enumerate(rank_list):
    rank_list[i]=[i+1,rank[0],rank[1]]
  return rank_list

def set_special(user):
  db.collection("User").document(user).update({"nomal_ending":"True"})

def get_special(user):
  return
  return 

#for doc in docs:
#    print(u'{} => {}'.format(doc.id, doc.to_dict()))

