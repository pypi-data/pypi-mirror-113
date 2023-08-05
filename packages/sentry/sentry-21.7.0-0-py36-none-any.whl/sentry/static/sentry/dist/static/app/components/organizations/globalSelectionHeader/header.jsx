Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Header = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  display: flex;\n  width: 100%;\n  height: 60px;\n\n  border-bottom: 1px solid ", ";\n  box-shadow: ", ";\n  z-index: ", ";\n\n  background: ", ";\n  font-size: ", ";\n  @media (min-width: ", " and max-width: ", ") {\n    margin-top: 54px;\n  }\n  @media (max-width: calc(", " - 1px)) {\n    margin-top: 0;\n  }\n"], ["\n  position: relative;\n  display: flex;\n  width: 100%;\n  height: 60px;\n\n  border-bottom: 1px solid ", ";\n  box-shadow: ", ";\n  z-index: ", ";\n\n  background: ", ";\n  font-size: ", ";\n  @media (min-width: ", " and max-width: ", ") {\n    margin-top: 54px;\n  }\n  @media (max-width: calc(", " - 1px)) {\n    margin-top: 0;\n  }\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.zIndex.globalSelectionHeader; }, function (p) { return p.theme.headerBackground; }, function (p) { return p.theme.fontSizeExtraLarge; }, function (props) { return props.theme.breakpoints[0]; }, function (props) {
    return props.theme.breakpoints[1];
}, function (props) { return props.theme.breakpoints[0]; });
exports.default = Header;
var templateObject_1;
//# sourceMappingURL=header.jsx.map