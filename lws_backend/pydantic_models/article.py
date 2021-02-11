from lws_backend.pydantic_models.material import Material
from lws_backend.pydantic_models.icon import Icon


class ArticlePreview(Material):
    icon: Icon


class Article(ArticlePreview):
    metaDescription: str
    articleText: str
