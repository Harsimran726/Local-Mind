from langgraph import graph 
from langgraph.graph import StateGraph, MessagesState, START, END
from pydantic import BaseModel
from typing import Optional 




# define the state graph 

class agentstates(BaseModel):
    project_name : Optional[str] = None 
    project_description : Optional[str] =None 
    last_update: Optional[str] 
    new_update: Optional[str] = None 
    tool_response: Optional[str] = None 
    agent_response: Optional[str] = None
    image_input: Optional[str] = None
    user_message: Optional[str] = None 
    image_response: Optional[str] = None
    file : Optional[list[str]]
    

class agent_status(BaseModel):
    current_state:  str # where is the agent in graph stage 
    state_history: list[str] # where has the agent been in graph stage 



def stategrahp():
    graph = StateGraph(state_schema=agentstates)
    return graph
