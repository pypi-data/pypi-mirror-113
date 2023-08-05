Object.defineProperty(exports, "__esModule", { value: true });
exports.makeRuleDetailsQuery = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var memoize_1 = tslib_1.__importDefault(require("lodash/memoize"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var actorAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/actorAvatar"));
var duration_1 = tslib_1.__importDefault(require("app/components/duration"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var locale_1 = require("app/locale");
var teamStore_1 = tslib_1.__importDefault(require("app/stores/teamStore"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var dates_1 = require("app/utils/dates");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var details_1 = require("app/views/alerts/details");
var constants_1 = require("../rules/details/constants");
var types_1 = require("../types");
var utils_1 = require("../utils");
/**
 * Retrieve the start/end for showing the graph of the metric
 * Will show at least 150 and no more than 10,000 data points
 */
var makeRuleDetailsQuery = function (incident) {
    var timeWindow = incident.alertRule.timeWindow;
    var timeWindowMillis = timeWindow * 60 * 1000;
    var minRange = timeWindowMillis * constants_1.API_INTERVAL_POINTS_MIN;
    var maxRange = timeWindowMillis * constants_1.API_INTERVAL_POINTS_LIMIT;
    var now = moment_1.default.utc();
    var startDate = moment_1.default.utc(incident.dateStarted);
    // make a copy of now since we will modify endDate and use now for comparing
    var endDate = incident.dateClosed ? moment_1.default.utc(incident.dateClosed) : moment_1.default(now);
    var incidentRange = Math.max(endDate.diff(startDate), 3 * timeWindowMillis);
    var range = Math.min(maxRange, Math.max(minRange, incidentRange));
    var halfRange = moment_1.default.duration(range / 2);
    return {
        start: dates_1.getUtcDateString(startDate.subtract(halfRange)),
        end: dates_1.getUtcDateString(moment_1.default.min(endDate.add(halfRange), now)),
    };
};
exports.makeRuleDetailsQuery = makeRuleDetailsQuery;
var AlertListRow = /** @class */ (function (_super) {
    tslib_1.__extends(AlertListRow, _super);
    function AlertListRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Memoized function to find a project from a list of projects
         */
        _this.getProject = memoize_1.default(function (slug, projects) {
            return projects.find(function (project) { return project.slug === slug; });
        });
        return _this;
    }
    Object.defineProperty(AlertListRow.prototype, "metricPreset", {
        get: function () {
            var incident = this.props.incident;
            return incident ? utils_1.getIncidentMetricPreset(incident) : undefined;
        },
        enumerable: false,
        configurable: true
    });
    AlertListRow.prototype.render = function () {
        var _a, _b, _c;
        var _d = this.props, incident = _d.incident, orgId = _d.orgId, projectsLoaded = _d.projectsLoaded, projects = _d.projects, organization = _d.organization;
        var slug = incident.projects[0];
        var started = moment_1.default(incident.dateStarted);
        var duration = moment_1.default
            .duration(moment_1.default(incident.dateClosed || new Date()).diff(started))
            .as('seconds');
        var hasRedesign = !utils_1.isIssueAlert(incident.alertRule) &&
            organization.features.includes('alert-details-redesign');
        var alertLink = hasRedesign
            ? {
                pathname: details_1.alertDetailsLink(organization, incident),
                query: { alert: incident.identifier },
            }
            : {
                pathname: "/organizations/" + orgId + "/alerts/" + incident.identifier + "/",
            };
        var ownerId = (_a = incident.alertRule.owner) === null || _a === void 0 ? void 0 : _a.split(':')[1];
        var teamName = '';
        if (ownerId) {
            teamName = (_c = (_b = teamStore_1.default.getById(ownerId)) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : '';
        }
        var teamActor = ownerId
            ? { type: 'team', id: ownerId, name: teamName }
            : null;
        return (<errorBoundary_1.default>
        <Title>
          <link_1.default to={alertLink}>{incident.title}</link_1.default>
        </Title>

        <NoWrap>
          {getDynamicText_1.default({
                value: <timeSince_1.default date={incident.dateStarted} extraShort/>,
                fixed: '1w ago',
            })}
        </NoWrap>
        <NoWrap>
          {incident.status === types_1.IncidentStatus.CLOSED ? (<duration_1.default seconds={getDynamicText_1.default({ value: duration, fixed: 1200 })}/>) : (<tag_1.default type="warning">{locale_1.t('Still Active')}</tag_1.default>)}
        </NoWrap>

        <ProjectBadge avatarSize={18} project={!projectsLoaded ? { slug: slug } : this.getProject(slug, projects)}/>
        <div>#{incident.id}</div>

        <FlexCenter>
          {teamActor ? (<react_1.Fragment>
              <StyledActorAvatar actor={teamActor} size={24} hasTooltip={false}/>{' '}
              <TeamWrapper>{teamActor.name}</TeamWrapper>
            </react_1.Fragment>) : ('-')}
        </FlexCenter>
      </errorBoundary_1.default>);
    };
    return AlertListRow;
}(react_1.Component));
var Title = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", "\n  min-width: 130px;\n"], ["\n  ", "\n  min-width: 130px;\n"])), overflowEllipsis_1.default);
var NoWrap = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
var ProjectBadge = styled_1.default(idBadge_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  flex-shrink: 0;\n"], ["\n  flex-shrink: 0;\n"])));
var FlexCenter = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  ", "\n  display: flex;\n  align-items: center;\n"], ["\n  ", "\n  display: flex;\n  align-items: center;\n"])), overflowEllipsis_1.default);
var TeamWrapper = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis_1.default);
var StyledActorAvatar = styled_1.default(actorAvatar_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
exports.default = AlertListRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=row.jsx.map