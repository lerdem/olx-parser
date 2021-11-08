from flask import Flask, Response

from ad.adapters.presenter import (
    FeedPresenter,
    FeedDetailedPresenter,
    FeedDebugPresenter,
)
from ad.adapters.repository import GetRepoCsv, GetDetailedRepoCsv, GetDebugRepo
from ad.core.usecases.get_ads import get

app = Flask(__name__)


@app.route('/rss')
def hello_world():
    data = get(GetRepoCsv(), FeedPresenter())
    return Response(data, headers={'Content-Type': 'application/rss+xml'})


@app.route('/detail-rss')
def detail_rss():
    data = get(GetDetailedRepoCsv(), FeedDetailedPresenter())
    return Response(data, headers={'Content-Type': 'application/rss+xml'})


@app.route('/debug-template')
def debug_template():
    data = get(GetDebugRepo(), FeedDebugPresenter())
    return Response(data, headers={'Content-Type': 'application/rss+xml'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=12345)
