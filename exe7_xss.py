from flask import Flask, render_template_string

from db import mongo_db

P1 = "<script>alert('xss1')</script>"
P2 = 'x" onerror="alert(\'xss2\')'
NOTA = ("Um |safe mal colocado declara o valor como HTML confiável, o Jinja2 pula o escape "
        "e o payload volta a ser interpretado pelo navegador.")

PAGINA = """<!doctype html><meta charset="utf-8"><title>Dashboard</title>
<h2>Incidentes</h2>
<table border="1" cellpadding="6">
<tr><th>Título</th><th>Ativo</th></tr>
{% for i in incidentes %}
<tr><td>{{ i.titulo }}</td><td><img src="/icone.png" alt="{{ i.ativo }}"> {{ i.ativo }}</td></tr>
{% endfor %}
</table>"""

app = Flask(__name__)
incidentes = mongo_db().incidentes


def semear():
    incidentes.delete_many({})
    incidentes.insert_many([{"titulo": P1, "ativo": P1}, {"titulo": P2, "ativo": P2}])


@app.after_request
def cabecalhos(resposta):
    resposta.headers["Content-Security-Policy"] = "default-src 'self'"
    return resposta


@app.get("/dashboard")
def dashboard():
    return render_template_string(PAGINA, incidentes=list(incidentes.find()))


@app.get("/dashboard-inseguro")
def dashboard_inseguro():
    linhas = "".join(
        f'<tr><td>{i["titulo"]}</td><td><img src="/icone.png" alt="{i["ativo"]}"> {i["ativo"]}</td></tr>'
        for i in incidentes.find())
    return f"<h2>INSEGURO: apenas para comparação</h2><table border='1'>{linhas}</table>"


if __name__ == "__main__":
    semear()
    print(NOTA)
    app.run()