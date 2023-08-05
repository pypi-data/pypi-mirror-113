Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var actorAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/actorAvatar"));
var styles_1 = require("app/components/charts/styles");
var utils_1 = require("app/components/charts/utils");
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var duration_1 = tslib_1.__importDefault(require("app/components/duration"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var keyValueTable_1 = require("app/components/keyValueTable");
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var types_1 = require("app/views/alerts/incidentRules/types");
var getEventTypeFilter_1 = require("app/views/alerts/incidentRules/utils/getEventTypeFilter");
var timeline_1 = tslib_1.__importDefault(require("app/views/alerts/rules/details/timeline"));
var alertBadge_1 = tslib_1.__importDefault(require("../../alertBadge"));
var types_2 = require("../../types");
var constants_1 = require("./constants");
var metricChart_1 = tslib_1.__importDefault(require("./metricChart"));
var relatedIssues_1 = tslib_1.__importDefault(require("./relatedIssues"));
var relatedTransactions_1 = tslib_1.__importDefault(require("./relatedTransactions"));
var DetailsBody = /** @class */ (function (_super) {
    tslib_1.__extends(DetailsBody, _super);
    function DetailsBody() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DetailsBody.prototype.getMetricText = function () {
        var rule = this.props.rule;
        if (!rule) {
            return '';
        }
        var aggregate = rule.aggregate;
        return locale_1.tct('[metric]', {
            metric: aggregate,
        });
    };
    DetailsBody.prototype.getTimeWindow = function () {
        var rule = this.props.rule;
        if (!rule) {
            return '';
        }
        var timeWindow = rule.timeWindow;
        return locale_1.tct('[window]', {
            window: <duration_1.default seconds={timeWindow * 60}/>,
        });
    };
    DetailsBody.prototype.getInterval = function () {
        var _a = this.props, _b = _a.timePeriod, start = _b.start, end = _b.end, rule = _a.rule;
        var startDate = moment_1.default.utc(start);
        var endDate = moment_1.default.utc(end);
        var timeWindow = rule === null || rule === void 0 ? void 0 : rule.timeWindow;
        if (timeWindow &&
            endDate.diff(startDate) < constants_1.API_INTERVAL_POINTS_LIMIT * timeWindow * 60 * 1000) {
            return timeWindow + "m";
        }
        return utils_1.getInterval({ start: start, end: end }, true);
    };
    DetailsBody.prototype.getFilter = function () {
        var rule = this.props.rule;
        if (!rule) {
            return null;
        }
        return (<Filters>
        <code>{getEventTypeFilter_1.extractEventTypeFilterFromRule(rule)}</code>&nbsp;&nbsp;
        {rule.query && <code>{rule.query}</code>}
      </Filters>);
    };
    DetailsBody.prototype.renderTrigger = function (trigger) {
        var rule = this.props.rule;
        if (!rule) {
            return null;
        }
        var status = trigger.label === 'critical' ? (<StatusWrapper>
          <icons_1.IconFire color="red300" size="sm"/> Critical
        </StatusWrapper>) : trigger.label === 'warning' ? (<StatusWrapper>
          <icons_1.IconWarning color="yellow300" size="sm"/> Warning
        </StatusWrapper>) : (<StatusWrapper>
          <icons_1.IconCheckmark color="green300" size="sm" isCircled/> Resolved
        </StatusWrapper>);
        var thresholdTypeText = rule.thresholdType === types_1.AlertRuleThresholdType.ABOVE ? locale_1.t('above') : locale_1.t('below');
        return (<TriggerCondition>
        {status}
        <TriggerText>{thresholdTypeText + " " + trigger.alertThreshold}</TriggerText>
      </TriggerCondition>);
    };
    DetailsBody.prototype.renderRuleDetails = function () {
        var _a, _b, _c;
        var rule = this.props.rule;
        if (rule === undefined) {
            return <placeholder_1.default height="200px"/>;
        }
        var criticalTrigger = rule === null || rule === void 0 ? void 0 : rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'critical';
        });
        var warningTrigger = rule === null || rule === void 0 ? void 0 : rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'warning';
        });
        var ownerId = (_a = rule.owner) === null || _a === void 0 ? void 0 : _a.split(':')[1];
        var teamActor = ownerId && { type: 'team', id: ownerId, name: '' };
        return (<React.Fragment>
        <SidebarGroup>
          <Heading>{locale_1.t('Metric')}</Heading>
          <RuleText>{this.getMetricText()}</RuleText>
        </SidebarGroup>

        <SidebarGroup>
          <Heading>{locale_1.t('Environment')}</Heading>
          <RuleText>{(_b = rule.environment) !== null && _b !== void 0 ? _b : 'All'}</RuleText>
        </SidebarGroup>

        <SidebarGroup>
          <Heading>{locale_1.t('Filters')}</Heading>
          {this.getFilter()}
        </SidebarGroup>

        <SidebarGroup>
          <Heading>{locale_1.t('Conditions')}</Heading>
          {criticalTrigger && this.renderTrigger(criticalTrigger)}
          {warningTrigger && this.renderTrigger(warningTrigger)}
        </SidebarGroup>

        <SidebarGroup>
          <Heading>{locale_1.t('Other Details')}</Heading>
          <keyValueTable_1.KeyValueTable>
            <keyValueTable_1.KeyValueTableRow keyName={locale_1.t('Team')} value={teamActor ? <actorAvatar_1.default actor={teamActor} size={24}/> : 'Unassigned'}/>

            {rule.createdBy && (<keyValueTable_1.KeyValueTableRow keyName={locale_1.t('Created By')} value={<CreatedBy>{(_c = rule.createdBy.name) !== null && _c !== void 0 ? _c : '-'}</CreatedBy>}/>)}

            {rule.dateModified && (<keyValueTable_1.KeyValueTableRow keyName={locale_1.t('Last Modified')} value={<timeSince_1.default date={rule.dateModified} suffix={locale_1.t('ago')}/>}/>)}
          </keyValueTable_1.KeyValueTable>
        </SidebarGroup>
      </React.Fragment>);
    };
    DetailsBody.prototype.renderMetricStatus = function () {
        var incidents = this.props.incidents;
        // get current status
        var activeIncident = incidents === null || incidents === void 0 ? void 0 : incidents.find(function (_a) {
            var dateClosed = _a.dateClosed;
            return !dateClosed;
        });
        var status = activeIncident ? activeIncident.status : types_2.IncidentStatus.CLOSED;
        var latestIncident = (incidents === null || incidents === void 0 ? void 0 : incidents.length) ? incidents[0] : null;
        // The date at which the alert was triggered or resolved
        var activityDate = activeIncident
            ? activeIncident.dateStarted
            : latestIncident
                ? latestIncident.dateClosed
                : null;
        return (<StatusContainer>
        <HeaderItem>
          <Heading noMargin>{locale_1.t('Current Status')}</Heading>
          <Status>
            <alertBadge_1.default status={status} hideText/>
            {activeIncident ? locale_1.t('Triggered') : locale_1.t('Resolved')}
            {activityDate ? <timeSince_1.default date={activityDate}/> : '-'}
          </Status>
        </HeaderItem>
      </StatusContainer>);
    };
    DetailsBody.prototype.renderLoading = function () {
        return (<Layout.Body>
        <Layout.Main>
          <placeholder_1.default height="38px"/>
          <ChartPanel>
            <panels_1.PanelBody withPadding>
              <placeholder_1.default height="200px"/>
            </panels_1.PanelBody>
          </ChartPanel>
        </Layout.Main>
        <Layout.Side>
          <placeholder_1.default height="200px"/>
        </Layout.Side>
      </Layout.Body>);
    };
    DetailsBody.prototype.render = function () {
        var _this = this;
        var _a = this.props, api = _a.api, rule = _a.rule, incidents = _a.incidents, location = _a.location, organization = _a.organization, timePeriod = _a.timePeriod, selectedIncident = _a.selectedIncident, handleZoom = _a.handleZoom, orgId = _a.params.orgId;
        if (!rule) {
            return this.renderLoading();
        }
        var query = rule.query, projectSlugs = rule.projects;
        var queryWithTypeFilter = (query + " " + getEventTypeFilter_1.extractEventTypeFilterFromRule(rule)).trim();
        return (<projects_1.default orgId={orgId} slugs={projectSlugs}>
        {function (_a) {
                var initiallyLoaded = _a.initiallyLoaded, projects = _a.projects;
                return initiallyLoaded ? (<React.Fragment>
              {selectedIncident &&
                        selectedIncident.alertRule.status === types_2.AlertRuleStatus.SNAPSHOT && (<StyledLayoutBody>
                    <StyledAlert type="warning" icon={<icons_1.IconInfo size="md"/>}>
                      {locale_1.t('Alert Rule settings have been updated since this alert was triggered.')}
                    </StyledAlert>
                  </StyledLayoutBody>)}
              <StyledLayoutBodyWrapper>
                <Layout.Main>
                  <HeaderContainer>
                    <HeaderGrid>
                      <HeaderItem>
                        <Heading noMargin>{locale_1.t('Display')}</Heading>
                        <ChartControls>
                          <dropdownControl_1.default label={timePeriod.display}>
                            {constants_1.TIME_OPTIONS.map(function (_a) {
                        var label = _a.label, value = _a.value;
                        return (<dropdownControl_1.DropdownItem key={value} eventKey={value} onSelect={_this.props.handleTimePeriodChange}>
                                {label}
                              </dropdownControl_1.DropdownItem>);
                    })}
                          </dropdownControl_1.default>
                        </ChartControls>
                      </HeaderItem>
                      {projects && projects.length && (<HeaderItem>
                          <Heading noMargin>{locale_1.t('Project')}</Heading>

                          <idBadge_1.default avatarSize={16} project={projects[0]}/>
                        </HeaderItem>)}
                      <HeaderItem>
                        <Heading noMargin>
                          {locale_1.t('Time Interval')}
                          <tooltip_1.default title={locale_1.t('The time window over which the metric is evaluated.')}>
                            <icons_1.IconInfo size="xs" color="gray200"/>
                          </tooltip_1.default>
                        </Heading>

                        <RuleText>{_this.getTimeWindow()}</RuleText>
                      </HeaderItem>
                    </HeaderGrid>
                  </HeaderContainer>

                  <metricChart_1.default api={api} rule={rule} incidents={incidents} timePeriod={timePeriod} selectedIncident={selectedIncident} organization={organization} projects={projects} interval={_this.getInterval()} filter={_this.getFilter()} query={queryWithTypeFilter} orgId={orgId} handleZoom={handleZoom}/>
                  <DetailWrapper>
                    <ActivityWrapper>
                      {(rule === null || rule === void 0 ? void 0 : rule.dataset) === types_1.Dataset.ERRORS && (<relatedIssues_1.default organization={organization} rule={rule} projects={(projects || []).filter(function (project) {
                            return rule.projects.includes(project.slug);
                        })} timePeriod={timePeriod}/>)}
                      {(rule === null || rule === void 0 ? void 0 : rule.dataset) === types_1.Dataset.TRANSACTIONS && (<relatedTransactions_1.default organization={organization} location={location} rule={rule} projects={(projects || []).filter(function (project) {
                            return rule.projects.includes(project.slug);
                        })} start={timePeriod.start} end={timePeriod.end} filter={getEventTypeFilter_1.extractEventTypeFilterFromRule(rule)}/>)}
                    </ActivityWrapper>
                  </DetailWrapper>
                </Layout.Main>
                <Layout.Side>
                  {_this.renderMetricStatus()}
                  <timeline_1.default api={api} organization={organization} rule={rule} incidents={incidents}/>
                  {_this.renderRuleDetails()}
                </Layout.Side>
              </StyledLayoutBodyWrapper>
            </React.Fragment>) : (<placeholder_1.default height="200px"/>);
            }}
      </projects_1.default>);
    };
    return DetailsBody;
}(React.Component));
exports.default = DetailsBody;
var SidebarGroup = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(3));
var DetailWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n\n  @media (max-width: ", ") {\n    flex-direction: column-reverse;\n  }\n"], ["\n  display: flex;\n  flex: 1;\n\n  @media (max-width: ", ") {\n    flex-direction: column-reverse;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var StatusWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  svg {\n    margin-right: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  svg {\n    margin-right: ", ";\n  }\n"])), space_1.default(0.5));
var HeaderContainer = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  height: 60px;\n  display: flex;\n  flex-direction: row;\n  align-content: flex-start;\n"], ["\n  height: 60px;\n  display: flex;\n  flex-direction: row;\n  align-content: flex-start;\n"])));
var HeaderGrid = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto auto auto;\n  align-items: stretch;\n  grid-gap: 60px;\n"], ["\n  display: grid;\n  grid-template-columns: auto auto auto;\n  align-items: stretch;\n  grid-gap: 60px;\n"])));
var HeaderItem = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n\n  > *:nth-child(2) {\n    flex: 1;\n    display: flex;\n    align-items: center;\n  }\n"], ["\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n\n  > *:nth-child(2) {\n    flex: 1;\n    display: flex;\n    align-items: center;\n  }\n"])));
var StyledLayoutBody = styled_1.default(Layout.Body)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  flex-grow: 0;\n  padding-bottom: 0 !important;\n  @media (min-width: ", ") {\n    grid-template-columns: auto;\n  }\n"], ["\n  flex-grow: 0;\n  padding-bottom: 0 !important;\n  @media (min-width: ", ") {\n    grid-template-columns: auto;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var StyledLayoutBodyWrapper = styled_1.default(Layout.Body)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  margin-bottom: -", ";\n"], ["\n  margin-bottom: -", ";\n"])), space_1.default(3));
var StyledAlert = styled_1.default(alert_1.default)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var ActivityWrapper = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n  width: 100%;\n"], ["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n  width: 100%;\n"])));
var Status = styled_1.default('div')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  display: grid;\n  grid-template-columns: auto auto auto;\n  grid-gap: ", ";\n  font-size: ", ";\n"], ["\n  position: relative;\n  display: grid;\n  grid-template-columns: auto auto auto;\n  grid-gap: ", ";\n  font-size: ", ";\n"])), space_1.default(0.5), function (p) { return p.theme.fontSizeLarge; });
var StatusContainer = styled_1.default('div')(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  height: 60px;\n  display: flex;\n  margin-bottom: ", ";\n"], ["\n  height: 60px;\n  display: flex;\n  margin-bottom: ", ";\n"])), space_1.default(1.5));
var Heading = styled_1.default(styles_1.SectionHeading)(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto auto;\n  justify-content: flex-start;\n  margin-top: ", ";\n  margin-bottom: ", ";\n  line-height: 1;\n  gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: auto auto;\n  justify-content: flex-start;\n  margin-top: ", ";\n  margin-bottom: ", ";\n  line-height: 1;\n  gap: ", ";\n"])), function (p) { return (p.noMargin ? 0 : space_1.default(2)); }, space_1.default(0.5), space_1.default(1));
var ChartControls = styled_1.default('div')(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n"], ["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n"])));
var ChartPanel = styled_1.default(panels_1.Panel)(templateObject_15 || (templateObject_15 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(2));
var RuleText = styled_1.default('div')(templateObject_16 || (templateObject_16 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var Filters = styled_1.default('span')(templateObject_17 || (templateObject_17 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  overflow-wrap: break-word;\n  font-size: ", ";\n  gap: ", ";\n"], ["\n  width: 100%;\n  overflow-wrap: break-word;\n  font-size: ", ";\n  gap: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space_1.default(1));
var TriggerCondition = styled_1.default('div')(templateObject_18 || (templateObject_18 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var TriggerText = styled_1.default('div')(templateObject_19 || (templateObject_19 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  white-space: nowrap;\n"], ["\n  margin-left: ", ";\n  white-space: nowrap;\n"])), space_1.default(0.5));
var CreatedBy = styled_1.default('div')(templateObject_20 || (templateObject_20 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis_1.default);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16, templateObject_17, templateObject_18, templateObject_19, templateObject_20;
//# sourceMappingURL=body.jsx.map