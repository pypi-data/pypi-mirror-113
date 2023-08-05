Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var is_prop_valid_1 = tslib_1.__importDefault(require("@emotion/is-prop-valid"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var breadcrumbs_1 = tslib_1.__importDefault(require("app/components/breadcrumbs"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var pageHeading_1 = tslib_1.__importDefault(require("app/components/pageHeading"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("../../utils");
function DetailsHeader(_a) {
    var _b;
    var hasIncidentRuleDetailsError = _a.hasIncidentRuleDetailsError, rule = _a.rule, params = _a.params;
    var isRuleReady = !!rule && !hasIncidentRuleDetailsError;
    var project = (_b = rule === null || rule === void 0 ? void 0 : rule.projects) === null || _b === void 0 ? void 0 : _b[0];
    var settingsLink = rule &&
        "/organizations/" + params.orgId + "/alerts/" + (utils_1.isIssueAlert(rule) ? 'rules' : 'metric-rules') + "/" + project + "/" + rule.id + "/";
    return (<Header>
      <BreadCrumbBar>
        <AlertBreadcrumbs crumbs={[
            { label: locale_1.t('Alerts'), to: "/organizations/" + params.orgId + "/alerts/rules/" },
            { label: locale_1.t('Alert Rule') },
        ]}/>
        <Controls>
          <button_1.default icon={<icons_1.IconEdit />} to={settingsLink}>
            {locale_1.t('Edit Rule')}
          </button_1.default>
        </Controls>
      </BreadCrumbBar>
      <Details>
        <RuleTitle data-test-id="incident-rule-title" loading={!isRuleReady}>
          {rule && !hasIncidentRuleDetailsError ? rule.name : locale_1.t('Loading')}
        </RuleTitle>
      </Details>
    </Header>);
}
exports.default = DetailsHeader;
var Header = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n"], ["\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; });
var BreadCrumbBar = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  margin-bottom: 0;\n  padding: ", " ", " ", ";\n"], ["\n  display: flex;\n  margin-bottom: 0;\n  padding: ", " ", " ", ";\n"])), space_1.default(2), space_1.default(4), space_1.default(1));
var AlertBreadcrumbs = styled_1.default(breadcrumbs_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n  font-size: ", ";\n  padding: 0;\n"], ["\n  flex-grow: 1;\n  font-size: ", ";\n  padding: 0;\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var Controls = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"])), space_1.default(1));
var Details = styled_1.default(organization_1.PageHeader)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n  padding: ", " ", " ", ";\n\n  grid-template-columns: max-content auto;\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n\n  @media (max-width: ", ") {\n    grid-template-columns: auto;\n    grid-auto-flow: row;\n  }\n"], ["\n  margin-bottom: 0;\n  padding: ", " ", " ", ";\n\n  grid-template-columns: max-content auto;\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n\n  @media (max-width: ", ") {\n    grid-template-columns: auto;\n    grid-auto-flow: row;\n  }\n"])), space_1.default(1.5), space_1.default(4), space_1.default(2), space_1.default(3), function (p) { return p.theme.breakpoints[1]; });
var RuleTitle = styled_1.default(pageHeading_1.default, {
    shouldForwardProp: function (p) { return typeof p === 'string' && is_prop_valid_1.default(p) && p !== 'loading'; },
})(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  ", ";\n  line-height: 1.5;\n"], ["\n  ", ";\n  line-height: 1.5;\n"])), function (p) { return p.loading && 'opacity: 0'; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=header.jsx.map