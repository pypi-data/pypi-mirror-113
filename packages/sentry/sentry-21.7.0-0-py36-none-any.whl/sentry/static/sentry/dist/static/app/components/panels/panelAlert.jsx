Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var icons_1 = require("app/icons");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var DEFAULT_ICONS = {
    info: <icons_1.IconInfo size="md"/>,
    error: <icons_1.IconClose isCircled size="md"/>,
    warning: <icons_1.IconFlag size="md"/>,
    success: <icons_1.IconCheckmark isCircled size="md"/>,
};
// Margin bottom should probably be a different prop
var PanelAlert = styled_1.default(function (_a) {
    var icon = _a.icon, props = tslib_1.__rest(_a, ["icon"]);
    return (<alert_1.default {...props} icon={icon || DEFAULT_ICONS[props.type]} system/>);
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: 0 0 1px 0;\n  padding: ", ";\n  border-radius: 0;\n  box-shadow: none;\n\n  &:last-child {\n    border-bottom: none;\n    margin: 0;\n    border-radius: 0 0 4px 4px;\n  }\n"], ["\n  margin: 0 0 1px 0;\n  padding: ", ";\n  border-radius: 0;\n  box-shadow: none;\n\n  &:last-child {\n    border-bottom: none;\n    margin: 0;\n    border-radius: 0 0 4px 4px;\n  }\n"])), space_1.default(2));
exports.default = PanelAlert;
var templateObject_1;
//# sourceMappingURL=panelAlert.jsx.map