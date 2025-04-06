from flask import Flask, render_template, request
import numpy as np
from methods import *
import os
from random import random
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    error = None
    root = None
    table_html = None
    image_path = None
    image_name = None  # Inicializa la variable image_name

    if request.method == "POST":
        try:
            # Capturar datos del formulario
            func_str = request.form["func"]
            method = request.form["method"]
            tol = float(request.form.get("tol", 1e-6))
            max_iter = int(request.form.get("max_iter", 100))
            
            f = lambda x: eval(func_str, {"x": x, "np": np, "__builtins__": {}})
            df = lambda x: (f(x + 1e-6) - f(x)) / 1e-6

            # Parámetros
            a = float(request.form.get("a") or 0)
            b = float(request.form.get("b") or 0)
            x0 = float(request.form.get("x0") or 0)
            x1 = float(request.form.get("x1") or 0)

            parametros = {"a": a, "b": b, "x0": x0, "x1": x1}

            # Ejecutar método
            if method == "bisection":
                root, iteraciones = bisection(f, a, b, tol, max_iter)
                plot_a, plot_b = a, b
            elif method == "false_position":
                root, iteraciones = false_position(f, a, b, tol, max_iter)
                plot_a, plot_b = a, b
            elif method == "newton":
                root, iteraciones = newton_raphson(f, df, x0, tol, max_iter)
                plot_a, plot_b = x0 - 5, x0 + 5
            elif method == "secant":
                root, iteraciones = secant(f, x0, x1, tol, max_iter)
                plot_a, plot_b = min(x0, x1) - 5, max(x0, x1) + 5
            elif method == "brent":
                root, iteraciones = brent_method(f, a, b, tol)
                plot_a, plot_b = a, b
            else:
                raise ValueError("Método no válido")

            # Generar gráfico único
            image_name = f"graph_{random():.5f}.png"
            image_path = os.path.join("static", image_name)  # Ruta correcta
            plot_function(f, plot_a, plot_b, iteraciones, method)  # Llamada a la función que genera el gráfico

            # Renombrar el archivo generado para que tenga el nombre único
            os.rename("static/graph.png", image_path)

            # Mostrar resultado
            resultado = f"Raíz encontrada: {root:.6f}"

            # Generar tabla HTML
            if iteraciones:
                table_html = "<table><tr><th>Iteración</th><th>x</th><th>f(x)</th></tr>"
                for it in iteraciones:
                    table_html += f"<tr><td>{it[0]}</td><td>{it[1]:.6f}</td><td>{it[2]:.6f}</td></tr>"
                table_html += "</table>"

        except Exception as e:
            error = str(e)

    return render_template("index.html", resultado=resultado, error=error, root=root,
                           table=table_html, image_path=image_name, func_str=func_str)  # Ahora pasa image_name directamente

if __name__ == "__main__":
    app.run(debug=True)
