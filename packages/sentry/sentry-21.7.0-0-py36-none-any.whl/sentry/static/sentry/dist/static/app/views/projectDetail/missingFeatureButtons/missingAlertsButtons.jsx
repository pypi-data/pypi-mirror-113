Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var createAlertButton_1 = tslib_1.__importDefault(require("app/components/createAlertButton"));
var locale_1 = require("app/locale");
var DOCS_URL = 'https://docs.sentry.io/product/alerts-notifications/metric-alerts/';
function MissingAlertsButtons(_a) {
    var organization = _a.organization, projectSlug = _a.projectSlug;
    return (<StyledButtonBar gap={1}>
      <createAlertButton_1.default organization={organization} iconProps={{ size: 'xs' }} size="small" priority="primary" referrer="project_detail" projectSlug={projectSlug} hideIcon>
        {locale_1.t('Create Alert')}
      </createAlertButton_1.default>
      <button_1.default size="small" external href={DOCS_URL}>
        {locale_1.t('Learn More')}
      </button_1.default>
    </StyledButtonBar>);
}
var StyledButtonBar = styled_1.default(buttonBar_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: minmax(auto, max-content) minmax(auto, max-content);\n"], ["\n  grid-template-columns: minmax(auto, max-content) minmax(auto, max-content);\n"])));
exports.default = MissingAlertsButtons;
var templateObject_1;
//# sourceMappingURL=missingAlertsButtons.jsx.map