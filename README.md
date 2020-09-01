# hydracodegenerator
### Generate Hydra code randomly.

![HCG Image](https://github.com/alecominotti/hydracodegenerator/blob/master/resources/image.png?raw=true, "Pimba")  

### Usage
	
```./hcg.py [options]```

	Options:
	[-f | --function] = Amount of functions to generate after the source.
	[--min] = Minimum amount of functions to generate (Default: 0).
	[--max] = Maximum amount of functions to generate (Default: 5).
	[--web] = Opens Hydra in the web browser with the generated code after generating it.
	[-i | --info] = Shows this information.
	
	HGC sometimes fails to correctly generate the encoded version of the code (Used to create the URL). If this happens, you can still copy the code and paste it in Hydra Manually.
	
#### Usage examples:
	./hcg.py
	./hcg.py -f 7
	./hcg.py --min 5 --max 12
	./hcg.py -f 5 --web
	./hcg.py --info

</br>

#### Links:
	
- Hydra, by Olivia Jack:
	  [https://github.com/ojack/hydra](https://github.com/ojack/hydra, "Hydra, By Olivia Jack")
  
</br>
  
##### Ale Cominotti - 2020
