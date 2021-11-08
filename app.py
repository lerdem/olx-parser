from flask import Flask, Response, request

from ad.adapters.presenter import FeedDebugPresenter
from ad.adapters.repository import GetDebugRepo
from ad.core.usecases.get_ads import get
from ad.implementations import get_base_ads, get_detail_ads

app = Flask(__name__)


@app.route('/rss')
def hello_world():
    data = get_base_ads(tag=request.args.get('tag'))
    return Response(data, headers={'Content-Type': 'application/rss+xml'})


@app.route('/detail-rss')
def detail_rss():
    data = get_detail_ads(tag=request.args.get('tag'))
    return Response(data, headers={'Content-Type': 'application/rss+xml'})


@app.route('/debug-template')
def debug_template():
    data = get(GetDebugRepo(), FeedDebugPresenter())
    return Response(data, headers={'Content-Type': 'application/rss+xml'})


if __name__ == '__main__':
    app.run(debug=False)
