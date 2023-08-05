Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var BaseButton = function (props) { return (<button_1.default size="zero" {...props}/>); };
var ActionButton = styled_1.default(BaseButton)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n  font-size: ", ";\n"], ["\n  padding: ", " ", ";\n  font-size: ", ";\n"])), function (p) { return (p.icon ? space_1.default(0.75) : '7px'); }, space_1.default(1), function (p) { return p.theme.fontSizeSmall; });
exports.default = ActionButton;
var templateObject_1;
//# sourceMappingURL=button.jsx.map