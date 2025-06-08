# user_q = "What are best practices for caching?"
from flask import Flask, request, jsonify
from .agentic_rag_simplified import graph, RAGState

# Compile the LangGraph graph
compiled_app = graph.compile()

app = Flask(__name__)

@app.route("/rag", methods=["POST"])
def rag_endpoint():
    try:
        data = request.get_json()
        user_question = data.get("question", "").strip()
        
        if not user_question:
            return jsonify({"error": "Missing 'question' in payload"}), 400

        initial_state = RAGState(
            user_question=user_question,
            kb_hits=[],
            initial_answer="",
            critique_result="",
            final_answer=""
        )

        result = compiled_app.invoke(initial_state)
        return jsonify({"answer": result["final_answer"]})


    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
