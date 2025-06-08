from langgraph.graph import StateGraph, END
from typing import List, Dict
from pydantic import BaseModel
from .index_kb import get_embedding, collection, client
from .prompts import generate_answer_prompt, critique_answer_prompt, refine_answer_prompt

import os
from dotenv import load_dotenv

load_dotenv(override=True)

class RAGState(BaseModel):
    user_question: str
    kb_hits: List[Dict]
    initial_answer: str
    critique_result: str
    final_answer: str


def retrieve_kb_node(state: RAGState) -> RAGState:
    emb = get_embedding(state.user_question)
    results = collection.query(query_embeddings=[emb], n_results=5)
    hits = [
        {
            "doc_id": r_id,
            "answer_snippet": r_doc,
            "source": r_meta["source"],
        }
        for r_id, r_doc, r_meta in zip(results["ids"][0], 
                                       results["documents"][0], 
                                       results["metadatas"][0])
    ]
    return state.copy(update={"kb_hits": hits})



def generate_answer_node(state: RAGState) -> RAGState:
    context = "\n".join([f"[{hit['doc_id']}] {hit['answer_snippet']}" for hit in state.kb_hits])
    prompt = generate_answer_prompt.format(
        user_question=state.user_question, 
        context=context)
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return state.copy(update={"initial_answer": response.choices[0].message.content.strip()})


def critique_answer_node(state: RAGState) -> RAGState:
    context = "\n".join([f"[{hit['doc_id']}] {hit['answer_snippet']}" for hit in state.kb_hits])
    prompt = critique_answer_prompt.format(
        user_question=state.user_question,
        initial_answer=state.initial_answer,
        context=context
    )
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return state.copy(update={"critique_result": response.choices[0].message.content.strip()})


def refine_answer_node(state: RAGState) -> RAGState:
    if state.critique_result.startswith("COMPLETE"):
        return state.copy(update={"final_answer": state.initial_answer})
    
    missing_keywords = state.critique_result.replace("REFINE:", "").strip()
    new_query = f"{state.user_question} and information on {missing_keywords}"
    emb = get_embedding(new_query)
    results = collection.query(query_embeddings=[emb], n_results=1)
    
    extra_snippet = results["documents"][0][0]
    doc_id = results["ids"][0][0]
    
    prompt = refine_answer_prompt.format(
        user_question=state.user_question,
        initial_answer=state.initial_answer,
        critique_result=state.critique_result,
        doc_id=doc_id,
        extra_snippet=extra_snippet
    )
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return state.copy(update={"final_answer": response.choices[0].message.content.strip()})

# Define the state graph for the RAG process
graph = StateGraph(RAGState)
graph.add_node("retrieve_kb", retrieve_kb_node)
graph.add_node("generate_answer", generate_answer_node)
graph.add_node("critique_answer", critique_answer_node)
graph.add_node("refine_answer", refine_answer_node)

graph.set_entry_point("retrieve_kb")
graph.add_edge("retrieve_kb", "generate_answer")
graph.add_edge("generate_answer", "critique_answer")
graph.add_edge('critique_answer', 'refine_answer')
graph.add_edge('refine_answer', END)