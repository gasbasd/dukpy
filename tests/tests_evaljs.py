import json
import dukpy
from diffreport import report_diff


class TestEvalJS(object):
    def test_object_return(self):
        ans = dukpy.evaljs(["var o = {'value': 5}",
                            "o['value'] += 3",
                            "o"])
        assert ans == {'value': 8}

    def test_coffee(self):
        ans = dukpy.coffee_compile('''
    fill = (container, liquid = "coffee") ->
        "Filling the #{container} with #{liquid}..."
''')
        assert ans == '''(function() {
  var fill;

  fill = function(container, liquid) {
    if (liquid == null) {
      liquid = "coffee";
    }
    return "Filling the " + container + " with " + liquid + "...";
  };

}).call(this);
'''

    def test_sum(self):
        n = dukpy.evaljs("dukpy['value'] + 3", value=7)
        assert n == 10

    def test_babel(self):
        ans = dukpy.babel_compile('''
class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
    toString() {
        return '(' + this.x + ', ' + this.y + ')';
    }
}
''')
        assert '''var Point = (function () {
    function Point(x, y) {
''' in ans['code'], ans['code']

    def test_typescript(self):
        ans = dukpy.typescript_compile('''
class Greeter {
    constructor(public greeting: string) { }
    greet() {
        return "<h1>" + this.greeting + "</h1>";
    }
};

var greeter = new Greeter("Hello, world!");
''')

        expected = """System.register([], function(exports_1) {
    var Greeter, greeter;
    return {
        setters:[],
        execute: function() {
            var Greeter = (function () {
                function Greeter(greeting) {
                    this.greeting = greeting;
                }
                Greeter.prototype.greet = function () {
                    return "<h1>" + this.greeting + "</h1>";
                };
                return Greeter;
            })();
            ;
            var greeter = new Greeter("Hello, world!");
        }
    }
});"""

        assert expected in ans, report_diff(expected, ans)
