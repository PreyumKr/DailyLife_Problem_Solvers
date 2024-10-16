const express = require('express');
const app = express();


// app.use(express.static('webpage'));
// app.set('view engine', 'ejs');

// app.listen(3000, () => {
    //     console.log('Server is running on http://localhost:3000');
    // });
    
const websocket = new WebSocket('ws://localhost:8080');

websocket.onopen = () => {
    console.log('Connected to server');
    // websocket.send('Hello from client');
};

// app.get("/webpage", (req, res) => {
//     res.render("index", { variableName: ${message.data} })
//     websocket.onmessage = (message) => {
//         console.log(`Received message => ${message.data}`);
        
//     };    
// });

websocket.onmessage = (message) => {
    console.log(`Received message => ${message.data}`);
    
};
