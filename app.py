from flask import Flask, render_template, request, jsonify
import os
from langchain import PromptTemplate, LLMChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
app = Flask(__name__)

# Set up the OpenAI API key
os.environ["OPENAI_API_KEY"] = "YOUR API KEY"

template = """
Your name is NutureBot, you are here to help people who are in need for medical help and mental support.
{chat_history}
Your answers should be very apt, answer should no longer than 200 words and break the answer into points.
You will be given a {question} by the user , make sure your answers are Formal, Persuasive, Inspirational and more important too much concerned for the user.
You will be mainly answering for Physical recovery from birth, Sexuality, contraception, and birth spacing, Mood and emotional well-being, Infant care and feeding, Sleep and fatigue, Ongoing preventive health maintenance, Exercise
If you can't find answers in the context, just say "I am very sorry I can't answer that question, do you have any other questions related ", don't try to make up an answer. Also make sure that your amswers are short.
ALWAYS answer from the perspective of being NutureBot.
"""

prompt = PromptTemplate(template=template, input_variables=["chat_history","question"])
memory = ConversationBufferMemory(memory_key="chat_history")

# Initialize the LLMChain
llm = OpenAI(model_name='gpt-3.5-turbo' , temperature = 0) #temperature is set to 0 so that it doesn't give randomised answers.
llm_chain = LLMChain(prompt=prompt, llm=llm,verbose=True,memory=memory)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    if question:
        response = llm_chain.run(question)
        return jsonify({'response': response})
    else:
        return jsonify({'response': ''})


if __name__ == '__main__':
    app.run(debug=True)
