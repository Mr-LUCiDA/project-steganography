from flask import Flask, render_template, request
from bio_logic import ProteinWatermarker

app = Flask(__name__)
tool = ProteinWatermarker()

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    host_seq = ""
    signature_text = ""
    status_msg = ""
    header_val = "DISTRIBUTED_SEQ"
    
    if request.method == 'POST':
        host_seq = request.form.get('host_input', '')
        signature_text = request.form.get('signature_input', '')
        header_val = request.form.get('header_input', 'DISTRIBUTED_SEQ')
        
        final_dna, status_msg = tool.inject_scattered(host_seq, signature_text)
        
        if final_dna:
            output = tool.format_fasta(header_val, final_dna)

    return render_template('index.html', output=output, 
                           host_seq=host_seq, signature_text=signature_text, 
                           header_val=header_val, status_msg=status_msg)

if __name__ == '__main__':
    app.run(debug=True)