var commander = require('commander');

commander.option(
    '-p, --proxy [HOST]',
    "Act as proxy for the specified host"
).parse(process.argv);

var WebSocket = require("ws");
var socket = new WebSocket.Server({ port: 23148 });

var util = require('./util');
var tag = "[PUBSUB]".yellow;

if (commander.proxy) {
    util.debug(tag, "Proxy mode activated");

    var proxy = new WebSocket("ws://" + commander.proxy);

    proxy.on('open', function () {
        proxy.send(JSON.stringify({
            type: "proxy"
        }));

        proxy.on('message', function (msg) {
            msg = JSON.parse(msg);

            if (msg.type === 'data') {
                socket.publish(msg.channel, msg.data);
            }
        });
    });
}

socket.subscribers = [];

socket.subscribeClient = function (client, channel) {
    var subscriptions = this.subscribers.filter(function (subscriber) {
        return (subscriber.client == client && subscriber.channel == channel);
    });

    if (subscriptions.length != 0) {
        util.debug(tag, "Client already subscribed to channel '" + channel + "'");

        client.send(JSON.stringify({
            type: "control",
            status: "ERR",
            message: "Client already subscribed to channel '" + channel + "'"
        }));

        return;
    }

    this.subscribers.push({
        channel: channel,
        client: client
    });

    util.debug(tag, "Client subscribed to channel '" + channel + "'");

    client.send(JSON.stringify({
        type: "control",
        status: "OK",
        channel: channel
    }));
};

socket.unsubscribeClient = function (client, channel) {
    var index = this.subscribers.reduce(function (foundIndex, subscriber, i) {
        if (foundIndex >= 0) {
            return foundIndex;
        }

        if (subscriber.client == client && subscriber.channel == channel) {
            return i;
        }

        return foundIndex;
    }, -1);

    if (index >= 0) {
        util.debug(tag, "Unsubscribing client from channel '" + channel + "'");
        this.subscribers.splice(index, 1);

        client.send(JSON.stringify({
            type: "control",
            status: "OK",
            channel: channel
        }));
    } else {
        client.send(JSON.stringify({
            type: "control",
            status: "ERR",
            message: "Unsubscribe failed"
        }));
    }
};

socket.removeClient = function (client) {
    var index = this.subscribers.reduce(function (foundIndex, subscriber, i) {
        if (foundIndex >= 0) {
            return foundIndex;
        }

        if (subscriber.client == client) {
            return i;
        }

        return foundIndex;
    }, -1);

    if (index >= 0) {
        util.debug(tag, "Unsubscribing client from channel '" + this.subscribers[index].channel + "'");
        this.subscribers.splice(index, 1);

        this.removeClient(client);
    }
};

socket.publish = function (channel, data) {
    this.subscribers.forEach(function (subscriber) {
        if (subscriber.channel == channel || subscriber.channel == undefined) {
            try {
                subscriber.client.send(JSON.stringify({
                    type: "data",
                    channel: channel,
                    data: data
                }));
            } catch (err) {
                util.debug(tag, "Removing dead client");
                socket.removeClient(subscriber.client);
            }
        }
    });
};

util.debug(tag, "Listening for websocket connections on port 23148");

socket.on("connection", function (client) {
    util.debug(tag, "Client connected");

    client.on("message", function (msg) {
        try {
          msg = JSON.parse(msg);
        } catch (err) {
          msg = { type: "null" };
        }

        switch (msg.type) {
            case "subscribe":
                socket.subscribeClient(client, msg.channel);
                break;
            case "unsubscribe":
                socket.unsubscribeClient(client, msg.channel);
                break;
            case "echo":
                util.debug(tag, "Received echo message");
                client.send(JSON.stringify(msg));
                break;
            case "data":
                socket.publish(msg.channel, msg.data);
                break;
            case "proxy":
                socket.subscribeClient(client);
                break;
        }
    });
});
