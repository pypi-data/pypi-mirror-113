Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_select_1 = require("react-select");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function renderEmailValue(status, valueProps) {
    var children = valueProps.children, props = tslib_1.__rest(valueProps, ["children"]);
    var error = status && status.error;
    var emailLabel = status === undefined ? (children) : (<tooltip_1.default disabled={!error} title={error}>
        <EmailLabel>
          {children}
          {!status.sent && !status.error && <SendingIndicator />}
          {status.error && <icons_1.IconWarning size="10px"/>}
          {status.sent && <icons_1.IconCheckmark size="10px" color="success"/>}
        </EmailLabel>
      </tooltip_1.default>);
    return (<react_select_1.components.MultiValue {...props}>{emailLabel}</react_select_1.components.MultiValue>);
}
var EmailLabel = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"])), space_1.default(0.5));
var SendingIndicator = styled_1.default(loadingIndicator_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n  .loading-indicator {\n    border-width: 2px;\n  }\n"], ["\n  margin: 0;\n  .loading-indicator {\n    border-width: 2px;\n  }\n"])));
SendingIndicator.defaultProps = {
    hideMessage: true,
    size: 14,
};
exports.default = renderEmailValue;
var templateObject_1, templateObject_2;
//# sourceMappingURL=renderEmailValue.jsx.map