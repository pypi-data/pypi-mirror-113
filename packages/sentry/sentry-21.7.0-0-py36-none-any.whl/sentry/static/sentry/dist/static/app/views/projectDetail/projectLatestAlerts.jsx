Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var styles_1 = require("app/components/charts/styles");
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("../alerts/types");
var missingAlertsButtons_1 = tslib_1.__importDefault(require("./missingFeatureButtons/missingAlertsButtons"));
var styles_2 = require("./styles");
var utils_1 = require("./utils");
var PLACEHOLDER_AND_EMPTY_HEIGHT = '172px';
var ProjectLatestAlerts = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectLatestAlerts, _super);
    function ProjectLatestAlerts() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderAlertRow = function (alert) {
            var organization = _this.props.organization;
            var status = alert.status, id = alert.id, identifier = alert.identifier, title = alert.title, dateClosed = alert.dateClosed, dateStarted = alert.dateStarted;
            var isResolved = status === types_1.IncidentStatus.CLOSED;
            var isWarning = status === types_1.IncidentStatus.WARNING;
            var Icon = isResolved ? icons_1.IconCheckmark : isWarning ? icons_1.IconWarning : icons_1.IconFire;
            var statusProps = { isResolved: isResolved, isWarning: isWarning };
            return (<AlertRowLink to={"/organizations/" + organization.slug + "/alerts/" + identifier + "/"} key={id}>
        <AlertBadge {...statusProps} icon={Icon}>
          <AlertIconWrapper>
            <Icon color="white"/>
          </AlertIconWrapper>
        </AlertBadge>
        <AlertDetails>
          <AlertTitle>{title}</AlertTitle>
          <AlertDate {...statusProps}>
            {isResolved
                    ? locale_1.tct('Resolved [date]', {
                        date: dateClosed ? <timeSince_1.default date={dateClosed}/> : null,
                    })
                    : locale_1.tct('Triggered [date]', { date: <timeSince_1.default date={dateStarted}/> })}
          </AlertDate>
        </AlertDetails>
      </AlertRowLink>);
        };
        return _this;
    }
    ProjectLatestAlerts.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        var _a = this.props, location = _a.location, isProjectStabilized = _a.isProjectStabilized;
        // TODO(project-detail): we temporarily removed refetching based on timeselector
        if (this.state !== nextState ||
            utils_1.didProjectOrEnvironmentChange(location, nextProps.location) ||
            isProjectStabilized !== nextProps.isProjectStabilized) {
            return true;
        }
        return false;
    };
    ProjectLatestAlerts.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, location = _a.location, isProjectStabilized = _a.isProjectStabilized;
        if (utils_1.didProjectOrEnvironmentChange(prevProps.location, location) ||
            prevProps.isProjectStabilized !== isProjectStabilized) {
            this.remountComponent();
        }
    };
    ProjectLatestAlerts.prototype.getEndpoints = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, isProjectStabilized = _a.isProjectStabilized;
        if (!isProjectStabilized) {
            return [];
        }
        var query = tslib_1.__assign(tslib_1.__assign({}, pick_1.default(location.query, Object.values(globalSelectionHeader_1.URL_PARAM))), { per_page: 3 });
        // we are listing 3 alerts total, first unresolved and then we fill with resolved
        return [
            [
                'unresolvedAlerts',
                "/organizations/" + organization.slug + "/incidents/",
                { query: tslib_1.__assign(tslib_1.__assign({}, query), { status: 'open' }) },
            ],
            [
                'resolvedAlerts',
                "/organizations/" + organization.slug + "/incidents/",
                { query: tslib_1.__assign(tslib_1.__assign({}, query), { status: 'closed' }) },
            ],
        ];
    };
    /**
     * If our alerts are empty, determine if we've configured alert rules (empty message differs then)
     */
    ProjectLatestAlerts.prototype.onLoadAllEndpointsSuccess = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, unresolvedAlerts, resolvedAlerts, _b, location, organization, isProjectStabilized, alertRules;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.state, unresolvedAlerts = _a.unresolvedAlerts, resolvedAlerts = _a.resolvedAlerts;
                        _b = this.props, location = _b.location, organization = _b.organization, isProjectStabilized = _b.isProjectStabilized;
                        if (!isProjectStabilized) {
                            return [2 /*return*/];
                        }
                        if (tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read((unresolvedAlerts !== null && unresolvedAlerts !== void 0 ? unresolvedAlerts : []))), tslib_1.__read((resolvedAlerts !== null && resolvedAlerts !== void 0 ? resolvedAlerts : []))).length !== 0) {
                            this.setState({ hasAlertRule: true });
                            return [2 /*return*/];
                        }
                        this.setState({ loading: true });
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + organization.slug + "/alert-rules/", {
                                method: 'GET',
                                query: tslib_1.__assign(tslib_1.__assign({}, pick_1.default(location.query, tslib_1.__spreadArray([], tslib_1.__read(Object.values(globalSelectionHeader_1.URL_PARAM))))), { per_page: 1 }),
                            })];
                    case 1:
                        alertRules = _c.sent();
                        this.setState({ hasAlertRule: alertRules.length > 0, loading: false });
                        return [2 /*return*/];
                }
            });
        });
    };
    Object.defineProperty(ProjectLatestAlerts.prototype, "alertsLink", {
        get: function () {
            var organization = this.props.organization;
            // as this is a link to latest alerts, we want to only preserve project and environment
            return {
                pathname: "/organizations/" + organization.slug + "/alerts/",
                query: {
                    statsPeriod: undefined,
                    start: undefined,
                    end: undefined,
                    utc: undefined,
                },
            };
        },
        enumerable: false,
        configurable: true
    });
    ProjectLatestAlerts.prototype.renderInnerBody = function () {
        var _a = this.props, organization = _a.organization, projectSlug = _a.projectSlug, isProjectStabilized = _a.isProjectStabilized;
        var _b = this.state, loading = _b.loading, unresolvedAlerts = _b.unresolvedAlerts, resolvedAlerts = _b.resolvedAlerts, hasAlertRule = _b.hasAlertRule;
        var alertsUnresolvedAndResolved = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read((unresolvedAlerts !== null && unresolvedAlerts !== void 0 ? unresolvedAlerts : []))), tslib_1.__read((resolvedAlerts !== null && resolvedAlerts !== void 0 ? resolvedAlerts : [])));
        var checkingForAlertRules = alertsUnresolvedAndResolved.length === 0 && hasAlertRule === undefined;
        var showLoadingIndicator = loading || checkingForAlertRules || !isProjectStabilized;
        if (showLoadingIndicator) {
            return <placeholder_1.default height={PLACEHOLDER_AND_EMPTY_HEIGHT}/>;
        }
        if (!hasAlertRule) {
            return (<missingAlertsButtons_1.default organization={organization} projectSlug={projectSlug}/>);
        }
        if (alertsUnresolvedAndResolved.length === 0) {
            return (<StyledEmptyStateWarning small>{locale_1.t('No alerts found')}</StyledEmptyStateWarning>);
        }
        return alertsUnresolvedAndResolved.slice(0, 3).map(this.renderAlertRow);
    };
    ProjectLatestAlerts.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectLatestAlerts.prototype.renderBody = function () {
        return (<styles_2.SidebarSection>
        <styles_2.SectionHeadingWrapper>
          <styles_1.SectionHeading>{locale_1.t('Latest Alerts')}</styles_1.SectionHeading>
          <styles_2.SectionHeadingLink to={this.alertsLink}>
            <icons_1.IconOpen />
          </styles_2.SectionHeadingLink>
        </styles_2.SectionHeadingWrapper>

        <div>{this.renderInnerBody()}</div>
      </styles_2.SidebarSection>);
    };
    return ProjectLatestAlerts;
}(asyncComponent_1.default));
var AlertRowLink = styled_1.default(link_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: 40px;\n  margin-bottom: ", ";\n  margin-left: ", ";\n  &,\n  &:hover,\n  &:focus {\n    color: inherit;\n  }\n  &:first-child {\n    margin-top: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  height: 40px;\n  margin-bottom: ", ";\n  margin-left: ", ";\n  &,\n  &:hover,\n  &:focus {\n    color: inherit;\n  }\n  &:first-child {\n    margin-top: ", ";\n  }\n"])), space_1.default(3), space_1.default(0.5), space_1.default(1));
var getStatusColor = function (_a) {
    var theme = _a.theme, isResolved = _a.isResolved, isWarning = _a.isWarning;
    return isResolved ? theme.green300 : isWarning ? theme.yellow300 : theme.red300;
};
var AlertBadge = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-shrink: 0;\n  /* icon warning needs to be treated differently to look visually centered */\n  line-height: ", ";\n\n  &:before {\n    content: '';\n    width: 30px;\n    height: 30px;\n    border-radius: ", ";\n    background-color: ", ";\n    transform: rotate(45deg);\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-shrink: 0;\n  /* icon warning needs to be treated differently to look visually centered */\n  line-height: ", ";\n\n  &:before {\n    content: '';\n    width: 30px;\n    height: 30px;\n    border-radius: ", ";\n    background-color: ", ";\n    transform: rotate(45deg);\n  }\n"])), function (p) { return (p.icon === icons_1.IconWarning ? undefined : 1); }, function (p) { return p.theme.borderRadius; }, function (p) { return getStatusColor(p); });
var AlertIconWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n"], ["\n  position: absolute;\n"])));
var AlertDetails = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin-left: ", ";\n  ", "\n"], ["\n  font-size: ", ";\n  margin-left: ", ";\n  ", "\n"])), function (p) { return p.theme.fontSizeMedium; }, space_1.default(2), overflowEllipsis_1.default);
var AlertTitle = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-weight: 400;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  font-weight: 400;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])));
var AlertDate = styled_1.default('span')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return getStatusColor(p); });
var StyledEmptyStateWarning = styled_1.default(emptyStateWarning_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  height: ", ";\n  justify-content: center;\n"], ["\n  height: ", ";\n  justify-content: center;\n"])), PLACEHOLDER_AND_EMPTY_HEIGHT);
exports.default = ProjectLatestAlerts;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=projectLatestAlerts.jsx.map