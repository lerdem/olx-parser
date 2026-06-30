from flask import Flask, Response, request, render_template

from ad.implementations import (
    get_detail_ads,
    get_full_ads_debug,
    get_dashboard_detail_ads
)

app = Flask(__name__)


@app.route('/detail-rss')
def detail_rss():
    data = get_detail_ads(
        tag=request.args.get('tag'), stop_words=request.args.getlist('sw')
    )
    return Response(data, headers={'Content-Type': 'application/rss+xml'})


@app.route('/debug-template')
def debug_template():
    data = get_full_ads_debug(
        tag=request.args.get('tag'), stop_words=request.args.getlist('sw')
    )
    return Response(data, headers={'Content-Type': 'application/rss+xml'})


@app.route('/debug-html')
def debug_html():
    from ad.adapters.presenter import _get_detail
    from ad.adapters.repository import GetDebugRepo

    data = _get_detail(GetDebugRepo().get_all()[0])
    return Response(data, headers={'Content-Type': 'text/html; charset=UTF-8'})


@app.route('/debug-table')
def debug_table():
    from ad.adapters.presenter import _get_table
    from ad.adapters.repository import GetTableDebugRepo

    data = _get_table(GetTableDebugRepo().get_all_detail())
    return Response(data, headers={'Content-Type': 'text/html; charset=UTF-8'})

# [Template 1: Read-Only]  --(On Click)-->   [Template 2: Input Field]
# [Template 1: Read-Only]  <--(On Blur/Submit)---   [Template 2: Input Field]

@app.route('/ads/<item_id>/edit-title', methods=['GET'])
def get_edit_title_form(item_id):
    from ad.adapters.repository import GetTableDebugRepo
    ads = GetTableDebugRepo().get_all_detail()
    ad = next((ad for ad in ads if ad.id == item_id), None)
    # None -> 404
    return render_template('partials/edit_title_cell_form.html', ad=ad)


@app.route('/ads/<item_id>/update-title', methods=['POST'])
def update_ad_title(item_id):
    from ad.adapters.repository import GetTableDebugRepo
    ads = GetTableDebugRepo().get_all_detail()
    ad = next((ad for ad in ads if ad.id == item_id), None)
    # Get the new name from the form data
    new_name = request.form.get('title', '').strip()

    if len(new_name) < 10:
        return render_template(
            'partials/edit_title_cell_form_error.html',
            ad=ad,
            wrong_input=new_name,
            error="Слишком короткий текст"
        )

    if new_name:
        ad.title = new_name
        # db.session.commit() # Save to your DB
    # Crucial: Return just the raw table cell layout so it swaps back cleanly
    return render_template('partials/title_cell.html', ad=ad)


@app.route('/dashboard_table_0f89d995ae58466cb8fc5fb042bb8263')
def table_dashboard():
    data = get_dashboard_detail_ads(
        tag=request.args.get('tag'), stop_words=request.args.getlist('sw')
    )
    return Response(data, headers={'Content-Type': 'text/html; charset=UTF-8'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8000)
