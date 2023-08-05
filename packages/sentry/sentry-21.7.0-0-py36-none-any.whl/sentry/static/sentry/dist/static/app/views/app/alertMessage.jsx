Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alertActions_1 = tslib_1.__importDefault(require("app/actions/alertActions"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var AlertMessage = function (_a) {
    var _b;
    var alert = _a.alert, system = _a.system;
    var handleCloseAlert = function () {
        alertActions_1.default.closeAlert(alert);
    };
    var url = alert.url, message = alert.message, type = alert.type;
    var icon = type === 'success' ? (<icons_1.IconCheckmark size="md" isCircled/>) : (<icons_1.IconWarning size="md"/>);
    return (<StyledAlert type={type} icon={icon} system={system}>
      <StyledMessage>
        {url ? <externalLink_1.default href={url}>{message}</externalLink_1.default> : message}
      </StyledMessage>
      <StyledCloseButton icon={<icons_1.IconClose size="md" isCircled/>} aria-label={locale_1.t('Close')} onClick={(_b = alert.onClose) !== null && _b !== void 0 ? _b : handleCloseAlert} size="zero" borderless/>
    </StyledAlert>);
};
exports.default = AlertMessage;
var StyledAlert = styled_1.default(alert_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n  margin: 0;\n"], ["\n  padding: ", " ", ";\n  margin: 0;\n"])), space_1.default(1), space_1.default(2));
var StyledMessage = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: block;\n  margin: auto ", " auto 0;\n"], ["\n  display: block;\n  margin: auto ", " auto 0;\n"])), space_1.default(4));
var StyledCloseButton = styled_1.default(button_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  background-color: transparent;\n  opacity: 0.4;\n  transition: opacity 0.1s linear;\n  position: absolute;\n  top: 50%;\n  right: 0;\n  transform: translateY(-50%);\n\n  &:hover,\n  &:focus {\n    background-color: transparent;\n    opacity: 1;\n  }\n"], ["\n  background-color: transparent;\n  opacity: 0.4;\n  transition: opacity 0.1s linear;\n  position: absolute;\n  top: 50%;\n  right: 0;\n  transform: translateY(-50%);\n\n  &:hover,\n  &:focus {\n    background-color: transparent;\n    opacity: 1;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=alertMessage.jsx.map