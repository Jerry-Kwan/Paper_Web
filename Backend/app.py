import os
import shutil
from flask import Flask, request, jsonify

import paper_processor as pp

TMP_SAVE = 'tmp_save/'
FILE_FOLDERS = [TMP_SAVE]
app = Flask(__name__)
save_dict = {}


# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


# receive pdf and analyze it, exception catching is to be done
@app.route('/upload', methods=['GET', 'POST'])
def upload_and_analyze():
    paper_pdf = request.files['file']
    uniqueId = request.form.get('uniqueId')
    f_path = TMP_SAVE + uniqueId + paper_pdf.filename

    paper_pdf.save(f_path)
    ppe = pp.PaperPdfExtract(f_path)
    save_dict[uniqueId] = ppe

    return jsonify({'ref_list': ppe.display_ref})


# return bib
@app.route('/bib', methods=['GET', 'POST'])
def get_bib():
    uniqueId = request.form.get('uniqueId')
    no = int(request.form.get('no'))
    ppe = save_dict[uniqueId]
    rpc = pp.RefPaperCrawler(ppe.partial_ref_author, ppe.clean_split_ref_text)
    ret = rpc.get_bib(no)
    if ret is None:
        return jsonify({'text': 'Not found'})
    else:
        return jsonify({'text': ret})


if __name__ == "__main__":
    for ff in FILE_FOLDERS:
        if not os.path.exists(ff):
            os.makedirs(ff)
        else:
            shutil.rmtree(ff)
            os.makedirs(ff)

    app.run(host='127.0.0.1', port=5003, debug=True)
