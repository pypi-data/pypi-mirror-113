Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var sentryAppComponents_1 = require("app/actionCreators/sentryAppComponents");
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var groupEventDetailsLoadingError_1 = tslib_1.__importDefault(require("app/components/errors/groupEventDetailsLoadingError"));
var eventEntries_1 = tslib_1.__importDefault(require("app/components/events/eventEntries"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var sidebar_1 = tslib_1.__importDefault(require("app/components/group/sidebar"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var mutedBox_1 = tslib_1.__importDefault(require("app/components/mutedBox"));
var reprocessedBox_1 = tslib_1.__importDefault(require("app/components/reprocessedBox"));
var resolutionBox_1 = tslib_1.__importDefault(require("app/components/resolutionBox"));
var suggestProjectCTA_1 = tslib_1.__importDefault(require("app/components/suggestProjectCTA"));
var analytics_1 = require("app/utils/analytics");
var fetchSentryAppInstallations_1 = tslib_1.__importDefault(require("app/utils/fetchSentryAppInstallations"));
var eventToolbar_1 = tslib_1.__importDefault(require("../eventToolbar"));
var reprocessingProgress_1 = tslib_1.__importDefault(require("../reprocessingProgress"));
var utils_1 = require("../utils");
var GroupEventDetails = /** @class */ (function (_super) {
    tslib_1.__extends(GroupEventDetails, _super);
    function GroupEventDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventNavLinks: '',
            releasesCompletion: null,
        };
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, project, organization, orgSlug, projSlug, projectId, releasesCompletionPromise, releasesCompletion;
            var _this = this;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, project = _a.project, organization = _a.organization;
                        orgSlug = organization.slug;
                        projSlug = project.slug;
                        projectId = project.id;
                        releasesCompletionPromise = api.requestPromise("/projects/" + orgSlug + "/" + projSlug + "/releases/completion/");
                        fetchSentryAppInstallations_1.default(api, orgSlug);
                        // TODO(marcos): Sometimes GlobalSelectionStore cannot pick a project.
                        if (projectId) {
                            sentryAppComponents_1.fetchSentryAppComponents(api, orgSlug, projectId);
                        }
                        else {
                            Sentry.withScope(function (scope) {
                                scope.setExtra('props', _this.props);
                                scope.setExtra('state', _this.state);
                                Sentry.captureMessage('Project ID was not set');
                            });
                        }
                        return [4 /*yield*/, releasesCompletionPromise];
                    case 1:
                        releasesCompletion = _b.sent();
                        this.setState({ releasesCompletion: releasesCompletion });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    GroupEventDetails.prototype.componentDidMount = function () {
        this.fetchData();
        // First Meaningful Paint for /organizations/:orgId/issues/:groupId/
        analytics_1.metric.measure({
            name: 'app.page.perf.issue-details',
            start: 'page-issue-details-start',
            data: {
                // start_type is set on 'page-issue-details-start'
                org_id: parseInt(this.props.organization.id, 10),
                group: this.props.organization.features.includes('enterprise-perf')
                    ? 'enterprise-perf'
                    : 'control',
                milestone: 'first-meaningful-paint',
                is_enterprise: this.props.organization.features
                    .includes('enterprise-orgs')
                    .toString(),
                is_outlier: this.props.organization.features
                    .includes('enterprise-orgs-outliers')
                    .toString(),
            },
        });
    };
    GroupEventDetails.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, environments = _a.environments, params = _a.params, location = _a.location, organization = _a.organization, project = _a.project;
        var environmentsHaveChanged = !isEqual_1.default(prevProps.environments, environments);
        // If environments are being actively changed and will no longer contain the
        // current event's environment, redirect to latest
        if (environmentsHaveChanged &&
            prevProps.event &&
            params.eventId &&
            !['latest', 'oldest'].includes(params.eventId)) {
            var shouldRedirect = environments.length > 0 &&
                !environments.find(function (env) { return env.name === utils_1.getEventEnvironment(prevProps.event); });
            if (shouldRedirect) {
                react_router_1.browserHistory.replace({
                    pathname: "/organizations/" + params.orgId + "/issues/" + params.groupId + "/",
                    query: location.query,
                });
                return;
            }
        }
        if (prevProps.organization.slug !== organization.slug ||
            prevProps.project.slug !== project.slug) {
            this.fetchData();
        }
    };
    GroupEventDetails.prototype.componentWillUnmount = function () {
        var api = this.props.api;
        api.clear();
    };
    Object.defineProperty(GroupEventDetails.prototype, "showExampleCommit", {
        get: function () {
            var project = this.props.project;
            var releasesCompletion = this.state.releasesCompletion;
            return ((project === null || project === void 0 ? void 0 : project.isMember) &&
                (project === null || project === void 0 ? void 0 : project.firstEvent) &&
                (releasesCompletion === null || releasesCompletion === void 0 ? void 0 : releasesCompletion.some(function (_a) {
                    var step = _a.step, complete = _a.complete;
                    return step === 'commit' && !complete;
                })));
        },
        enumerable: false,
        configurable: true
    });
    GroupEventDetails.prototype.renderContent = function (eventWithMeta) {
        var _a = this.props, group = _a.group, project = _a.project, organization = _a.organization, environments = _a.environments, location = _a.location, loadingEvent = _a.loadingEvent, onRetry = _a.onRetry, eventError = _a.eventError;
        if (loadingEvent) {
            return <loadingIndicator_1.default />;
        }
        if (eventError) {
            return (<groupEventDetailsLoadingError_1.default environments={environments} onRetry={onRetry}/>);
        }
        return (<eventEntries_1.default group={group} event={eventWithMeta} organization={organization} project={project} location={location} showExampleCommit={this.showExampleCommit}/>);
    };
    GroupEventDetails.prototype.renderReprocessedBox = function (reprocessStatus, mostRecentActivity) {
        if (reprocessStatus !== utils_1.ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT &&
            reprocessStatus !== utils_1.ReprocessingStatus.REPROCESSED_AND_HAS_EVENT) {
            return null;
        }
        var _a = this.props, group = _a.group, organization = _a.organization;
        var count = group.count, groupId = group.id;
        var groupCount = Number(count);
        return (<reprocessedBox_1.default reprocessActivity={mostRecentActivity} groupCount={groupCount} groupId={groupId} orgSlug={organization.slug}/>);
    };
    GroupEventDetails.prototype.render = function () {
        var _a;
        var _b = this.props, className = _b.className, group = _b.group, project = _b.project, organization = _b.organization, environments = _b.environments, location = _b.location, event = _b.event, groupReprocessingStatus = _b.groupReprocessingStatus;
        var eventWithMeta = metaProxy_1.withMeta(event);
        // Reprocessing
        var hasReprocessingV2Feature = (_a = organization.features) === null || _a === void 0 ? void 0 : _a.includes('reprocessing-v2');
        var activities = group.activity;
        var mostRecentActivity = utils_1.getGroupMostRecentActivity(activities);
        return (<div className={className}>
        {event && (<errorBoundary_1.default customComponent={null}>
            <suggestProjectCTA_1.default event={event} organization={organization}/>
          </errorBoundary_1.default>)}
        <div className="event-details-container">
          {hasReprocessingV2Feature &&
                groupReprocessingStatus === utils_1.ReprocessingStatus.REPROCESSING ? (<reprocessingProgress_1.default totalEvents={mostRecentActivity.data.eventCount} pendingEvents={group.statusDetails
                    .pendingEvents}/>) : (<react_1.Fragment>
              <div className="primary">
                {eventWithMeta && (<eventToolbar_1.default group={group} event={eventWithMeta} organization={organization} location={location} project={project}/>)}
                {group.status === 'ignored' && (<mutedBox_1.default statusDetails={group.statusDetails}/>)}
                {group.status === 'resolved' && (<resolutionBox_1.default statusDetails={group.statusDetails} projectId={project.id}/>)}
                {this.renderReprocessedBox(groupReprocessingStatus, mostRecentActivity)}
                {this.renderContent(eventWithMeta)}
              </div>
              <div className="secondary">
                <sidebar_1.default organization={organization} project={project} group={group} event={eventWithMeta} environments={environments}/>
              </div>
            </react_1.Fragment>)}
        </div>
      </div>);
    };
    return GroupEventDetails;
}(react_1.Component));
exports.default = styled_1.default(GroupEventDetails)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n"])));
var templateObject_1;
//# sourceMappingURL=groupEventDetails.jsx.map