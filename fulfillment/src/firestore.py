from google.cloud import firestore
import os

db = firestore.Client()

#adding collections and documents
doc_ref = db.collection(u'users').document(u'alovelace')
doc_ref.set({
    u'first': u'Ada',
    u'last': u'Lovelace',
    u'born': 1814
})
doc_ref = db.collection(u'users').document(u'aturing')
doc_ref.set({
    u'first': u'Alan',
    u'middle': u'Mathison',
    u'last': u'Turing',
    u'born': 1912
})
#retrieving documents matching user query
docs = db.collection(u'users')
query_ref=docs.where(u'first', u'==', u'Ada').stream()
for post in query_ref:
    print(u'{} => {}'.format(post.id, post.to_dict()))