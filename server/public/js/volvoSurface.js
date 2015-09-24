/**
 * Initialise SVG surfaces by loading them asynchronously.
 *
 * This function is intended to be used as a constructor for initialising
 * a series of SVG graphics by loading them via AJAX and placing them into
 * given DOM elements. When called, the function expects a dictionary with a
 * set of key-value pairs, where the keys designate CSS selectors and the
 * values are URL of the SVG graphics to be loaded into the DOM element which
 * matches the given selector.
 *
 * The elements are wrapped into promises and loaded from the server. If (and
 * only if) all of the given elements were loaded correctly a callback passed
 * to the method loaded() is invoked. This callback is where application code
 * should be placed. For example:
 *
 *   var surface = new VolvoSurface({
 *     "#container1": "js/img1.svg",
 *     "#container2": "js/img2.svg"
 *   });
 *
 *   surface.loaded(function () {
 *     console.log("all SVGs loaded");
 *     // application code goes here
 *   });
 *
 * In the example above a new object is created and the constructor function
 * will try to load img1.svg and img2.svg via AJAX and place the contents into
 * the DOM elements with the IDs container1 and container2 respectively. Once
 * the elements are both successfully loaded, the callback passed to loaded()
 * is invoked and 'all SVGs loaded' will be printed. Application code should be
 * placed inside this callback.
 **/
function VolvoSurface(svgMappings) {
    // array where all promises for AJAX calls are stored
    this.promises = [];

    // iterate object
    for (var key in svgMappings) {
        if (svgMappings.hasOwnProperty(key)) {
            // create new promise for each AJAX call
            var promise = new Promise(function (resolve, reject) {
                // load SVG and place it into the element designated by 'key'.
                // see http://api.jquery.com/load/ for documentation on the
                // .load() function
                $(key).load(svgMappings[key], function (res, status) {
                    // reject the promise in case of error resolve otherwise
                    if (status == 'error') {
                        reject();
                    } else {
                        resolve();
                    }
                });
            });

            // add promise to array
            this.promises.push(promise);
        }
    }

    this.loaded = function (callback) {
        // if all promises resolve successfully, invoke the callback
        Promise.all(this.promises).then(callback);
    };
}

/**
 * jQuery plugin which adds methods for working with some SVG elements.
 *
 * This plugin attaches the function .polygon() to the jquery namespace. This
 * function can be passed a number or an array of numbers and will select all
 * polygons matching the numbers from a specially annotated SVG. If the
 * function is called without any arguments it will return all polygons which
 * have the special annotation.
 *
 * Moreover, the attaches a function .lightness() to the matched elements,
 * which enables one to easily adjust the lightness of the selected polygons.
 * The first value to be passed into that function is the hue of the desired
 * colour between 0 and 360 and the second value the desired brightness with 0
 * being black, 50 being the selected colour and 100 being white. Check
 * http://hslpicker.com/ for reference on the HSL colour model.
 *
 *   $("#container1").polygon(12).lightness(60, 80);
 *   $("#container1").polygon([1,2,3]).lightness(60, 80);
 *   $("#container1").polygon().lightness(60, 80);
 *
 * In the example above a light yellow colour is applied to the polygon with
 * number 12, the polygons with numbers 1, 2 and three and to all polygons
 * respectively. Note that the example assumes, that the SVG and thus the
 * annotated polygons, are descendants of (i.e. contained in) the DOM node with
 * id container1. If you want to modify any other properties of the polygons,
 * you can use jQuery's .attr() method, for instance:
 *
 *   $("#container1").polygon([1, 2]).attr("stroke-width", 1.5);
 *
 * The example sets the stroke width of the polygons with numbers 1 and 2 in
 * the DOM * element container1 to 1.5. If you prefer to work with raw DOM
 * nodes, you can do so by accessing them via indexing:
 *
 *  $("#container1").polygon(2)[0].style.fill = "#FF0000";
 *
 * Note that this applies the style only to the first element (i.e. index 0).
 * If you want to apply the style to multiple elements, you'd have to iterate
 * them:
 *
 *   var matchedElements = $("#container1").polygon([1,2,3]);
 *
 *   for (var i=0; i<matchedElements.length; i++) {
 *     matchedElements[i].style.fill = "#FF0000";
 *   }
 *
 * This is why .attr() is the preferred method. It provides a means to set any
 * property of a set of DOM elements at once. See http://api.jquery.com/attr/
 * for further reference. (Note that CSS properties should be set using the
 * method .css(); see http://api.jquery.com/css/)
 **/
(function ($) {
    $.fn.polygon = function (id) {
        var jq = {};

        if (id === undefined) {
            // if no argument was provided, return all polygons
            jq = $(this).find(".polygon");
        } else if (id instanceof Array) {
            // if an array was provided, return matching polygons

            // build selector
            var selector = id.map(function (i) {
                return i;
            });


            jq = $(this).find(selector.join(","));
        } else {
            // if a single element was provided use it to create selector
            jq = $(this).find(id);
        }

        // attach function lightness() to the set of matched elements
        jq.setHSLA = function (hue, saturation, lightness, alpha) {
            // if lightness is 100 (pure white) make background transparent
            if (lightness === 100) {
                $(this).attr("fill", "none");
            } else {
                // set base colour and lightness using HSLA with saturation
                // fixed at 100% and an opacity of 0.7
                $(this).attr("fill", "hsla(" + hue + ", " + saturation + "%, " + lightness + "%, " + alpha + ")");
            }
        };

        // return set of matched elements
        return jq;
    };
}(jQuery));
