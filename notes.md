# Notes for Project 2

## Prompts
Promp has to include all the info that the LLM wil lneed to solve the problem. The prompt has to include **both the info in the Bayesian network and the evidence**.  
Search the internet for *probabilistic reasoning* in LLMs to see some ways on how to **represent a Bayesian network in a prompt**.  

## Structured Output:  
The diagnose method should only return two values (a specific string, and a probability). You will have to get this from LLM response. Three ways:  
1. Parse the text output of the LLM with your own code to extract the name of the disease and probility (This is cumbersome!)  
2. Include in the prompt instructions to generate only the required info and not to produce any other text.
3. Specify an output template of [structured output](https://ai.google.dev/gemini-api/docs/structured-output?example=recipe). This is the most reliable way. See slides on prompting on Canvas for examples.
