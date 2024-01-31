from flask import Flask, Response, request

from ad.implementations import get_detail_ads, get_full_ads_debug

app = Flask(__name__)


@app.route('/detail-rss')
def detail_rss():
    data = get_detail_ads(
        tag=request.args.get('tag'), sw=request.args.get('stop_words')
    )
    return Response(data, headers={'Content-Type': 'application/rss+xml'})


@app.route('/debug-template')
def debug_template():
    data = get_full_ads_debug(
        tag=request.args.get('tag'), sw=request.args.get('stop_words')
    )
    return Response(data, headers={'Content-Type': 'application/rss+xml'})


@app.route('/debug-html')
def debug_html():
    from ad.adapters.presenter import _get_detail
    from ad.adapters.repository import GetDebugRepo

    data = _get_detail(GetDebugRepo().get_all()[0])
    return Response(data, headers={'Content-Type': 'text/html; charset=UTF-8'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8000)
