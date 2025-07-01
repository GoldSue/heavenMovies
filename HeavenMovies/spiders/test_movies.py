import unittest
from unittest.mock import MagicMock, patch
from scrapy.http import HtmlResponse
from HeavenMovies.spiders.movies import MoviesSpider
from HeavenMovies.items import HeavenmoviesItem


class TestMoviesSpider(unittest.TestCase):
    def setUp(self):
        self.spider = MoviesSpider()

    def test_parse_with_valid_data(self):
        """测试正常情况下的数据提取"""
        # 模拟 HTML 响应
        html = """
        <div class="co_content2">
            <ul>
                <a href=\"detail/1.html\">《电影标题1》</a>
                <a href=\"detail/2.html\">电影标题2</a>
            </ul>
        </div>
        """
        response = HtmlResponse(url='http://example.com', body=html.encode('utf-8'))

        # 调用 parse 方法
        results = list(self.spider.parse(response))

        # 验证结果
        self.assertEqual(len(results), 2)
        
        # 验证第一个结果
        request1 = results[0]
        self.assertEqual(request1.url, 'http://example.com/detail/1.html')
        self.assertEqual(request1.cb_kwargs['item']['title'], '电影标题1')
        
        # 验证第二个结果
        request2 = results[1]
        self.assertEqual(request2.url, 'http://example.com/detail/2.html')
        self.assertEqual(request2.cb_kwargs['item']['title'], '电影标题2')

    def test_parse_with_invalid_data(self):
        """测试缺少标题或URL的情况"""
        # 模拟 HTML 响应 (一个缺少标题，一个缺少URL)
        html = """
        <div class="co_content2">
            <ul>
                <a href=\"detail/1.html\"></a>
                <a>电影标题2</a>
            </ul>
        </div>
        """
        response = HtmlResponse(url='http://example.com', body=html.encode('utf-8'))

        # 调用 parse 方法
        results = list(self.spider.parse(response))

        # 验证结果 (应该过滤掉无效数据)
        self.assertEqual(len(results), 0)


if __name__ == '__main__':
    unittest.main()