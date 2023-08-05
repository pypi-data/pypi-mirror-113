Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var startCase_1 = tslib_1.__importDefault(require("lodash/startCase"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var pluginIcon_1 = tslib_1.__importDefault(require("app/plugins/components/pluginIcon"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var integrationUtil_1 = require("app/utils/integrationUtil");
var integrationStatus_1 = tslib_1.__importDefault(require("./integrationStatus"));
var urlMap = {
    plugin: 'plugins',
    firstParty: 'integrations',
    sentryApp: 'sentry-apps',
    documentIntegration: 'document-integrations',
};
var IntegrationRow = function (props) {
    var organization = props.organization, type = props.type, slug = props.slug, displayName = props.displayName, status = props.status, publishStatus = props.publishStatus, configurations = props.configurations, categories = props.categories, alertText = props.alertText;
    var baseUrl = publishStatus === 'internal'
        ? "/settings/" + organization.slug + "/developer-settings/" + slug + "/"
        : "/settings/" + organization.slug + "/" + urlMap[type] + "/" + slug + "/";
    var renderDetails = function () {
        if (type === 'sentryApp') {
            return publishStatus !== 'published' && <PublishStatus status={publishStatus}/>;
        }
        // TODO: Use proper translations
        return configurations > 0 ? (<StyledLink to={baseUrl + "?tab=configurations"}>{configurations + " Configuration" + (configurations > 1 ? 's' : '')}</StyledLink>) : null;
    };
    var renderStatus = function () {
        // status should be undefined for document integrations
        if (status) {
            return <integrationStatus_1.default status={status}/>;
        }
        return <LearnMore to={baseUrl}>{locale_1.t('Learn More')}</LearnMore>;
    };
    return (<PanelRow noPadding data-test-id={slug}>
      <FlexContainer>
        <pluginIcon_1.default size={36} pluginId={slug}/>
        <Container>
          <IntegrationName to={baseUrl}>{displayName}</IntegrationName>
          <IntegrationDetails>
            {renderStatus()}
            {renderDetails()}
          </IntegrationDetails>
        </Container>
        <InternalContainer>
          {categories === null || categories === void 0 ? void 0 : categories.map(function (category) { return (<CategoryTag key={category} category={startCase_1.default(category)} priority={category === publishStatus}/>); })}
        </InternalContainer>
      </FlexContainer>
      {alertText && (<AlertContainer>
          <alert_1.default type="warning" icon={<icons_1.IconWarning size="sm"/>}>
            <span>{alertText}</span>
            <ResolveNowButton href={baseUrl + "?tab=configurations&referrer=directory_resolve_now"} size="xsmall" onClick={function () {
                return integrationUtil_1.trackIntegrationEvent('integrations.resolve_now_clicked', {
                    integration_type: integrationUtil_1.convertIntegrationTypeToSnakeCase(type),
                    integration: slug,
                }, organization);
            }}>
              {locale_1.t('Resolve Now')}
            </ResolveNowButton>
          </alert_1.default>
        </AlertContainer>)}
    </PanelRow>);
};
var PanelRow = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  flex-direction: column;\n"], ["\n  flex-direction: column;\n"])));
var FlexContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n"])), space_1.default(2));
var InternalContainer = styled_1.default(FlexContainer)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: 0 ", ";\n"], ["\n  padding: 0 ", ";\n"])), space_1.default(2));
var Container = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  padding: 0 16px;\n"], ["\n  flex: 1;\n  padding: 0 16px;\n"])));
var IntegrationName = styled_1.default(link_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
var IntegrationDetails = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-top: 6px;\n  font-size: 0.8em;\n"], ["\n  display: flex;\n  align-items: center;\n  margin-top: 6px;\n  font-size: 0.8em;\n"])));
var StyledLink = styled_1.default(link_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  &:before {\n    content: '|';\n    color: ", ";\n    margin-right: ", ";\n    font-weight: normal;\n  }\n"], ["\n  color: ", ";\n  &:before {\n    content: '|';\n    color: ", ";\n    margin-right: ", ";\n    font-weight: normal;\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.gray200; }, space_1.default(0.75));
var LearnMore = styled_1.default(link_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var PublishStatus = styled_1.default(function (_a) {
    var status = _a.status, props = tslib_1.__rest(_a, ["status"]);
    return (<div {...props}>{locale_1.t("" + status)}</div>);
})(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-weight: light;\n  margin-right: ", ";\n  text-transform: capitalize;\n  &:before {\n    content: '|';\n    color: ", ";\n    margin-right: ", ";\n    font-weight: normal;\n  }\n"], ["\n  color: ", ";\n  font-weight: light;\n  margin-right: ", ";\n  text-transform: capitalize;\n  &:before {\n    content: '|';\n    color: ", ";\n    margin-right: ", ";\n    font-weight: normal;\n  }\n"])), function (props) {
    return props.status === 'published' ? props.theme.success : props.theme.gray300;
}, space_1.default(0.75), function (p) { return p.theme.gray200; }, space_1.default(0.75));
// TODO(Priscila): Replace this component with the Tag component
var CategoryTag = styled_1.default(function (_a) {
    var _priority = _a.priority, category = _a.category, p = tslib_1.__rest(_a, ["priority", "category"]);
    return <div {...p}>{category}</div>;
})(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  padding: 1px 10px;\n  background: ", ";\n  border-radius: 20px;\n  font-size: ", ";\n  margin-right: ", ";\n  line-height: ", ";\n  text-align: center;\n  color: ", ";\n"], ["\n  display: flex;\n  flex-direction: row;\n  padding: 1px 10px;\n  background: ", ";\n  border-radius: 20px;\n  font-size: ", ";\n  margin-right: ", ";\n  line-height: ", ";\n  text-align: center;\n  color: ", ";\n"])), function (p) { return (p.priority ? p.theme.purple200 : p.theme.gray100); }, space_1.default(1.5), space_1.default(1), space_1.default(3), function (p) { return (p.priority ? p.theme.white : p.theme.gray500); });
var ResolveNowButton = styled_1.default(button_1.default)(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  float: right;\n"], ["\n  color: ", ";\n  float: right;\n"])), function (p) { return p.theme.subText; });
var AlertContainer = styled_1.default('div')(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  padding: 0px ", " 0px 68px;\n"], ["\n  padding: 0px ", " 0px 68px;\n"])), space_1.default(3));
exports.default = IntegrationRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12;
//# sourceMappingURL=integrationRow.jsx.map