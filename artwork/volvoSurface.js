function VolvoSurface(svgMappings) {
    this.promises = [];

    for (var key in svgMappings) {
        if (svgMappings.hasOwnProperty(key)) {
            var promise = new Promise(function (resolve, reject) {
                $(key).load(svgMappings[key], function (res, status) {
                    if (status == 'error') {
                        reject()
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
    }
}

(function ($) {
    $.fn.polygon = function (id) {
        var jq = $(this).find("#polygon_" + id);

        jq.lightness = function (baseColor, lightness) {
            $(this).attr("fill", "hsla(" + baseColor + ", 100%, " + lightness + "%, 1)");
        }

        return jq
    }

    $.fn.polygons = function (id) {
        return $(this).find(".polygon");
    }
}(jQuery));
