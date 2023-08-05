Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getPadding = function (_a) {
    var disablePadding = _a.disablePadding, hasButtons = _a.hasButtons;
    return react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n  padding-right: ", ";\n"], ["\n  padding: ", " ", ";\n  padding-right: ", ";\n"])), hasButtons ? space_1.default(1) : space_1.default(2), disablePadding ? 0 : space_1.default(2), hasButtons ? space_1.default(1) : null);
};
var PanelHeader = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  color: ", ";\n  font-size: ", ";\n  font-weight: 600;\n  text-transform: uppercase;\n  border-bottom: 1px solid ", ";\n  border-radius: ", " ", " 0 0;\n  background: ", ";\n  line-height: 1;\n  position: relative;\n  ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  color: ", ";\n  font-size: ", ";\n  font-weight: 600;\n  text-transform: uppercase;\n  border-bottom: 1px solid ", ";\n  border-radius: ", " ", " 0 0;\n  background: ", ";\n  line-height: 1;\n  position: relative;\n  ", ";\n"])), function (p) { return (p.lightText ? p.theme.gray300 : p.theme.gray400); }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.backgroundSecondary; }, getPadding);
exports.default = PanelHeader;
var templateObject_1, templateObject_2;
//# sourceMappingURL=panelHeader.jsx.map