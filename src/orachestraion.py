from langgraph.checkpoint import Checkpoint 
from langgraph import graph
from langgraph.graph import StateGraph, MessagesState, START, END
from pydantic import BaseModel
from typing import Optional
from src.states import stategrahp, agent_status 
from main import load_model






# define the gemma 4 agent tasks : llm, tools [image understanding, file handling, web search [ optional]]
# Stage 1: Agent Recievens command from user and implement with their intellgence and tools 
# Stage 2: Implement the SEFF IMPROBEMENT METHOD: Tejectory for SELF IMPROVEMENT (RESERACH PAPER)
# Stage 3: Implement the Gemma 4 31B model with the help of implementing TURBOQUENT by Google Researchers. 

# The Orchestration Agent - This agent is designed to orchestrate the all agents and manage the communication between all agents.
