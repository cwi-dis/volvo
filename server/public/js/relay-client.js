/*jslint browser: true */
/*global WebSocket, Promise */

var RelayClient = function (url) {
    var thiz = this;

    this.url = url;
    this.socket = new WebSocket(url);

    this.subscriptions = {};
    this.pendingSubscriptions = {};

    this.echocallback = function () {
      return;
    };

    this.socketConnected = new Promise(function (resolve) {
        thiz.socket.onopen = function () {
            resolve();
        };
    });

    this.socketConnected.then(function () {
        thiz.socket.onmessage = function (event) {
            var data = JSON.parse(event.data);

            if (data.type === "control" && data.status === "OK") {
                if (thiz.pendingSubscriptions[data.channel]) {
                    if (thiz.subscriptions[data.channel] === undefined) {
                        thiz.subscriptions[data.channel] = [];
                    }

                    thiz.pendingSubscriptions[data.channel].forEach(function (f) {
                        thiz.subscriptions[data.channel].push(f);
                    });

                    delete thiz.pendingSubscriptions[data.channel];
                }
            } else if (data.type === "data") {
                if (thiz.subscriptions[data.channel]) {
                    thiz.subscriptions[data.channel].forEach(function (f) {
                        f.call(null, data.data);
                    });
                }
            } else if (data.type === "echo" && data.cmd === "rtt") {
                var delay = (new Date().getTime()) - data.timestamp;

                thiz.echocallback.call(null, delay);
                thiz.echocallback = function () {
                    return;
                };
            }
        };
    });
};

RelayClient.prototype.subscribe = function (channel, callback) {
    var thiz = this;

    if (thiz.subscriptions[channel] !== undefined) {
        thiz.subscriptions[channel].push(callback);
        return;
    }

    if (thiz.pendingSubscriptions[channel] !== undefined) {
        thiz.pendingSubscriptions[channel].push(callback);
        return;
    }

    this.socketConnected.then(function () {
        thiz.socket.send(JSON.stringify({
            type: "subscribe",
            channel: channel
        }));
    });

    this.pendingSubscriptions[channel] = [callback];
};

RelayClient.prototype.unsubscribe = function (channel) {
    var thiz = this;

    this.socketConnected.then(function () {
        thiz.socket.send(JSON.stringify({
            type: "unsubscribe",
            channel: channel
        }));
    });
};

RelayClient.prototype.rtt = function (echocallback) {
    var thiz = this;
    this.echocallback = echocallback;

    this.socketConnected.then(function () {
        thiz.socket.send(JSON.stringify({
            type: "echo",
            cmd: "rtt",
            timestamp: new Date().getTime()
        }));
    });
};

RelayClient.prototype.close = function () {
    this.socket.close();
};
