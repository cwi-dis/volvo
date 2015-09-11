## Sensor Relay

Publish-Subscribe architecture on top of WebSockets for relaying sensor data
from sensors to browser clients. Frontend files can be found in the folder
public/.

### Installation

In order to run the server, first make sure you have `node.js` and `npm`
installed. You should be able to get both by installing Node from your
operating system's package manager.

Once you have Node and NPM installed change into the project's root directory
and run the following command:

    $ npm install

This will install all the project's dependencies into the project's root
folder. The server is now ready to run.

### Running the application

To start the application run the following command:

    $ npm start

This will set up a WebSocket server on port 23148 and a HTTP server on
port 8080. Opening `http://localhost:8080` in a web browser will display
the visualisations and any data sent to port 23148.
