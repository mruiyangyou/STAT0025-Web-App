from crypt import methods
import json
from flask import Flask,render_template,request, jsonify
import numpy as np
from scipy.optimize import linprog
import os
import time
from app.GraphivSol_utils import GraphicSol_Input, SolveGraphicSolution
from app.utils import input_preprocess                                                      

import numpy as np
import pandas as pd
from scipy.optimize import linprog
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from app.StoCal_utils import MarkovDp
from app.Simplex_utils import Simplex, Simplex_loop, SimplexInput, Construct_initial_df
from app.BigM_utils import BigM_loop, Big_M

app = Flask(__name__)

app.config['photo_folder'] = os.path.join('static', 'imgs')
app.config['markov_folder'] = os.path.join('static', 'markovfiles')
app.config['simplex_folder'] = os.path.join('static', 'simplexExcel')
app.config['bigm_folder'] = os.path.join('static', 'bigMfiles')

# Link betwenen each pages
@app.route('/')
def toIndexPage():
    return render_template('home.html')

@app.route('/GraphicSolution')
def toGraphicPage():
    return render_template('GraphicSolution.html')

@app.route('/SimplexSolution')
def toSimplexPage():
    return render_template('SimplexSolution.html')

@app.route('/MarkovDynamicSolution')
def toStochasticPage():
    return render_template('MarkovDynamicSolution.html')

@app.route('/BigMSolution')
def toBigMPage():
    return render_template('BigMSolution.html')

# Calculation
@app.route('/GraphicSolution/gracal', methods = ['POST'])

def graphCalIndex():
    data = request.get_json()
    input = GraphicSol_Input(
        num_of_products = input_preprocess(data[0]['input1']),
        cost_coef = input_preprocess(data[1]['input2']),
        resources_coef = input_preprocess(data[2]['input3']),
        resources = input_preprocess(data[3]['input4']),
        product_name = input_preprocess(data[4]['input5']),
        resource_name = input_preprocess(data[5]['input6'])
    )
    solve = SolveGraphicSolution()
    
    # Solve the problem
    x, value = solve.solve_lp(input)
    x_max, y_max, res, doc = solve.get_minmax(input)
    fig_name = solve.plot(
        input,x_max, y_max, res, doc, x, value
    )
    
    file_name = os.path.join(app.config['photo_folder'], fig_name)
    data = {'No1': x[0], 'No2': x[1], 'value': value, 'img': file_name}
    return jsonify(data)

@app.route('/MarkovDynamicSolution/stocal', methods = ['POST'])
def StoCalIndex():
    data = request.get_json()
    markov = MarkovDp(
        reward_matrix = input_preprocess(data[0]['input1']),
        terminal_reward= input_preprocess(data[1]['input2']),
        action_tm = input_preprocess(data[2]['input3'])
    )
    df = markov.get_reward_df(int(data[3]['input4']), float(data[4]['input5']))
    file_name = time.strftime('rewardDf_' + '%m%d_%H:%M:%S.xlsx')
    df.to_excel(os.path.join('app/static/markovfiles', file_name), 
                    index = None)
    data = {'file': os.path.join(app.config['markov_folder'], file_name)}
    # return send_file('reward_df.xlsx', as_attachment=True)
    return jsonify(data)
  
@app.route('/SimplexSolution/simcal', methods = ['POST'])
def SimCalIndex():
    data = request.get_json()
    input = SimplexInput(
        objective = data[0]['input1'],
        num_of_products = int(data[1]['input2']),
        cost_coef = input_preprocess(data[2]['input3']),
        resources_coef = input_preprocess(data[3]['input4']),
        resources= input_preprocess(data[4]['input5'])
    )

    output, file_name = Simplex_loop(input,'app/static/simplexExcel')
    data = {'output': output, 'path': os.path.join(app.config['simplex_folder'], file_name)}
    return jsonify(data)

@app.route('/BigMSolution/bigMcal', methods = ['POST'])
def BigMCalIndex():
    data = request.get_json()
    input = Big_M(
        objective = data[0]['input1'],
        num_of_products = int(data[1]['input2']),
        cost_coef = input_preprocess(data[2]['input3']),
        resources_coef = input_preprocess(data[3]['input4']),
        resources= input_preprocess(data[4]['input5']),
        constraint_char = input_preprocess(data[5]['input6'])
    )
    output, file_name = BigM_loop(input, 'app/static/bigMfiles')
    data = {'output': output, 'path': os.path.join(app.config['bigm_folder'], file_name)}
    return jsonify(data)

# if __name__ == '__main__':
#     app.run()