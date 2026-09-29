from html.parser import HTMLParser

from data_master_app.products_ui import render_home


class Controls(HTMLParser):
    def __init__(self):
        super().__init__()
        self.by_id = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.by_id[attrs['id']] = attrs


def test_legacy_global_source_controls_are_not_visible():
    page = render_home()
    controls = Controls()
    controls.feed(page)
    assert 'hidden' in controls.by_id['productsFile']
    assert 'hidden' in controls.by_id['analyzeProductsBtn']
    assert 'hidden' not in controls.by_id['generateProductsBtn']
    assert '"products.title": "Source data"' not in page
    assert 'data-general-upload' in page
    assert 'data-nested-upload' in page
