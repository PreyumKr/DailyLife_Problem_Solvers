const fs = require('fs');
const WebSocket = require('ws');

// Create a WebSocket server on port 8080
const wss = new WebSocket.Server({ port: 8080 });

// Helper function to read the last N lines from a file
function readLastNLines(filename, numLines, callback) {
    const stream = fs.createReadStream(filename, { encoding: 'utf8' });
    let data = '';
    let lines = [];

    stream.on('data', chunk => {
        data = chunk + data; // Prepend new data since we're reading backwards

        lines = data.split('\n');
        if (lines.length > numLines) {
            stream.destroy(); // Stop reading when we have enough lines
        }
    });

    stream.on('close', () => {
        // Return the last N lines
        const lastLines = lines.slice(-numLines);
        callback(null, lastLines);
    });

    stream.on('error', (err) => {
        callback(err, null);
    });

    // Start reading from the end of the file by chunking backwards
    const CHUNK_SIZE = 1024;
    const stats = fs.statSync(filename);
    let position = Math.max(0, stats.size - CHUNK_SIZE);

    function readNextChunk() {
        if (position === 0) {
            // If we've reached the start of the file, read the last chunk
            stream.read();
            return;
        }

        stream.read(CHUNK_SIZE);
        position = Math.max(0, position - CHUNK_SIZE);
    }

    stream.on('readable', readNextChunk);
}

// When a client connects
wss.on('connection', (ws) => {
    console.log('Client connected!');

    // Read and send the last 10 lines of the log file to the client
    readLastNLines('log.txt', 10, (err, lastMessages) => {
        if (err) {
            console.error('Error reading log file:', err);
            return;
        }

        lastMessages.forEach((line) => {
            ws.send(`Last message => ${line}`);
        });
    });

    // Track the last known size of the file to detect changes
    let lastKnownSize = fs.statSync('log.txt').size;

    // Watch for changes in the log file
    fs.watch('log.txt', (eventType, filename) => {
        if (eventType === 'change') {
            const stats = fs.statSync('log.txt');
            const newSize = stats.size;

            if (newSize > lastKnownSize) {
                // Read the new content added to the file
                const readStream = fs.createReadStream('log.txt', {
                    start: lastKnownSize,
                    end: newSize
                });

                let newContent = '';
                readStream.on('data', (chunk) => {
                    newContent += chunk;
                });

                readStream.on('end', () => {
                    const newMessages = newContent.split('\n').filter(line => line.trim() !== '');
                    newMessages.forEach((message) => {
                        ws.send(`Updated message => ${message}`);
                    });

                    // Update the last known size to the new size
                    lastKnownSize = newSize;
                });
            }
        }
    });

    // Handle messages from the client (optional)
    ws.on('message', (message) => {
        console.log(`Received message => ${message}`);
    });

    // Handle WebSocket connection closure
    ws.on('close', () => {
        console.log('Client disconnected');
    });
});
