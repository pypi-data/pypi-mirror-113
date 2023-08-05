Object.defineProperty(exports, "__esModule", { value: true });
exports.IconWrapper = exports.GridCellLeft = exports.GridCell = exports.aroundContentStyle = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var IconWrapper = styled_1.default('div', {
    shouldForwardProp: function (prop) { return prop !== 'color'; },
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  width: 26px;\n  height: 26px;\n  background: ", ";\n  box-shadow: ", ";\n  border-radius: 32px;\n  z-index: ", ";\n  position: relative;\n  border: 1px solid ", ";\n  color: ", ";\n  ", "\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  width: 26px;\n  height: 26px;\n  background: ", ";\n  box-shadow: ", ";\n  border-radius: 32px;\n  z-index: ", ";\n  position: relative;\n  border: 1px solid ", ";\n  color: ", ";\n  ", "\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.dropShadowLightest; }, function (p) { return p.theme.zIndex.breadcrumbs.iconWrapper; }, function (p) { return p.theme.border; }, function (p) { return p.theme.textColor; }, function (p) {
    return p.color &&
        "\n      color: " + (p.theme[p.color] || p.color) + ";\n      border-color: " + (p.theme[p.color] || p.color) + ";\n    ";
});
exports.IconWrapper = IconWrapper;
var GridCell = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  height: ", ";\n  position: relative;\n  white-space: pre-wrap;\n  word-break: break-all;\n  border-bottom: 1px solid ", ";\n  padding: ", ";\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n  }\n  ", "\n  ", ";\n"], ["\n  height: ", ";\n  position: relative;\n  white-space: pre-wrap;\n  word-break: break-all;\n  border-bottom: 1px solid ", ";\n  padding: ", ";\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n  }\n  ", "\n  ", ";\n"])), function (p) { return (p.height ? p.height + "px" : '100%'); }, function (p) { return p.theme.innerBorder; }, space_1.default(1), function (p) { return p.theme.breakpoints[0]; }, space_1.default(1), space_1.default(2), function (p) {
    return p.hasError &&
        "\n      border-bottom: 1px solid " + p.theme.red300 + ";\n      :after {\n        content: '';\n        position: absolute;\n        top: -1px;\n        left: 0;\n        height: 1px;\n        width: 100%;\n        background: " + p.theme.red300 + ";\n      }\n    ";
}, function (p) { return p.isLastItem && "border-bottom: none"; });
exports.GridCell = GridCell;
var GridCellLeft = styled_1.default(GridCell)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n  line-height: 1;\n  padding: ", " ", " ", " ", ";\n  :before {\n    content: '';\n    display: block;\n    width: 1px;\n    top: 0;\n    bottom: 0;\n    left: 21px;\n    background: ", ";\n    position: absolute;\n    @media (min-width: ", ") {\n      left: 29px;\n    }\n  }\n"], ["\n  align-items: center;\n  line-height: 1;\n  padding: ", " ", " ", " ", ";\n  :before {\n    content: '';\n    display: block;\n    width: 1px;\n    top: 0;\n    bottom: 0;\n    left: 21px;\n    background: ", ";\n    position: absolute;\n    @media (min-width: ", ") {\n      left: 29px;\n    }\n  }\n"])), space_1.default(1), space_1.default(0.5), space_1.default(1), space_1.default(1), function (p) { return (p.hasError ? p.theme.red300 : p.theme.innerBorder); }, function (p) { return p.theme.breakpoints[0]; });
exports.GridCellLeft = GridCellLeft;
var aroundContentStyle = function (p) { return "\n  border: 1px solid " + p.theme.border + ";\n  border-radius: " + p.theme.borderRadius + ";\n  box-shadow: " + p.theme.dropShadowLightest + ";\n  z-index: 1;\n"; };
exports.aroundContentStyle = aroundContentStyle;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=styles.jsx.map