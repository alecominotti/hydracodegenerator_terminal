# hydracodegenerator [terminal]

</br>

## For a newer, better and updated version of HCG please visit [this repo](https://github.com/alecominotti/hydracodegenerator).

</br>

### Generate Hydra code randomly.

![HCG Image](https://github.com/alecominotti/hydracodegenerator_terminal/blob/master/resources/image.png?raw=true "Pimba")  

</br>

###### English
- HCG is a script that randomly generates code in Hydra sintax. The sources, functions, the amount of them and the values of their arguments are all generated randomly (within customizable lower and upper bounds).
- From the script arguments you can specify a wide variety of parameters to customize the code, such as the lower and upper bounds for random number generation, probabilities of generating some kind of arguments and more.
- In <b>Live Session Mode</b> you can automatically run and visualize the generated code in Hydra, since it opens Hydra in a web browser and executes the generated code in real time, everytime you press Enter.
- HCG aims to allow you to explore the infinite creation posibilities that Hydra provides, combining them with the art of randomness and the user customization, allowing you to find inspiration, new ideas or just pass the time.

###### Español
- HCG es un script que genera codigo en sintaxis de Hydra de manera aleatoria. Las sources, functions, la cantidad de ellas y los valores de sus argumentos son todos generados aleatoriamente (dentro de un rango personalizable).
- Desde los argumentos del script podés especificar una gran variedad de parámetros para personalizar el código, como los límites inferiores y superiores para la generación aleatoria de números, la probabilidad de generar algunos tipos de funciones y más.
- En el modo <b>Live Session Mode</b> podés ejecutar y visualizar el código en Hydra de manera automática, ya que abre Hydra en el navegador web y ejecuta el nuevo código generado en tiempo real, cada vez que apretás Enter.
- HCG tiene como objetivo permitirte explorar las infinitas posibilidades de creación que provee Hydra, combinándolas con el arte de lo aleatorio y la personalización del usuario, permitiéndote encontrar inspiración, nuevas ideas o simplemente pasar el rato.


</br>

### Usage
	
- Windows: ```py hcg.py [options]```
- Linux and Mac: ```python3 hcg.py [options]```

	<pre>Options:
	[-f | --function] &lt;Integer&gt; = Constant amount of functions.
	[-fmin] &lt;Integer&gt; = Minimum amount of functions to generate (Default: 0).
	[-fmax] &lt;Integer&gt; = Maximum amount of functions to generate (Default: 5).
	[-amin] &lt;Float&gt; = Minimum value for function arguments (Default: 0).
	[-amax] &lt;Float&gt; = Maximum value for function arguments (Default: 5).
	[-ap | --arrow-prob] &lt;Integer&gt; = Probability of generating an arrow function as an argument (0 to 100). (Default: 10) | ex.: "() => Math.sin(time)" 
	[-mp | --mouse-prob] &lt;Integer&gt; = Probability of generating a mouse arrow function as an argument (0 to 100). (Default: 20) | ex.: "() => mouse.x" 
	[-mip | --modulate-itself-prob] &lt;Integer&gt; = Probability of setting "o0" as an argument for the modulate functions (0 to 100). (Default: 20) | ex.: "modulate(o0, 1)"
	[-xs] &lt;String&gt; = Exclusive sources to use, separated by commas (ex.: osc,voronoi).
	[-xf] &lt;String&gt; = Exclusive functions to use, separated by commas (ex.: colorama,modulate).
	[-i | --ignore] &lt;String&gt; = Sources or functions to ignore, separated by commas (ex.: osc,brightness).
	[--use-all] = Doesn't ignore any source or function.
	[-web] = Opens Hydra in the web browser with the generated code after generating it. (Google Chrome only).
	[-live] = Starts <b>Live Session Mode</b>, where HCG opens up the web browser, writes the generated code and run it automatically in Hydra, everytime you press Enter. (Google Chrome only).
	[-hc | --hide-code] = Hides code in Hydra when running in Live Session Mode.
	[-l | --localhost] &lt;IP:PORT|PORT&gt; = Allows you to use Live Session Mode in your locally running Hydra, specifying the IP:PORT or just PORT if it's running on the same computer.
	[-i | --info] = Shows this information.
	Experimental:
	[-um | --use-media] = Allows camera and microphone in Live Session Mode (Blocked by default to avoid window prompts).
	[-cb | --close-browser] = In Live Session Mode, closes browser window when the script is stopped. WINDOWS 10 ALWAYS CLOSES THE BROWSER WHEN THE SCRIPT IS STOPPED.
	
	Remember you can combine almost all options.</pre>
	
</br>

### How to install and run the script:

You must have Python 3 installed. You can download it here: [https://www.python.org/downloads/](https://www.python.org/downloads/, "Python 3 Download")\
(or `sudo apt-get install python3` on terminal)

#### Windows:

- Open up a terminal (program called "cmd") and clone the directory, typing:
	<pre>git clone https://github.com/alecominotti/hydracodegenerator.git</pre>
- Enter the directory:	
	<pre>cd hydracodegenerator</pre>
- Run the script:	
	<pre>py hcg.py</pre>


#### Linux and Mac:

- Open up a terminal and clone the directory, typing:
	<pre>git clone https://github.com/alecominotti/hydracodegenerator.git</pre>
- Enter the directory:	
	<pre>cd hydracodegenerator</pre>
- Run the script:	
	<pre>python3 hcg.py</pre>
	
</br>

#### Usage examples (on Windows replace "python3" with "py"):
	python3 hcg.py
	python3 hcg.py -f 7
	python3 hcg.py --fmin 5 --fmax 10 --amin 0.5 --amax 15
	python3 hcg.py -xs osc,voronoi
	python3 hcg.py -xf colorama,modulateScale,kaleid
	python3 hcg.py --ignore noise,brightness,luma,gradient
	python3 hcg.py -ap 45 -mp 5 -mip 70
	python3 hcg.py --use-all	
	python3 hcg.py -f 8 --web
	python3 hcg.py -f 7 --live
	python3 hcg.py -f 10 --live -hc
	python3 hcg.py --live -hc -l 8000
	python3 hcg.py --live -hc -l 192.168.0.69:8000
	python3 hcg.py --live --hide-code --use-media --close-browser
	python3 hcg.py --info

</br>

#### Links:
	
- Hydra, by Olivia Jack:
	  [https://github.com/ojack/hydra](https://github.com/ojack/hydra "Hydra, By Olivia Jack")
  
</br>

----------------------------------------------------------------------------------------------------------------
  
##### Ale Cominotti - 2020
