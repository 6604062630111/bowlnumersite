from flask import Flask, request, render_template_string
from sympy import sympify, Symbol
from math import inf

app = Flask(__name__)

def bisection(fx, xl, xr, epsilon):
    x = Symbol("x")
    xm = (xl + xr) / 2
    fxm = fx.subs(x, xm)
    fxr = fx.subs(x, xr)
    if fxm * fxr < 0:
        xl = xm
    else:
        xr = xm

    iterations = []
    i = 0
    criterion = inf

    while criterion > epsilon:
        xmnew = (xl + xr) / 2
        fxm = fx.subs(x, xmnew)
        fxr = fx.subs(x, xr)

        if fxm * fxr < 0:
            xl = xmnew
        else:
            xr = xmnew

        criterion = abs((xmnew - xm) / xmnew)
        iterations.append(f"Iteration {i+1}: xm = {xmnew}, criterion = {criterion}")

        xm = xmnew
        i += 1

    # return all iterations + summary
    summary = {
        "iterations": i,
        "result": xm,
        "log": iterations
    }
    return summary

# 🔹 HTML Page
HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Bisection Method</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
    }
    h2, h3 {
      margin-bottom: 10px;
    }
    form {
      margin-bottom: 20px;
    }
    label {
      display: block;
      margin-top: 8px;
    }
    input[type=text] {
      padding: 5px;
      width: 200px;
      margin-top: 4px;
    }
    input[type=submit] {
      margin-top: 10px;
      padding: 5px 15px;
    }
    pre {
      background: #f2f2f2;
      padding: 10px;
    }
    .summary {
      margin-top: 15px;
      padding: 10px;
      border: 1px solid #ccc;
    }
  </style>
</head>
<body>
  <h2>Bisection Calculator</h2>
  <form method="post">
    <label>function f(x):</label>
    <input type="text" name="fx" placeholder="example: x**4 - 13" required>
    
    <label>xl:</label>
    <input type="text" name="xl" required>
    
    <label>xr:</label>
    <input type="text" name="xr" required>
    
    <label>epsilon:</label>
    <input type="text" name="epsilon" required>
    
    <br>
    <input type="submit" value="Enter">
  </form>

  {% if summary %}
    <h3>Iterations</h3>
    <pre>
{% for line in summary.log %}
{{ line }}
{% endfor %}
    </pre>

    <div class="summary">
      <h3>Answer is</h3>
      Total iteration: {{ summary.iterations }}<br>
      x = {{ summary.result }}
    </div>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    if request.method == "POST":
        fx_input = request.form["fx"]
        xl = float(request.form["xl"])
        xr = float(request.form["xr"])
        epsilon = float(request.form["epsilon"])

        fx = sympify(fx_input)
        summary = bisection(fx, xl, xr, epsilon)

    return render_template_string(HTML, summary=summary)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

