Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var styles_1 = require("app/components/charts/styles");
var duration_1 = tslib_1.__importDefault(require("app/components/duration"));
var keyValueTable_1 = require("app/components/keyValueTable");
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var seenByList_1 = tslib_1.__importDefault(require("app/components/seenByList"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var index_1 = require("app/views/alerts/details/index");
var constants_1 = require("app/views/alerts/incidentRules/constants");
var presets_1 = require("app/views/alerts/incidentRules/presets");
var types_1 = require("app/views/alerts/incidentRules/types");
var types_2 = require("../types");
var utils_2 = require("../utils");
var activity_1 = tslib_1.__importDefault(require("./activity"));
var chart_1 = tslib_1.__importDefault(require("./chart"));
var DetailsBody = /** @class */ (function (_super) {
    tslib_1.__extends(DetailsBody, _super);
    function DetailsBody() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Object.defineProperty(DetailsBody.prototype, "metricPreset", {
        get: function () {
            var incident = this.props.incident;
            return incident ? utils_2.getIncidentMetricPreset(incident) : undefined;
        },
        enumerable: false,
        configurable: true
    });
    /**
     * Return a string describing the threshold based on the threshold and the type
     */
    DetailsBody.prototype.getThresholdText = function (value, thresholdType, isAlert) {
        if (isAlert === void 0) { isAlert = false; }
        if (!utils_1.defined(value)) {
            return '';
        }
        var isAbove = thresholdType === types_1.AlertRuleThresholdType.ABOVE;
        var direction = isAbove === isAlert ? '>' : '<';
        return direction + " " + value;
    };
    DetailsBody.prototype.renderRuleDetails = function () {
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k;
        var incident = this.props.incident;
        if (incident === undefined) {
            return <placeholder_1.default height="200px"/>;
        }
        var criticalTrigger = incident === null || incident === void 0 ? void 0 : incident.alertRule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'critical';
        });
        var warningTrigger = incident === null || incident === void 0 ? void 0 : incident.alertRule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'warning';
        });
        return (<keyValueTable_1.KeyValueTable>
        <keyValueTable_1.KeyValueTableRow keyName={locale_1.t('Data Source')} value={utils_2.DATA_SOURCE_LABELS[(_a = incident.alertRule) === null || _a === void 0 ? void 0 : _a.dataset]}/>
        <keyValueTable_1.KeyValueTableRow keyName={locale_1.t('Metric')} value={(_b = incident.alertRule) === null || _b === void 0 ? void 0 : _b.aggregate}/>
        <keyValueTable_1.KeyValueTableRow keyName={locale_1.t('Time Window')} value={incident && <duration_1.default seconds={incident.alertRule.timeWindow * 60}/>}/>
        {((_c = incident.alertRule) === null || _c === void 0 ? void 0 : _c.query) && (<keyValueTable_1.KeyValueTableRow keyName={locale_1.t('Filter')} value={<span title={(_d = incident.alertRule) === null || _d === void 0 ? void 0 : _d.query}>{(_e = incident.alertRule) === null || _e === void 0 ? void 0 : _e.query}</span>}/>)}
        <keyValueTable_1.KeyValueTableRow keyName={locale_1.t('Critical Trigger')} value={this.getThresholdText(criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold, (_f = incident.alertRule) === null || _f === void 0 ? void 0 : _f.thresholdType, true)}/>
        {utils_1.defined(warningTrigger) && (<keyValueTable_1.KeyValueTableRow keyName={locale_1.t('Warning Trigger')} value={this.getThresholdText(warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold, (_g = incident.alertRule) === null || _g === void 0 ? void 0 : _g.thresholdType, true)}/>)}

        {utils_1.defined((_h = incident.alertRule) === null || _h === void 0 ? void 0 : _h.resolveThreshold) && (<keyValueTable_1.KeyValueTableRow keyName={locale_1.t('Resolution')} value={this.getThresholdText((_j = incident.alertRule) === null || _j === void 0 ? void 0 : _j.resolveThreshold, (_k = incident.alertRule) === null || _k === void 0 ? void 0 : _k.thresholdType)}/>)}
      </keyValueTable_1.KeyValueTable>);
    };
    DetailsBody.prototype.renderChartHeader = function () {
        var _a, _b, _c, _d, _e;
        var incident = this.props.incident;
        var alertRule = incident === null || incident === void 0 ? void 0 : incident.alertRule;
        return (<ChartHeader>
        <div>
          {(_b = (_a = this.metricPreset) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : locale_1.t('Custom metric')}
          <ChartParameters>
            {locale_1.tct('Metric: [metric] over [window]', {
                metric: <code>{(_c = alertRule === null || alertRule === void 0 ? void 0 : alertRule.aggregate) !== null && _c !== void 0 ? _c : '\u2026'}</code>,
                window: (<code>
                  {incident ? (<duration_1.default seconds={incident.alertRule.timeWindow * 60}/>) : ('\u2026')}
                </code>),
            })}
            {((alertRule === null || alertRule === void 0 ? void 0 : alertRule.query) || ((_d = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _d === void 0 ? void 0 : _d.dataset)) &&
                locale_1.tct('Filter: [datasetType] [filter]', {
                    datasetType: ((_e = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _e === void 0 ? void 0 : _e.dataset) && (<code>{constants_1.DATASET_EVENT_TYPE_FILTERS[incident.alertRule.dataset]}</code>),
                    filter: (alertRule === null || alertRule === void 0 ? void 0 : alertRule.query) && <code>{alertRule.query}</code>,
                })}
          </ChartParameters>
        </div>
      </ChartHeader>);
    };
    DetailsBody.prototype.renderChartActions = function () {
        var _this = this;
        var _a = this.props, incident = _a.incident, params = _a.params, stats = _a.stats;
        return (
        // Currently only one button in pannel, hide panel if not available
        <feature_1.default features={['discover-basic']}>
        <ChartActions>
          <projects_1.default slugs={incident === null || incident === void 0 ? void 0 : incident.projects} orgId={params.orgId}>
            {function (_a) {
                var initiallyLoaded = _a.initiallyLoaded, fetching = _a.fetching, projects = _a.projects;
                var preset = _this.metricPreset;
                var ctaOpts = {
                    orgSlug: params.orgId,
                    projects: (initiallyLoaded ? projects : []),
                    incident: incident,
                    stats: stats,
                };
                var _b = preset
                    ? preset.makeCtaParams(ctaOpts)
                    : presets_1.makeDefaultCta(ctaOpts), buttonText = _b.buttonText, props = tslib_1.__rest(_b, ["buttonText"]);
                return (<button_1.default size="small" priority="primary" disabled={!incident || fetching || !initiallyLoaded} {...props}>
                  {buttonText}
                </button_1.default>);
            }}
          </projects_1.default>
        </ChartActions>
      </feature_1.default>);
    };
    DetailsBody.prototype.render = function () {
        var _a, _b;
        var _c = this.props, params = _c.params, incident = _c.incident, organization = _c.organization, stats = _c.stats;
        var hasRedesign = (incident === null || incident === void 0 ? void 0 : incident.alertRule) &&
            !utils_2.isIssueAlert(incident === null || incident === void 0 ? void 0 : incident.alertRule) &&
            organization.features.includes('alert-details-redesign');
        var alertRuleLink = hasRedesign && incident
            ? index_1.alertDetailsLink(organization, incident)
            : "/organizations/" + params.orgId + "/alerts/metric-rules/" + (incident === null || incident === void 0 ? void 0 : incident.projects[0]) + "/" + ((_a = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _a === void 0 ? void 0 : _a.id) + "/";
        return (<StyledPageContent>
        <Main>
          {incident &&
                incident.status === types_2.IncidentStatus.CLOSED &&
                incident.statusMethod === types_2.IncidentStatusMethod.RULE_UPDATED && (<AlertWrapper>
                <alert_1.default type="warning" icon={<icons_1.IconWarning size="sm"/>}>
                  {locale_1.t('This alert has been auto-resolved because the rule that triggered it has been modified or deleted')}
                </alert_1.default>
              </AlertWrapper>)}
          <organization_1.PageContent>
            <ChartPanel>
              <panels_1.PanelBody withPadding>
                {this.renderChartHeader()}
                {incident && stats ? (<chart_1.default triggers={incident.alertRule.triggers} resolveThreshold={incident.alertRule.resolveThreshold} aggregate={incident.alertRule.aggregate} data={stats.eventStats.data} started={incident.dateStarted} closed={incident.dateClosed || undefined}/>) : (<placeholder_1.default height="200px"/>)}
              </panels_1.PanelBody>
              {this.renderChartActions()}
            </ChartPanel>
          </organization_1.PageContent>
          <DetailWrapper>
            <ActivityPageContent>
              <StyledNavTabs underlined>
                <li className="active">
                  <link_1.default to="">{locale_1.t('Activity')}</link_1.default>
                </li>

                <SeenByTab>
                  {incident && (<StyledSeenByList iconPosition="right" seenBy={incident.seenBy} iconTooltip={locale_1.t('People who have viewed this alert')}/>)}
                </SeenByTab>
              </StyledNavTabs>
              <activity_1.default incident={incident} params={params} incidentStatus={!!incident ? incident.status : null}/>
            </ActivityPageContent>
            <Sidebar>
              <SidebarHeading>
                <span>{locale_1.t('Alert Rule')}</span>
                {(((_b = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _b === void 0 ? void 0 : _b.status) !== types_2.AlertRuleStatus.SNAPSHOT ||
                hasRedesign) && (<SideHeaderLink disabled={!!(incident === null || incident === void 0 ? void 0 : incident.id)} to={(incident === null || incident === void 0 ? void 0 : incident.id)
                    ? {
                        pathname: alertRuleLink,
                    }
                    : ''}>
                    {locale_1.t('View Alert Rule')}
                  </SideHeaderLink>)}
              </SidebarHeading>
              {this.renderRuleDetails()}
            </Sidebar>
          </DetailWrapper>
        </Main>
      </StyledPageContent>);
    };
    return DetailsBody;
}(react_1.Component));
exports.default = DetailsBody;
var Main = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  background-color: ", ";\n  padding-top: ", ";\n  flex-grow: 1;\n"], ["\n  background-color: ", ";\n  padding-top: ", ";\n  flex-grow: 1;\n"])), function (p) { return p.theme.background; }, space_1.default(3));
var DetailWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n\n  @media (max-width: ", ") {\n    flex-direction: column-reverse;\n  }\n"], ["\n  display: flex;\n  flex: 1;\n\n  @media (max-width: ", ") {\n    flex-direction: column-reverse;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var ActivityPageContent = styled_1.default(organization_1.PageContent)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  @media (max-width: ", ") {\n    width: 100%;\n    margin-bottom: 0;\n  }\n"], ["\n  @media (max-width: ", ") {\n    width: 100%;\n    margin-bottom: 0;\n  }\n"])), theme_1.default.breakpoints[0]);
var Sidebar = styled_1.default(organization_1.PageContent)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  width: 400px;\n  flex: none;\n  padding-top: ", ";\n\n  @media (max-width: ", ") {\n    width: 100%;\n    padding-top: ", ";\n    margin-bottom: 0;\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  width: 400px;\n  flex: none;\n  padding-top: ", ";\n\n  @media (max-width: ", ") {\n    width: 100%;\n    padding-top: ", ";\n    margin-bottom: 0;\n    border-bottom: 1px solid ", ";\n  }\n"])), space_1.default(3), theme_1.default.breakpoints[0], space_1.default(3), function (p) { return p.theme.border; });
var SidebarHeading = styled_1.default(styles_1.SectionHeading)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
var SideHeaderLink = styled_1.default(link_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  font-weight: normal;\n"], ["\n  font-weight: normal;\n"])));
var StyledPageContent = styled_1.default(organization_1.PageContent)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n  flex-direction: column;\n"], ["\n  padding: 0;\n  flex-direction: column;\n"])));
var ChartPanel = styled_1.default(panels_1.Panel)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject([""], [""])));
var ChartHeader = styled_1.default('header')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(1));
var ChartActions = styled_1.default(panels_1.PanelFooter)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  padding: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  padding: ", ";\n"])), space_1.default(2));
var ChartParameters = styled_1.default('div')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  grid-gap: ", ";\n  align-items: center;\n  overflow-x: auto;\n\n  > * {\n    position: relative;\n  }\n\n  > *:not(:last-of-type):after {\n    content: '';\n    display: block;\n    height: 70%;\n    width: 1px;\n    background: ", ";\n    position: absolute;\n    right: -", ";\n    top: 15%;\n  }\n"], ["\n  color: ", ";\n  font-size: ", ";\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  grid-gap: ", ";\n  align-items: center;\n  overflow-x: auto;\n\n  > * {\n    position: relative;\n  }\n\n  > *:not(:last-of-type):after {\n    content: '';\n    display: block;\n    height: 70%;\n    width: 1px;\n    background: ", ";\n    position: absolute;\n    right: -", ";\n    top: 15%;\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(4), function (p) { return p.theme.gray200; }, space_1.default(2));
var AlertWrapper = styled_1.default('div')(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", " 0;\n"], ["\n  padding: ", " ", " 0;\n"])), space_1.default(2), space_1.default(4));
var StyledNavTabs = styled_1.default(navTabs_1.default)(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var SeenByTab = styled_1.default('li')(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  margin-left: ", ";\n  margin-right: 0;\n\n  .nav-tabs > & {\n    margin-right: 0;\n  }\n"], ["\n  flex: 1;\n  margin-left: ", ";\n  margin-right: 0;\n\n  .nav-tabs > & {\n    margin-right: 0;\n  }\n"])), space_1.default(2));
var StyledSeenByList = styled_1.default(seenByList_1.default)(templateObject_15 || (templateObject_15 = tslib_1.__makeTemplateObject(["\n  margin-top: 0;\n"], ["\n  margin-top: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15;
//# sourceMappingURL=body.jsx.map