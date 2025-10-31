# 🧬 NuGene Advisor  
A Multi-Agent AI System built using the *Google Agent Development Kit (ADK)* with a *Flask backend* and a clean *HTML/CSS/JavaScript frontend*.

This project was created for the *ADK Agent Development Challenge*, demonstrating multi-agent routing, tool integration, and web-based interaction.

---

## ✅ 🔍 Project Overview

NuGene Advisor is a two-agent system that provides:

### *1. NuGenomics Customer Support Agent*
- Answers questions *strictly from the NuGenomics FAQ page*  
- Uses a *constrained FAQ browsing tool*  
- Provides *follow-up suggestions*  
- Includes *strict guardrails* to avoid going off-topic  

### *2. Genetic Wellness Information Agent*
- Handles general questions on *fitness, genetics, nutrition, and wellness*
- Uses *three custom tools*:
  - ✅ BMI Calculator  
  - ✅ Current Day & Time Context Tool  
  - ✅ Google Search Tool (required custom external tool)
- Maintains *light memory* (e.g., remembers calculated BMI)
- Responds using clean *Markdown formatting*

### *Router Agent*
- Acts as the *root agent*
- Routes every message to the correct specialist agent  
- Gives a greeting message when the user greets  
- The final output includes the *name of the agent* that processed the query  

---

## ✅ ✨ Key Features Added

### ✅ 1. *Follow-up Suggestions*  
Customer Support Agent adds relevant follow-up questions after every factual answer.

### ✅ 2. *BMI Memory*
Wellness Agent remembers BMI calculated earlier and uses it in later queries.

### ✅ 3. *Strict Guardrails*
Agents politely decline queries outside their domain.

### ✅ 4. *Router Greeting Feature*
The router greets back and explains its routing capability when the user says "Hi".

### ✅ 5. *Agent Identification*
Every final response mentions *which agent handled the query*.

---

## ✅ 🤖 AI Assistance Tools Used

During development of this project, I used the following AI tools for help, code suggestions, debugging, and explanation:

- *Google Gemini*  
- *GitHub Copilot*  
- *ChatGPT*

These tools supported brainstorming, code refinement, documentation, and resolving errors throughout the project.

---
 


---

## ✅ 🧰 Tool Integrations

### *1. BMI Calculator Tool*
For weight, diet, and fitness-related queries.

### *2. Time Context Tool*
Used for motivating or schedule-based advice.

### *3. Google Search Tool*
Required for ADK challenge — used for trends and latest research.

### *4. FAQ Browser Tool*
Used only by the Customer Support Agent.

---

## ✅ 💻 Tech Stack

- Google ADK (Agent Development Kit)  
- Gemini 2.0 Flash  
- Python Flask  
- HTML, CSS, JavaScript  
- BeautifulSoup + Requests  
- ADK InMemorySessionService  

---

## ✅ 🚀 How to Run the Project

### *1️⃣ Install dependencies*

pip install -r requirements.txt


### *2️⃣ Add environment variable*
Create a .env file:


GOOGLE_API_KEY=your_api_key_here


### *3️⃣ Start the Flask server*

python app.py


### *4️⃣ Visit the app*
Open:


http://localhost:5000


---

## ✅ 🧪 Tool Integration Tests

Use these test inputs to demonstrate functionality:

### ✅ Customer Support (FAQ tool)

What does the NuGenomics test include?


### ✅ Guardrail Test

Tell me about DNA diet plans.


### ✅ BMI Calculation (BMI tool)

Calculate my BMI. Weight 70 kg, height 1.7 m.


### ✅ BMI Memory

Is my BMI healthy?


### ✅ Time Context Tool

What is the best time today for a workout?


### ✅ Google Search Tool

What are the latest trends in genetic wellness?


### ✅ Router Greeting

Hi!


---

 

---

 


*R. Akash*  
NuGene Advisor – ADK Agent Development Challenge Submission
