# ChatBot config file

# OpenAI API key (set here for convenience, or leave blank to require user input)
OPENAI_API_KEY = "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"

# System prompt for the LLM (strict RAG)
SYSTEM_PROMPT = (
	"You are a helpful assistant. Only answer using the provided context below. "
	"If the answer is not in the context, say 'I don't know based on the provided information.' "
	"Do not use any outside knowledge.\n\nContext:\n{context}"
)

# Messages template for OpenAI chat
def get_messages(context, user_input):
	return [
		{"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
		{"role": "user", "content": f"Question: {user_input}\nAnswer:"}
	]

# Sample Q&A pairs for UI/demo
SAMPLE_QA = [
	{
		"question": "What are the World Guidelines for Falls Prevention?",
		"answer": "The World Guidelines for Falls Prevention and Management for Older Adults provide a global framework and expert recommendations for healthcare professionals to identify, assess, and reduce the risk of falls in older adults."
	},
	{
		"question": "Why is falls prevention important for older adults?",
		"answer": "Falls are common in people aged 65 and over, with a 30% chance of falling each year. Falls can lead to injury, loss of independence, and even death, making prevention critical for quality of life."
	},
	{
		"question": "How should healthcare professionals assess the risk of falls?",
		"answer": "Healthcare professionals should use validated tools to assess gait, balance, and functional mobility, and consider risk factors such as age, multimorbidity, and medication use."
	},
	{
		"question": "What interventions are recommended to prevent falls?",
		"answer": "A person-centred approach is recommended, including exercise, medication review, and addressing environmental hazards, often in combination."
	}
]

# Path to the RAG vector DB directory (relative to this file)
RAG_VECTORDB_DIR = "../RAG/data/vectordb"
# ChromaDB collection name
RAG_VECTORDB_COLLECTION = "worldfalls"
