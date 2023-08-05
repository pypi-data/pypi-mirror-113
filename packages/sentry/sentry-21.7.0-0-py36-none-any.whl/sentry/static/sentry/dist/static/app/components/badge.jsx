Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var Badge = styled_1.default(function (_a) {
    var children = _a.children, text = _a.text, props = tslib_1.__rest(_a, ["children", "text"]);
    return (<span {...props}>{children !== null && children !== void 0 ? children : text}</span>);
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  height: 20px;\n  min-width: 20px;\n  line-height: 20px;\n  border-radius: 20px;\n  padding: 0 5px;\n  margin-left: ", ";\n  font-size: 75%;\n  font-weight: 600;\n  text-align: center;\n  color: ", ";\n  background: ", ";\n  transition: background 100ms linear;\n\n  position: relative;\n  top: -1px;\n"], ["\n  display: inline-block;\n  height: 20px;\n  min-width: 20px;\n  line-height: 20px;\n  border-radius: 20px;\n  padding: 0 5px;\n  margin-left: ", ";\n  font-size: 75%;\n  font-weight: 600;\n  text-align: center;\n  color: ", ";\n  background: ", ";\n  transition: background 100ms linear;\n\n  position: relative;\n  top: -1px;\n"])), space_1.default(0.5), function (p) { var _a; return p.theme.badge[(_a = p.type) !== null && _a !== void 0 ? _a : 'default'].color; }, function (p) { var _a; return p.theme.badge[(_a = p.type) !== null && _a !== void 0 ? _a : 'default'].background; });
exports.default = Badge;
var templateObject_1;
//# sourceMappingURL=badge.jsx.map