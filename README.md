Project proposal  

 

Industry Supervisor:  Elementz 

 

Project Title:  Testing and Governance Framework for AI integrations 
 

Work Mode:  Remote/ Hybrid 

 

Project Goal:  

This project aims to build an AI monitoring/testing and insights dashboard to evaluate the performance and reliability of AI integrations within our product ecosystem.  
 
As our company adopts AI more into our software product offering, it's critical to ensure that these integrations remain accurate, efficient, fair, scalable, and cost-effective in an online (e.g. Azure & Azure Foundry) and offline (e.g. self-hosted Ollama & Langchain ) environment. As our application data and user base grows, we would like to remain confident our AI integrations continually perform as outlined with the above expectations. 
 

The student team will build a modular testing platform and governance dashboard that: 

    Continuously evaluates our AI integrations (e.g., chatbots, recommendation engines, classifiers, semantic search) across key metrics, for example: 

    Accuracy 

    Latency  

    Bias Mitigation 

    Hallucination Rate 

    Scalability 

    Cost 

    Security 

    Environmental impact 

    Other (your suggestions) 

    Supports Governance by: 

    Ensuring appropriate logging and auditing of AI decisions is in place 

    Tracking compliance against configurable internal AI policies we can set 

    Flagging anomalies or breaches within our configured measure limits 

    Providing transparency into model behaviour and updates 

    The tool could educate by offering hits/ tips/ suggestions from resources such as Mitre Atlas & others for example. 
     

Skills Required:  

 

    Backend Development: Python/ Node.js/ .Net (making and integrating REST APIs) 

    Frontend Development: React/ Angular 

    ML/AI Understanding: Evaluation metrics, model behaviour analysis, testing & governance. 

    Data Visualization: Plotly, D3.js, AMCharts or similar 

    Additional: Familiarity with LLMs, prompt evaluation, and integration of observability tools (e.g., LangSmith, AI Foundry, Grafana, Open Telemetry, wandb.ai) 

 
Project Resources:  

    Access to an example chat bot and/ or semantic search 

    Suggestions on tooling and configuration 

    SME support from Full Stack Engineer/ QA Engineer/ AI Engineer 

 

Contact Hours Schedule (minimum 1h per week):  

    Project Kick off 

    Daily Scrum (12-20 mins/pd) 

    Fortnightly Progress Demo 

    Sprint Planning fortnightly (1x hr) 

    Final Demo 

Requirements:
    Pip
    Node.js
    ollama
    python

When initiating the project on new enviromentsyou must change the pathing for the database:
C:/Users/OliJa/Desktop/AI-Dashboard/AI-DashBoard/mydata.db -> Your path

RUN COMMANDS (In a virtual enviroment):
    
    pip install -r requirements.txt

    Terminal 1:
        cd website
        cd my-react-app
        npm run dev

    Terminal 2:
        cd flask-server
        python server.py



 
