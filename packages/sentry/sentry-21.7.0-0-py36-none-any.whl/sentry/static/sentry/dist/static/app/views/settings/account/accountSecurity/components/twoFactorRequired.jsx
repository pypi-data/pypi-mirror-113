Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getPendingInvite_1 = tslib_1.__importDefault(require("app/utils/getPendingInvite"));
var TwoFactorRequired = function () {
    return !getPendingInvite_1.default() ? null : (<StyledAlert data-test-id="require-2fa" type="error" icon={<icons_1.IconFlag size="md"/>}>
      {locale_1.tct('You have been invited to an organization that requires [link:two-factor authentication].' +
            ' Setup two-factor authentication below to join your organization.', {
            link: <externalLink_1.default href="https://docs.sentry.io/accounts/require-2fa/"/>,
        })}
    </StyledAlert>);
};
var StyledAlert = styled_1.default(alert_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: ", " 0;\n"], ["\n  margin: ", " 0;\n"])), space_1.default(3));
exports.default = TwoFactorRequired;
var templateObject_1;
//# sourceMappingURL=twoFactorRequired.jsx.map