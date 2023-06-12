// Get the UI elements
let userinput = document.getElementById("userinput");
let sendbutton = document.getElementById("sendbutton");
let chatbody = document.getElementById("chatbody");

// Add event listener for the send button
sendbutton.addEventListener("click", function() {
   // Get the user input value
   let input = userinput.value;

   // Check if the input is not empty
   if (input) {
      // Create a new div element for the user message
      let usermessage = document.createElement("div");
      usermessage.className = "message usermessage";
      let usertext = document.createElement("div");
      usertext.className = "text";
      let userp = document.createElement("p");
      userp.textContent = input;
      usertext.appendChild(userp);
      usermessage.appendChild(usertext);

      // Append the user message to the chat body
      chatbody.appendChild(usermessage);

      // Scroll to the bottom of the chat body
      chatbody.scrollTop = chatbody.scrollHeight;

      // Clear the user input field
      userinput.value = "";

      // Send the user input to the server using fetch API
      fetch("/getresponse", {
         method: "POST",
         headers: {
            "Content-Type": "application/json"
         },
         body: JSON.stringify({input: input})
      })
      .then(response => response.json())
      .then(data => {
         // Get the bot response from the data
         let output = data.output;

         // Create a new div element for the bot message
         let botmessage = document.createElement("div");
         botmessage.className = "message botmessage";
         let bottext = document.createElement("div");
         bottext.className = "text";
         let botp = document.createElement("p");
         botp.textContent = output;
         bottext.appendChild(botp);
         botmessage.appendChild(bottext);

         // Append the bot message to the chat body
         chatbody.appendChild(botmessage);

         // Scroll to the bottom of the chat body
         chatbody.scrollTop = chatbody.scrollHeight;
      })
      .catch(error => console.error(error));
   }
});