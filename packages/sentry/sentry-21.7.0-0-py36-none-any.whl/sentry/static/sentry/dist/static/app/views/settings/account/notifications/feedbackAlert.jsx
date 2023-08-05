Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var FeedbackAlert = function () { return (<StyledAlert type="info" icon={<icons_1.IconInfo />}>
    {locale_1.tct('Got feedback? Email [email:ecosystem-feedback@sentry.io].', {
        email: <a href="mailto:ecosystem-feedback@sentry.io"/>,
    })}
  </StyledAlert>); };
var StyledAlert = styled_1.default(alert_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: 20px 0px;\n"], ["\n  margin: 20px 0px;\n"])));
exports.default = FeedbackAlert;
var templateObject_1;
//# sourceMappingURL=feedbackAlert.jsx.map