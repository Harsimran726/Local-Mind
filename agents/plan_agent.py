# Plan Agent - This agent is designed to create a plan for the tasks, devide the problem into small tasks with proper plan 
# The all agents have peer to peer communication and they can ask for help from each other agents.  


from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel 
from langgraph.graph import Graph 
from langgraph.checkpoint.memory import InMemorySaver
from src.main import load_model
from src.main import llm_gemma4e2b_it
import json
from tools import docs_tool, vision_tool, retrieval_tool

# create a safe parser for json response  
def safe_json_parser(json_string):
    """Parse JSON string safely, handling various edge cases."""
    if not json_string:
        return None
    
    if not isinstance(json_string, str):
        try:
            return json_string if isinstance(json_string, dict) else None
        except Exception:
            return None
    
    json_string = json_string.strip()
    
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        # Try to extract JSON from markdown code blocks
        if "```json" in json_string:
            try:
                start = json_string.find("```json") + 7
                end = json_string.find("```", start)
                if end > start:
                    return json.loads(json_string[start:end].strip())
            except json.JSONDecodeError:
                pass
        
        # Try to extract JSON object/array enclosed in braces/brackets
        try:
            for i, char in enumerate(json_string):
                if char in "{[":
                    for j in range(len(json_string), i, -1):
                        if json_string[j-1] in "}]":
                            return json.loads(json_string[i:j])
        except json.JSONDecodeError:
            pass
        
        return None
    except Exception:
        return None

class PlanAgent:
    graph: Graph = Graph(saver=InMemorySaver())
    vectorstore: FAISS = None
    embedding_model: HuggingFaceEmbeddings = None
    
    def __init__(self, ):
        super().__init__()
        self.model= load_model()
        self.processor = self.model["processor"]
        self.model = self.model["model"] 

    def create_plan(self,query):
        print(f"QUERY RECEIVED IN THE PLAN AGENT : {query}")
        system_prompt = """ You are a helpful assistant that can understand user query and generate a plan to solve to query or if users want to build something than make a plan for it then you act like a senior AI product manager. """
        chat_messages = [
            {"role": "system", "content": "You are a helpful assistant that can understand user query and provide accurate information."},
            {"role": "user", "content": f"Create a plan to solve the following problem: {query}"}
        ]
        user_query = f"Create a plan to solve the following problem: {query}"
        gemma4 = llm_gemma4e2b_it(self.model, self.processor,system_prompt)
        response = gemma4.invoke(user_query)
        print(f"RESPONSE FROM THE  PLAN AGENT : {response}")
        # call the tool then return the llm with tool response   

        # response of gemma models 
        # tools = {message_to_user: "PUt here message for user", tool_name: "tool name like vision_tool, docs_tool, retrieval_tool",tool_message: "Put here message for tool like retrival"}
        
        response_dict = safe_json_parser(response)

        if response_dict and "tools" in response_dict:
            tools = response_dict["tool_name"]
            tool_message = response_dict["tool_message"]
            
            
            # return message_to_user 
        


planeagent = PlanAgent()
plan_maker = planeagent.create_plan("I want to build a 3d Premium Website for the busienses who is in real estate industry, build it now for me")