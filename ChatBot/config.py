# ChatBot config file

# OpenAI API key is now loaded from 'openai_key.txt' (excluded from version control).
# Place your OpenAI API key in a file named 'openai_key.txt' in this directory.
import os
OPENAI_KEY_PATH = os.path.join(os.path.dirname(__file__), 'openai_key.txt')
try:
	with open(OPENAI_KEY_PATH, 'r') as f:
		OPENAI_API_KEY = f.read().strip()
except Exception:
	OPENAI_API_KEY = ""

# System prompt for the LLM (strict RAG)
SYSTEM_PROMPT = (
	"You are a helpful assistant for questions about the World Falls Prevention Guidelines. First, try to answer using only the provided context below. "
	"If the answer is not in the context, you may use your own knowledge, but you must clearly state: "
	"'This answer is not present in the information I have, so I am providing an answer based on my training.' "
	"Even when using your own knowledge, only answer if it is directly related to the World Falls Prevention Guidelines. Do not provide general information unrelated to this topic.\n\n"
	"Context:\n{context}"
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
	},
	{"question": "Who developed the World Falls Guidelines?", "answer": "The guidelines were developed by the World Falls Task Force, which included 96 multidisciplinary experts from 39 countries and 36 scientific and academic societies."},
	{"question": "What is the main goal of the World Falls Guidelines?", "answer": "The main goal is to provide evidence- and consensus-based recommendations for the prevention and management of falls in older adults globally."},
	{"question": "What is the P4 approach in falls prevention?", "answer": "The P4 approach stands for Personalisation, Prediction, Prevention, and Participation, focusing on individualized care and shared decision-making for fall risk management."},
	{"question": "What is the prevalence of falls in people over 80?", "answer": "People aged over 80 have a 50% chance of falling at least once a year."},
	{"question": "What are the psychological impacts of falls in older adults?", "answer": "Falls can result in loss of confidence, depression, and fear of falling, which may further reduce independence and quality of life."},
	{"question": "What is the global burden of falls?", "answer": "The Global Burden of Disease study reported nearly 17 million years of life lost from falls in 2017."},
	{"question": "Why is a multidisciplinary approach important in falls prevention?", "answer": "A multidisciplinary approach brings together expertise from various fields, ensuring comprehensive assessment and management of fall risks for older adults."},
	{"question": "What role do caregivers play in falls prevention?", "answer": "Caregivers are important in supporting older adults, especially those with cognitive impairment, in implementing falls prevention strategies and maintaining safety."},
	{"question": "How can technology support falls prevention?", "answer": "Digital technology, such as e-health tools and wearables, can assist in fall risk screening, assessment, and management, supporting a person-centred approach."},
	{"question": "What is the significance of medication review in falls prevention?", "answer": "Medication reviews and deprescribing of fall-risk-increasing drugs are recommended interventions to reduce fall risk in older adults."},
	{"question": "What is a multifactorial falls prevention intervention?", "answer": "A multifactorial intervention addresses multiple risk factors for falls, such as balance, medication, environment, and vision, tailored to the individual's needs."},
	{"question": "What are common risk factors for falls in older adults?", "answer": "Common risk factors include age, previous falls, gait and balance problems, medication use, vision impairment, and environmental hazards."},
	{"question": "How often should older adults be assessed for fall risk?", "answer": "Older adults should be regularly assessed for fall risk, especially after a fall or change in health status."},
	{"question": "What is the role of exercise in falls prevention?", "answer": "Exercise, particularly balance and strength training, is a key intervention to reduce fall risk and improve mobility in older adults."},
	{"question": "How do the guidelines address falls in people with Parkinson's disease?", "answer": "The guidelines recommend tailored interventions for people with Parkinson's disease, considering their specific risk factors and needs."},
	{"question": "What is the importance of person-centred care in falls prevention?", "answer": "Person-centred care ensures that interventions are tailored to the individual's preferences, needs, and values, improving adherence and outcomes."},
	{"question": "What is the impact of polypharmacy on falls risk?", "answer": "Polypharmacy, or the use of multiple medications, increases the risk of falls, making medication review and deprescribing important strategies."},
	{"question": "How can environmental modifications help prevent falls?", "answer": "Modifying the home environment to remove hazards, improve lighting, and add supports can significantly reduce fall risk."},
	{"question": "What is the role of vision assessment in falls prevention?", "answer": "Regular vision assessment and correction of visual impairment are recommended to reduce fall risk in older adults."},
	{"question": "How do the guidelines address falls in community-dwelling older persons?", "answer": "The guidelines recommend multifactorial interventions and community-based strategies to prevent falls among older adults living at home."},
	{"question": "What is the significance of fear of falling?", "answer": "Fear of falling can lead to reduced activity, social isolation, and increased risk of future falls, so it should be addressed in prevention plans."},
	{"question": "What is the evidence for deprescribing in falls prevention?", "answer": "Systematic reviews show that deprescribing certain medications can reduce fall risk in older adults."},
	{"question": "How are informal caregivers involved in falls prevention?", "answer": "Informal caregivers play a key role in supporting older adults with cognitive impairment in implementing falls prevention strategies."},
	{"question": "What is the importance of global representation in the guidelines?", "answer": "Global representation ensures that the guidelines are applicable and relevant across diverse healthcare systems and populations."},
	{"question": "What are the main components of a falls prevention plan?", "answer": "A falls prevention plan may include exercise, medication review, vision correction, environmental modifications, and education."},
	{"question": "How do the guidelines address implementation challenges?", "answer": "The guidelines discuss strategies for implementing multifactorial falls prevention interventions in community and healthcare settings."},
	{"question": "What is the role of shared decision-making in falls prevention?", "answer": "Shared decision-making involves the older person in treatment choices, improving adherence and outcomes."},
	{"question": "How do the guidelines address falls in older adults with cognitive impairment?", "answer": "The guidelines recommend involving caregivers and tailoring interventions to the needs of those with cognitive impairment."},
	{"question": "What is the impact of frailty on falls risk?", "answer": "Frailty increases the risk of falls and related injuries, so it should be considered in assessment and prevention strategies."},
	{"question": "How do the guidelines support healthcare professionals?", "answer": "The guidelines provide evidence-based recommendations and practical tools for healthcare professionals to assess and manage fall risk in older adults."},
	{"question": "Where can I find the full World Falls Guidelines?", "answer": "The full guidelines are published in Age and Ageing and are available online at https://academic.oup.com/ageing/article-lookup/doi/10.1093/ageing/afac205."}
]

# Path to the RAG vector DB directory (relative to this file)
RAG_VECTORDB_DIR = "../RAG/data/vectordb"
# ChromaDB collection name
RAG_VECTORDB_COLLECTION = "worldfalls"

# Max number of previous Q&A pairs to use as conversational context
MAX_HISTORY = 5
