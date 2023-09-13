from goods.models import Goods
from haystack import indexes

class GoodsIndex(indexes.SearchIndex, indexes.Indexable):
    """商品的索引"""
    # document=True 搜索引擎使用该字段内容作为索引来检索,只能有一个字段具有该属性True
    # use_template=True 使用模板建立索引
    #指定搜索的字段
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        #指定搜索的模型类为Goods
        return Goods

    def index_queryset(self, using=None):
        """创建索引的字段"""
        return self.get_model().objects.all()