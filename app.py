from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import qa_chain  
import uvicorn

app = FastAPI()

# Allow frontend HTML access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        query = request.question
        result = qa_chain.invoke({"query": query})
        answer = result["result"]
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}

# Root endpoint
@app.get("/")
def home():
    return {"message": "RAG Chatbot API is running 🚀"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)


