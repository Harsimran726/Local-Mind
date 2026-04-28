from dotenv import load_dotenv 
from PIL import Image # for image
load_dotenv()
import os 
import json
import torch
from transformers import AutoProcessor, AutoModelForCausalLM


def load_model():
    try:
        print(f"INSIDE LOAD MODEL FUNCTION")
        processor = AutoProcessor.from_pretrained("google/gemma-4-E2B-it")
        # print(f"PROECEOR : {processor}")
        model = AutoModelForCausalLM.from_pretrained(
            "google/gemma-4-E2B-it",
            dtype=torch.float16,
            device_map="auto",
        #    offload_folder="offload",     # Creates a folder to store layers that don't fit in RAM
    low_cpu_mem_usage=True,       # Crucial: prevents the initial RAM spike
    offload_state_dict=True       # Forces the 'layer-by-layer' disk mapping
            )
        # print(f"MODEL LOADED SUCCESSFULLY:- {model}")
        return model, processor
    except Exception as e:
        return {"status":300,"message":f"ERROR LOAD MODEL: {e}"}
# print(load_model())
# model, processor = load_model()


class llm_gemma4e2b_it:
    def __init__(self, model, processor,system_prompt):
        self.model = model
        self.processor = processor
        self.system_prompt = system_prompt
    def invoke(self,x):
        # pass
        print(f"INSIDE THE INVOKE FUNCTION OF THE GEMMA MODEL")
        # system_prompt = """ You are a helpful assistant that can understand user query and provide accurate information."""

        messages = [
    {"role": "system", "content": self.system_prompt},
    {"role": "user", "content": {x}},
]

# process the input 
        text = processor.apply_chat_template(
    messages, 
    tokenize=False,
    return_tensors="pt",
    add_generation_prompt=True,
    enable_thinking=False
    )

        inputs = processor(text=text, return_tensors="pt").to(model.device)
        input_len =inputs['input_ids'].shape[1]

# if processor.pad_token is None:
#     processor.pad_token = processor.eos_token
#     model.config.pad_token_id = model.config.eos_token_id

# generate the respones 
        print(f"INPUTS: {inputs}")
        outputs = model.generate(**inputs,max_new_tokens=100)
        response = processor.batch_decode(outputs[0][input_len:], skip_special_tokens=True)

        print(response)
        return response

import gc
del model
torch.cuda.empty_cache()
del processor

gc.collect()
