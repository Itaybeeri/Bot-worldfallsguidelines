# World Falls Guidelines Q&A Project

This project is designed to help people get trustworthy answers about the World Falls Prevention Guidelines.

We built a knowledge base (using a method called Retrieval-Augmented Generation, or RAG) by collecting information from the official World Falls Guidelines website and its PDF publications. This means the chatbot is able to answer questions using real, up-to-date information from these sources.

## What does the chatbot do?

- You can ask any question about the World Falls Guidelines.
- The chatbot will do its best to answer using only the information found in the guidelines and official documents.
- If the answer is not found in the guidelines, the chatbot will let you know and avoid guessing.
- Every answer includes a reference to the source, so you know where the information came from.

## Why did we build this?

Falls are a major health concern for older adults worldwide. The World Falls Guidelines provide expert recommendations to help prevent and manage falls. Our goal is to make this important knowledge easy to access for everyone—clinicians, caregivers, and the public—using a simple question-and-answer chatbot.

## How does it work?

1. We collected and processed all the content from the World Falls Guidelines website and its PDFs.
2. We built a special database that lets the chatbot quickly find the most relevant information for any question.
3. When you ask a question, the chatbot searches this database and shows you the best answer it can find, along with the source.

## Try it out!

To try the chatbot, you first need to build the knowledge base (RAG) and then run the chatbot:

1. **Build the knowledge base:**
   - Go to the `RAG` folder and follow the instructions in `RAG/README.md` to process the website and PDFs. This step collects and organizes all the information the chatbot will use.
2. **Run the chatbot:**
   - Once the knowledge base is ready, you can run the chatbot on your own computer. See the `ChatBot/README.md` for simple instructions on how to get started.

---

_This project is for demonstration and educational purposes only. Always consult a healthcare professional for medical advice._
