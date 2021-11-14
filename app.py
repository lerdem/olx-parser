from flask import Flask, Response, request
from ad.implementations import get_base, get_detail

app = Flask(__name__)


@app.route('/rss')
def hello_world():
    data = get_base(tag=request.args.get('tag'))
    return Response(data, headers={'Content-Type': 'application/rss+xml'})


@app.route('/detail-rss')
def detail_rss():
    data = get_detail(tag=request.args.get('tag'))
    return Response(data, headers={'Content-Type': 'application/rss+xml'})


if __name__ == '__main__':
    app.run(debug=False)
