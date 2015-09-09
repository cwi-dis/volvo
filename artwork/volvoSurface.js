function VolvoSurface(svgMappings) {
    this.promises = [];

    for (var key in svgMappings) {
        if (svgMappings.hasOwnProperty(key)) {
            var promise = new Promise(function (resolve, reject) {
                $(key).load(svgMappings[key], function (res, status) {
                    if (status == 'error') {
                        reject();
                    } else {
                        resolve();
                    }
                });
            });

            this.promises.push(promise);
        }
    }

    this.loaded = function (callback) {
        Promise.all(this.promises).then(callback);
    };
}

(function ($) {
    $.fn.polygon = function (id) {
        var jq = {};

        if (id instanceof Array) {
            var selector = id.map(function (i) {
                return "#polygon_" + i;
            });

            jq = $(this).find(selector.join(","));
        } else {
            jq = $(this).find("#polygon_" + id);
        }

        jq.lightness = function (baseColor, lightness) {
            $(this).attr("fill", "hsla(" + baseColor + ", 100%, " + lightness + "%, 1)");
        };

        jq.getDOMNode = function () {
            return $(this).get(0);
        };

        return jq;
    };

    $.fn.polygons = function (id) {
        var jq = $(this).find(".polygon");

        jq.lightness = function (baseColor, lightness) {
            $(this).attr("fill", "hsla(" + baseColor + ", 100%, " + lightness + "%, 1)");
        };

        return jq;
    };
}(jQuery));
