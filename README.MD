
### Project Directory

``` 
+-- PromptLearning
|   +-- src
|   ...
|
+-- prompt-learning-env
```

### Create a Virtual Environment
`virtualenv -p python3.11 ..\prompt-learning-env`

### Activate the Virtual Environment
`..\prompt-learning-env\Scripts\activate`

### OpenAI API key setting
- Open lib/util_gpt_4.py.
- Change open-api-key on `API_KEY = "sk-...."`.

### Execute the code
- Run `s2_experiments/experiment.py`.

### Check the results
- `data/prompt-history`
