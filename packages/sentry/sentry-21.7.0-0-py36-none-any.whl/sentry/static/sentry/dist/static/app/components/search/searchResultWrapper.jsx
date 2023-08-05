Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var SearchResultWrapper = styled_1.default(function (_a) {
    var highlighted = _a.highlighted, props = tslib_1.__rest(_a, ["highlighted"]);
    return (<div {...props} ref={function (element) { var _a; return highlighted && ((_a = element === null || element === void 0 ? void 0 : element.scrollIntoView) === null || _a === void 0 ? void 0 : _a.call(element, { block: 'nearest' })); }}/>);
})(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  cursor: pointer;\n  display: block;\n  color: ", ";\n  padding: 10px;\n  scroll-margin: 120px;\n\n  ", ";\n\n  &:not(:first-child) {\n    border-top: 1px solid ", ";\n  }\n"], ["\n  cursor: pointer;\n  display: block;\n  color: ", ";\n  padding: 10px;\n  scroll-margin: 120px;\n\n  ", ";\n\n  &:not(:first-child) {\n    border-top: 1px solid ", ";\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) {
    return p.highlighted && react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n      color: ", ";\n      background: ", ";\n    "], ["\n      color: ", ";\n      background: ", ";\n    "])), p.theme.purple300, p.theme.backgroundSecondary);
}, function (p) { return p.theme.innerBorder; });
exports.default = SearchResultWrapper;
var templateObject_1, templateObject_2;
//# sourceMappingURL=searchResultWrapper.jsx.map