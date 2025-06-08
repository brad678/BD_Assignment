generate_answer_prompt = """You are a software best-practices assistant. 
User Question: {user_question}
Retrieved Snippets:
{context}
Task:
Based on these snippets, write a concise answer to the user’s question. 
Cite each snippet you use by its doc_id in square brackets (e.g., [KB004]).
Return only the answer text."""

critique_answer_prompt = """You are a critical QA assistant. The user asked: {user_question}
Initial Answer:
{initial_answer}
KB Snippets:
{context}
Task:
Determine if the initial answer fully addresses the question using only these snippets.
- If it does, respond exactly: COMPLETE
- If it misses any point or cites missing info, respond: REFINE: <short list of missing topic keywords>
Return exactly one line."""

refine_answer_prompt = """You are a software best-practices assistant refining your answer. 
User Question: {user_question}
Initial Answer:
{initial_answer}
Critique:
{critique_result}
Additional Snippet:
[{doc_id}] {extra_snippet}
Task:
Incorporate this snippet into the answer, covering the missing points.
Cite any snippet you use by doc_id in square brackets.
Return only the final refined answer."""

