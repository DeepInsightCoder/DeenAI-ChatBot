document.getElementById('send-btn').addEventListener('click', sendMessage);
   document.getElementById('clear-btn').addEventListener('click', clearChat);

   function sendMessage() {
       const userInput = document.getElementById('user-input').value;
       if (userInput.trim() === "") return;

       // Display user's message
       const chatHistory = document.getElementById('chat-history');
       chatHistory.innerHTML += <div class="user-message">You: ${userInput}</div>;

       // Clear input field
       document.getElementById('user-input').value = "";

       // Send request to Flask backend
       fetch('/chat', {
           method: 'POST',
           headers: {
               'Content-Type': 'application/x-www-form-urlencoded',
           },
           body: user_input=${encodeURIComponent(userInput)},
       })
       .then(response => response.text())
       .then(response => {
           // Display chatbot's response
           chatHistory.innerHTML += <div class="bot-message">Bot: ${response}</div>;
           chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll to bottom
       })
       .catch(error => {
           console.error('Error:', error);
       });
   }

   function clearChat() {
       document.getElementById('chat-history').innerHTML = "";
   }