# hydracodegenerator
### Generate Hydra code randomly.

![HCG Image](https://github.com/alecominotti/hydracodegenerator/blob/master/resources/image.png?raw=true, "Pimba")  

- HGC is a script that randomly generates code in Hydra syntax. The sources, functions, the amount of them  and the values of their arguments are all generated randomly (within a specified lower and upper bound).
- From the script arguments you can specify a constant amount of functions or a lower and upper bound, to generate a random number of functions between them.
- More advanced variables can be modified from the CodeGenerator class attributes, such as the lower and upper bounds for the source and function arguments, the probabilities of generating a time function like `() => Math.sin(time * 0.3)` as an argument and more.

</br>

### Usage
	
- Windows: ```py hcg.py [options]```
- Linux and Mac: ```python3 hcg.py [options]```

	<pre>Options:
	[-f | --function] = Amount of functions to generate after the source.
	[--min] = Minimum amount of functions to generate (Default: 0).
	[--max] = Maximum amount of functions to generate (Default: 5).
	[--web] = Opens Hydra in the web browser with the generated code after generating it.
	[-i | --info] = Shows this information.</pre>
	
	- You need to have Python 3 installed.
	- HGC sometimes fails to correctly generate the encoded version of the code (Used to create the URL). If this happens, you can still copy the code and paste it in Hydra manually.
</br>

### How to install and run the script:
#### Windows:

- Open up a terminal (program called "cmd") and type:
	<pre>git clone https://github.com/alecominotti/hydracodegenerator.git</pre>
- Enter the directory:	
	<pre>cd hydracodegenerator</pre>
- Run the script:	
	<pre>py hcg.py</pre>


#### Linux and Mac:

- Open up a terminal and type:
	<pre>git clone https://github.com/alecominotti/hydracodegenerator.git</pre>
- Enter the directory:	
	<pre>cd hydracodegenerator</pre>
- Run the script:	
	<pre>python3 hcg.py</pre>
	
</br>

#### Usage examples (on Windows replace "python3" with "py"):
	python3 hcg.py
	python3 hcg.py -f 7
	python3 hcg.py --min 5 --max 12
	python3 hcg.py -f 5 --web
	python3 hcg.py --info

</br>

#### Links:
	
- Hydra, by Olivia Jack:
	  [https://github.com/ojack/hydra](https://github.com/ojack/hydra, "Hydra, By Olivia Jack")
  
</br>
  
##### Ale Cominotti - 2020
