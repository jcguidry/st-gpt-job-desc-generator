import openai
import time

def stream(model, prompt, box):

    stream.s = ''  # Initialize s as an attribute of the function


    response = openai.ChatCompletion.create(
        model=model,
        messages=prompt,
        temperature=0,
        stream=True  
    )
    if response:
        stream.s = ''
        for chunk in response:
            if chunk['choices'][0]['finish_reason'] == "stop":
                break
            for c in chunk['choices'][0]['delta']['content']:
                stream.s += c
                time.sleep(.005)
                box.write(stream.s)