from flask import Flask, request, jsonify, send_from_directory
import openai
from flask_cors import CORS
import os
import dotenv
import re

# Load environment variables from the .env file
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# System content for the chatbot
system_content = """You are a helpful assistant tasked with answering any questions about Alireza's CV and personal website. Give short and conversational answers that try to engage the user to ask more questions. You should provide short, concise, informative answers based on the information below:

Alireza Bavafa is a Master’s student in Business Analytics at the University of Maryland, with an impressive academic background that includes an MBA in Marketing from the University of Tehran and a Bachelor’s degree in Civil Engineering from Iran University of Science and Technology. With 5 years of experience in the industry, Alireza has worked across various fields of business analytics and product management. His career spans roles in companies like Wekala, known as a top service for purchasing products from international stores for Iranians; Golrang Industrial Group, the largest producer of detergent and hygiene products in Iran; and Snapp! Grocery, which dominates the Iranian market for online taxi services, food ordering, and supermarket goods, holding an 80% market share. At Snapp! Grocery, Alireza played a key role in managing dark stores—facilities dedicated to fulfilling online grocery orders.
In addition to his professional roles, Alireza had two notable entrepreneurial experiences. The first was at age 20, where he developed a marketing and customer management system using Telegram. This platform featured a digital menu, check-in, lottery, and a restaurant/cafe recommendation system for both business owners and customers. Although it had potential, the project could not continue due to Telegram being filtered in Iran. His second venture, at age 25, involved an e-commerce business for selling cardboard sheets, cartons, and boxes, offering online price inquiries and purchases. He successfully handed over this business before immigrating to the United States.
Alireza’s achievements include automating a system at PediaMetrix for collecting and analyzing user data through APIs, which reduced manual efforts by 80% and created a robust lead generation database. At Golrang Industrial Group, he designed and implemented procurement enterprise software that scaled data pipelines and automated workflows, resulting in a 30% improvement in efficiency. This initiative involved creating an internal portal to manage the company's international procurement process, replacing the Excel-based system with a streamlined solution that automated over 80 internal steps, facilitated cross-departmental approvals, and integrated with the company’s Qlik-based BI platform. The portal featured a sourcing management module for end-to-end supplier management, including API integration for tracking sample status and generating resource development reports, enhancing product lifecycle management.
Alireza also developed a supplier selection model using optimization algorithms, which incorporated supplier performance scores to optimize for both cost efficiency and quality. By integrating performance data into the optimization model using Excel Solver, the system enabled data-driven decision-making that accounted for reliability and quality in addition to cost. This approach resulted in a 3% cost savings by prioritizing suppliers who consistently delivered higher quality and met performance standards.
Additionally, he launched over five procurement dashboards that integrated inventory management with sales, enhancing supply chain transparency and operational efficiency. These dashboards provided real-time analytics on the procurement of raw materials, supplier profiles, and delivery timelines, enabling predictive analytics for demand forecasting and better risk management. The centralization of procurement data improved decision-making processes, resource allocation, and supplier relationship management, resulting in a more agile and responsive supply chain.
At the University of Maryland, Alireza developed ETL pipelines and over 10 dashboards for major U.S. infrastructure projects, significantly enhancing user experience. He managed end-to-end data processes, using SQL, AWS, and Python to facilitate data integration and automation, ensuring the smooth operation of the Billaunchpad website under the Build America Center. He also conducted comprehensive Benefit-Cost Analyses (BCA) for federal grant applications, evaluating the financial viability and compliance of large-scale projects with USDOT guidelines. Moreover, he collaborated with a technical team to develop a chatbot powered by large language models, improving service efficiency by 30% and streamlining the process for users seeking funding opportunities under the Bipartisan Infrastructure Law.
Known for his hardworking and positive nature, Alireza brings enthusiasm and a results-driven approach to every project. He excels in cross-functional team settings and thrives on solving complex problems. His technical skills encompass Python, R, SQL, and data analytics tools such as Power BI and Tableau, along with a strong foundation in cloud platforms like AWS and Google Cloud. He is further certified in Google Advanced Data Analytics, Agile Project Management, and Product Analytics.
In his personal time, Alireza enjoys listening to podcasts on entrepreneurship, watching sci-fi movies, and playing sports like tennis. With his blend of analytical expertise, leadership qualities, and entrepreneurial spirit, he is eager to contribute to dynamic teams, making him an ideal candidate for roles in analytics, data science, or business strategy.
"""

def sanitize_message(message):
    # Remove any special characters, limit length, etc.
    message = re.sub(r'[^\w\s]', ' ', message)  # Basic sanitization (removes non-word characters)
    return message[-1000:]  # Limit input to 1000 characters for safety

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

# Route to serve the chatbot.html file
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    user_message = sanitize_message(user_message)
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_message}
            ]
        )
        response_message = response.choices[0].message.content.strip()
        return jsonify({"response": response_message})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=10000,debug=True)