from flask import Flask, request, render_template

   app = Flask(_name_)

   @app.route('/')
   def home():
       return render_template('index.html')

   @app.route('/chat', methods=['POST'])
   def chat():
       user_input = request.form['user_input']
       # Add your chatbot logic here
       response = f"You said: {user_input}"  # Replace with actual chatbot response
       return response

   if _name_ == '_main_':
       app.run(host='0.0.0.0', port=8080)