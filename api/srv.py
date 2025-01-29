import numpy as np
import os
from flask import Flask, request, render_template, redirect, url_for, flash
import joblib  # Importação correta do joblib

# Inicialização do Flask
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'supersecretkey'  # Chave secreta para usar o sistema de flash messages

# Tenta carregar o modelo
try:
    model = joblib.load('model/model.pkl')  # Carregamento do modelo
    print("Modelo carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    model = None  # Define o modelo como None se não for possível carregá-lo

# Rota principal
@app.route('/')
def display_gui():
    return render_template('template.html')

# Rota para processar o formulário
@app.route('/verificar', methods=['POST'])
def verificar():
    # Verifica se o modelo foi carregado corretamente
    if model is None:
        flash("Erro: Modelo não carregado. Contate o administrador.")
        return redirect(url_for('display_gui'))

    try:
        # Captura os dados do formulário
        sexo = request.form['gridRadiosSexo']
        casado = request.form['gridRadiosCasado']
        educacao = request.form['educacao']
        dependentes = int(request.form['dependentes'])
        trabalho = request.form['gridRadiosTrabalhoProprio']
        rendimento = float(request.form['rendimento'])
        valoremprestimo = float(request.form['valoremprestimo'])

        # Cria um array numpy com os dados do formulário
        teste = np.array([[sexo, casado, educacao, dependentes, trabalho, rendimento, valoremprestimo]])

        # Exibe os dados no console para depuração
        print(":::::: Dados de Teste ::::::")
        print(f"Sexo: {sexo}")
        print(f"Número de Dependentes: {dependentes}")
        print(f"Casado: {casado}")
        print(f"Educação: {educacao}")
        print(f"Trabalha por conta própria: {trabalho}")
        print(f"Rendimento: {rendimento}")
        print(f"Valor do empréstimo: {valoremprestimo}")
        print("\n")

        # Faz a predição usando o modelo
        classe = model.predict(teste)[0]
        print(f"Classe Predita: {classe}")

        # Retorna o resultado para o template
        return render_template('template.html', classe=str(classe))

    except KeyError as e:
        flash(f"Erro: Campo do formulário faltando - {e}")
        return redirect(url_for('display_gui'))
    except ValueError as e:
        flash(f"Erro: Dados inválidos no formulário - {e}")
        return redirect(url_for('display_gui'))
    except Exception as e:
        flash(f"Erro inesperado ao processar os dados: {e}")
        return redirect(url_for('display_gui'))

# Inicialização do servidor Flask
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5500))  # Porta padrão 5500
    app.run(host='0.0.0.0', port=port)