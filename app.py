import gradio as gr
from numpy import *

from fractal_generator import FractalGenerator

TITLE = "Fractal Generator"
DESCRIPTION = "<center>Create your own fractal art!</center>"
EXAMPLES = [
    ["Julia", "sin(z**12 + cos(0.7*z**12) + 1.41)"],
    ["Julia", "sin(z**6 + cos(0.7*z**6) + tan(z**3) + 1.41)"],
    ["Julia", "sin(z**7 + cos(z**5) + tanh(z**3) + 0.61)"],
    ["Julia", "sin(arcsin(z**7) + arccos(z**5) + arctan(z**3) + 0.61)"],
    ["Julia", "sin(arccos(z**3 - z**2 + z)+ 0.61)"],
    ["Julia", "log(arccos(z**3 - z**2 + z)+ 0.61)"],
    ["Julia", "sin(z**4 + 3.41)*exp(2.5*1J)"],
    ["Julia", "cos(cosh(z**3) - sinh(z**2) + tanh(z**4))**2"],
    ["Julia", "sin(z**5 + cos(z**5 + sin(z**5 + cos(z**5))) + 1.41)"]
]
ARTICLE = r"""<center>
              This application uses Julia and Mandelbrot fractal algorithms.
              These plots show the convergence plot for infinitely composed complex functions <br>
              These functions are based on artist-defined generating functions $f(z)$ with $z \in \mathbb{C}$ as follows<br>
              $$ F(z) = \prod^{\inf} f(z)  $$<br>
              Done by dr. Gabriel Lopez<br> 
              For more please visit: <a href='https://sites.google.com/view/dr-gabriel-lopez/home'>My Page</a><br>
              </center>"""

# interactive function
def plot_fractal(fractal_type: str, python_function: str):
    frac = FractalGenerator(n=500, max_iter=10)
    if fractal_type == "Julia":
        frac.create_julia(lambda z: eval(python_function))
    elif fractal_type == "Mandelbrot":
        frac.create_mandelbrot()
    else:
        print("Current wrong option: ", fractal_type)
    return frac.plot()


# gradio frontend elements
in_dropdown = gr.Dropdown(
    choices=["Julia", "Mandelbrot"], label="Select a type of fractal:", value="Julia"
)
in_text = gr.Textbox(
    value="sin(z**4 + 1.41)",
    label=f"Enter function using $z$ as complex-variable. You can use all numpy functions. 1J = \sqrt{-1}",
    placeholder="your own z function",
    lines=4,
)
out_plot = gr.Plot(label="Fractal plot")

# gradio interface
gr.Interface(
    inputs=[in_dropdown, in_text],
    outputs=out_plot,
    fn=plot_fractal,
    examples=EXAMPLES,
    title=TITLE,
    description=DESCRIPTION,
    article=ARTICLE,
).launch()
