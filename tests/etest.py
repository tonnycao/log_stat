from datetime import datetime
from elasticsearch import Elasticsearch

size = 2147483647
r = round(size/(1024*1024),6)
print(r)
exit(0)

hosts = [{"host": "localhost", "port": 9200}]
es = Elasticsearch(hosts = hosts)
doc = {
    'author': 'tonnycao',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}
# result = es.indices.create(index='news', ignore=[400, 404])
# print(result)

data = {
    'title': '美国留给伊拉克的是个烂摊子吗',
    'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
    'date': '2011-12-16'
}

datas = [
    {
        'title': '美国留给伊拉克的是个烂摊子吗',
        'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
        'date': '2011-12-16'
    },
    {
        'title': '公安部：各地校车将享最高路权',
        'url': 'http://www.chinanews.com/gn/2011/12-16/3536077.shtml',
        'date': '2011-12-16'
    },
    {
        'title': '中韩渔警冲突调查：韩警平均每天扣1艘中国渔船',
        'url': 'https://news.qq.com/a/20111216/001044.htm',
        'date': '2011-12-17'
    },
    {
        'title': '中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首',
        'url': 'http://news.ifeng.com/world/detail_2011_12/16/11372558_0.shtml',
        'date': '2011-12-18'
    }
]
mapping = {
    'properties': {
        'title': {
            'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
        }
    }
}
es.indices.delete(index='news', ignore=[400, 404])
es.indices.create(index='news', ignore=400)
result = es.indices.put_mapping(index='news', body=mapping)
print(result)
for data in datas:
    result = es.index(index='news', doc_type='politics', body=data)
    print(result)

# res = es.index(index="test-index", doc_type='tweet', id=3, body=doc)
# print(res)

# res = es.get(index="test-index", doc_type='tweet', id=3)
# print(res['_source'])


res = es.search(index='news', body={"query": {"match": {"title": "中国"}}})
# print(result)
# res = es.search(index="news", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
        print(hit)