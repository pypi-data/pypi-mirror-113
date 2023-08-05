Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var memoize_1 = tslib_1.__importDefault(require("lodash/memoize"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var menuItemActionLink_1 = tslib_1.__importDefault(require("app/components/actions/menuItemActionLink"));
var actorAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/actorAvatar"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var dropdownLink_1 = tslib_1.__importDefault(require("app/components/dropdownLink"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var types_1 = require("app/views/alerts/incidentRules/types");
var alertBadge_1 = tslib_1.__importDefault(require("../alertBadge"));
var types_2 = require("../types");
var utils_1 = require("../utils");
var RuleListRow = /** @class */ (function (_super) {
    tslib_1.__extends(RuleListRow, _super);
    function RuleListRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Memoized function to find a project from a list of projects
         */
        _this.getProject = memoize_1.default(function (slug, projects) {
            return projects.find(function (project) { return project.slug === slug; });
        });
        return _this;
    }
    RuleListRow.prototype.activeIncident = function () {
        var _a;
        var rule = this.props.rule;
        return (((_a = rule.latestIncident) === null || _a === void 0 ? void 0 : _a.status) !== undefined &&
            [types_2.IncidentStatus.CRITICAL, types_2.IncidentStatus.WARNING].includes(rule.latestIncident.status));
    };
    RuleListRow.prototype.renderLastIncidentDate = function () {
        var rule = this.props.rule;
        if (utils_1.isIssueAlert(rule)) {
            return null;
        }
        if (!rule.latestIncident) {
            return '-';
        }
        if (this.activeIncident()) {
            return (<div>
          {locale_1.t('Triggered ')}
          <timeSince_1.default date={rule.latestIncident.dateCreated}/>
        </div>);
        }
        return (<div>
        {locale_1.t('Resolved ')}
        <timeSince_1.default date={rule.latestIncident.dateClosed}/>
      </div>);
    };
    RuleListRow.prototype.renderAlertRuleStatus = function () {
        var _a, _b;
        var rule = this.props.rule;
        if (utils_1.isIssueAlert(rule)) {
            return null;
        }
        var activeIncident = this.activeIncident();
        var criticalTrigger = rule === null || rule === void 0 ? void 0 : rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'critical';
        });
        var warningTrigger = rule === null || rule === void 0 ? void 0 : rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'warning';
        });
        var trigger = activeIncident && ((_a = rule.latestIncident) === null || _a === void 0 ? void 0 : _a.status) === types_2.IncidentStatus.CRITICAL
            ? criticalTrigger
            : warningTrigger !== null && warningTrigger !== void 0 ? warningTrigger : criticalTrigger;
        var iconColor = 'green300';
        if (activeIncident) {
            iconColor =
                (trigger === null || trigger === void 0 ? void 0 : trigger.label) === 'critical'
                    ? 'red300'
                    : (trigger === null || trigger === void 0 ? void 0 : trigger.label) === 'warning'
                        ? 'yellow300'
                        : 'green300';
        }
        var thresholdTypeText = activeIncident && rule.thresholdType === types_1.AlertRuleThresholdType.ABOVE
            ? locale_1.t('Above')
            : locale_1.t('Below');
        return (<FlexCenter>
        <icons_1.IconArrow color={iconColor} direction={activeIncident && rule.thresholdType === types_1.AlertRuleThresholdType.ABOVE
                ? 'up'
                : 'down'}/>
        <TriggerText>{thresholdTypeText + " " + ((_b = trigger === null || trigger === void 0 ? void 0 : trigger.alertThreshold) === null || _b === void 0 ? void 0 : _b.toLocaleString())}</TriggerText>
      </FlexCenter>);
    };
    RuleListRow.prototype.render = function () {
        var _a;
        var _b, _c, _d, _e, _f, _g;
        var _h = this.props, rule = _h.rule, projectsLoaded = _h.projectsLoaded, projects = _h.projects, organization = _h.organization, orgId = _h.orgId, onDelete = _h.onDelete, userTeams = _h.userTeams;
        var slug = rule.projects[0];
        var editLink = "/organizations/" + orgId + "/alerts/" + (utils_1.isIssueAlert(rule) ? 'rules' : 'metric-rules') + "/" + slug + "/" + rule.id + "/";
        var hasRedesign = !utils_1.isIssueAlert(rule) && organization.features.includes('alert-details-redesign');
        var detailsLink = "/organizations/" + orgId + "/alerts/rules/details/" + rule.id + "/";
        var ownerId = (_b = rule.owner) === null || _b === void 0 ? void 0 : _b.split(':')[1];
        var teamActor = ownerId
            ? { type: 'team', id: ownerId, name: '' }
            : null;
        var canEdit = ownerId ? userTeams.has(ownerId) : true;
        var hasAlertList = organization.features.includes('alert-details-redesign');
        var alertLink = utils_1.isIssueAlert(rule) ? (rule.name) : (<TitleLink to={hasRedesign ? detailsLink : editLink}>{rule.name}</TitleLink>);
        var IssueStatusText = (_a = {},
            _a[types_2.IncidentStatus.CRITICAL] = locale_1.t('Critical'),
            _a[types_2.IncidentStatus.WARNING] = locale_1.t('Warning'),
            _a[types_2.IncidentStatus.CLOSED] = locale_1.t('Resolved'),
            _a[types_2.IncidentStatus.OPENED] = locale_1.t('Resolved'),
            _a);
        return (<errorBoundary_1.default>
        {!hasAlertList ? (<React.Fragment>
            <RuleType>{utils_1.isIssueAlert(rule) ? locale_1.t('Issue') : locale_1.t('Metric')}</RuleType>
            <Title>{alertLink}</Title>
          </React.Fragment>) : (<React.Fragment>
            <AlertNameWrapper isIncident={utils_1.isIssueAlert(rule)}>
              <FlexCenter>
                <tooltip_1.default title={utils_1.isIssueAlert(rule)
                    ? locale_1.t('Issue Alert')
                    : locale_1.tct('Metric Alert Status: [status]', {
                        status: IssueStatusText[(_d = (_c = rule === null || rule === void 0 ? void 0 : rule.latestIncident) === null || _c === void 0 ? void 0 : _c.status) !== null && _d !== void 0 ? _d : types_2.IncidentStatus.CLOSED],
                    })}>
                  <alertBadge_1.default status={(_e = rule === null || rule === void 0 ? void 0 : rule.latestIncident) === null || _e === void 0 ? void 0 : _e.status} isIssue={utils_1.isIssueAlert(rule)} hideText/>
                </tooltip_1.default>
              </FlexCenter>
              <AlertNameAndStatus>
                <AlertName>{alertLink}</AlertName>
                {!utils_1.isIssueAlert(rule) && this.renderLastIncidentDate()}
              </AlertNameAndStatus>
            </AlertNameWrapper>
            <FlexCenter>{this.renderAlertRuleStatus()}</FlexCenter>
          </React.Fragment>)}

        <FlexCenter>
          <ProjectBadgeContainer>
            <ProjectBadge avatarSize={18} project={!projectsLoaded ? { slug: slug } : this.getProject(slug, projects)}/>
          </ProjectBadgeContainer>
        </FlexCenter>

        <FlexCenter>
          {teamActor ? <actorAvatar_1.default actor={teamActor} size={24}/> : '-'}
        </FlexCenter>

        {!hasAlertList && <CreatedBy>{(_g = (_f = rule === null || rule === void 0 ? void 0 : rule.createdBy) === null || _f === void 0 ? void 0 : _f.name) !== null && _g !== void 0 ? _g : '-'}</CreatedBy>}
        <FlexCenter>
          <dateTime_1.default date={getDynamicText_1.default({
                value: rule.dateCreated,
                fixed: new Date('2021-04-20'),
            })} format="ll"/>
        </FlexCenter>
        <ActionsRow>
          <access_1.default access={['alerts:write']}>
            {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<React.Fragment>
                <StyledDropdownLink>
                  <dropdownLink_1.default anchorRight caret={false} title={<button_1.default tooltipProps={{
                            containerDisplayMode: 'flex',
                        }} size="small" type="button" aria-label={locale_1.t('Show more')} icon={<icons_1.IconEllipsis size="xs"/>}/>}>
                    <li>
                      <link_1.default to={editLink}>{locale_1.t('Edit')}</link_1.default>
                    </li>
                    <confirm_1.default disabled={!hasAccess || !canEdit} message={locale_1.tct("Are you sure you want to delete [name]? You won't be able to view the history of this alert once it's deleted.", {
                        name: rule.name,
                    })} header={locale_1.t('Delete Alert Rule?')} priority="danger" confirmText={locale_1.t('Delete Rule')} onConfirm={function () { return onDelete(slug, rule); }}>
                      <menuItemActionLink_1.default title={locale_1.t('Delete')}>
                        {locale_1.t('Delete')}
                      </menuItemActionLink_1.default>
                    </confirm_1.default>
                  </dropdownLink_1.default>
                </StyledDropdownLink>

                {/* Small screen actions */}
                <StyledButtonBar gap={1}>
                  <confirm_1.default disabled={!hasAccess || !canEdit} message={locale_1.tct("Are you sure you want to delete [name]? You won't be able to view the history of this alert once it's deleted.", {
                        name: rule.name,
                    })} header={locale_1.t('Delete Alert Rule?')} priority="danger" confirmText={locale_1.t('Delete Rule')} onConfirm={function () { return onDelete(slug, rule); }}>
                    <button_1.default type="button" icon={<icons_1.IconDelete />} size="small" title={locale_1.t('Delete')}/>
                  </confirm_1.default>
                  <tooltip_1.default title={locale_1.t('Edit')}>
                    <button_1.default size="small" type="button" icon={<icons_1.IconSettings />} to={editLink}/>
                  </tooltip_1.default>
                </StyledButtonBar>
              </React.Fragment>);
            }}
          </access_1.default>
        </ActionsRow>
      </errorBoundary_1.default>);
    };
    return RuleListRow;
}(React.Component));
var columnCss = react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  height: 100%;\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  height: 100%;\n"])));
var RuleType = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  font-weight: 400;\n  color: ", ";\n  text-transform: uppercase;\n  ", "\n"], ["\n  font-size: ", ";\n  font-weight: 400;\n  color: ", ";\n  text-transform: uppercase;\n  ", "\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; }, columnCss);
var Title = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), columnCss);
var TitleLink = styled_1.default(link_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis_1.default);
var CreatedBy = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  ", "\n  ", "\n"], ["\n  ", "\n  ", "\n"])), overflowEllipsis_1.default, columnCss);
var FlexCenter = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var AlertNameWrapper = styled_1.default(FlexCenter)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) { return p.isIncident && "padding: " + space_1.default(3) + " " + space_1.default(2) + "; line-height: 2.4;"; });
var AlertNameAndStatus = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  ", "\n  margin-left: ", ";\n  line-height: 1.35;\n"], ["\n  ", "\n  margin-left: ", ";\n  line-height: 1.35;\n"])), overflowEllipsis_1.default, space_1.default(1.5));
var AlertName = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  ", "\n  font-size: ", ";\n\n  @media (max-width: ", ") {\n    max-width: 300px;\n  }\n  @media (max-width: ", ") {\n    max-width: 165px;\n  }\n  @media (max-width: ", ") {\n    max-width: 100px;\n  }\n"], ["\n  ", "\n  font-size: ", ";\n\n  @media (max-width: ", ") {\n    max-width: 300px;\n  }\n  @media (max-width: ", ") {\n    max-width: 165px;\n  }\n  @media (max-width: ", ") {\n    max-width: 100px;\n  }\n"])), overflowEllipsis_1.default, function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.theme.breakpoints[3]; }, function (p) { return p.theme.breakpoints[2]; }, function (p) { return p.theme.breakpoints[1]; });
var ProjectBadgeContainer = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n"], ["\n  width: 100%;\n"])));
var ProjectBadge = styled_1.default(idBadge_1.default)(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  flex-shrink: 0;\n"], ["\n  flex-shrink: 0;\n"])));
var TriggerText = styled_1.default('div')(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  white-space: nowrap;\n"], ["\n  margin-left: ", ";\n  white-space: nowrap;\n"])), space_1.default(1));
var StyledButtonBar = styled_1.default(buttonBar_1.default)(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  display: none;\n  justify-content: flex-start;\n  align-items: center;\n\n  @media (max-width: ", ") {\n    display: flex;\n  }\n"], ["\n  display: none;\n  justify-content: flex-start;\n  align-items: center;\n\n  @media (max-width: ", ") {\n    display: flex;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var StyledDropdownLink = styled_1.default('div')(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject(["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n  }\n"], ["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var ActionsRow = styled_1.default(FlexCenter)(templateObject_15 || (templateObject_15 = tslib_1.__makeTemplateObject(["\n  justify-content: center;\n  padding: ", ";\n"], ["\n  justify-content: center;\n  padding: ", ";\n"])), space_1.default(1));
exports.default = RuleListRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15;
//# sourceMappingURL=row.jsx.map