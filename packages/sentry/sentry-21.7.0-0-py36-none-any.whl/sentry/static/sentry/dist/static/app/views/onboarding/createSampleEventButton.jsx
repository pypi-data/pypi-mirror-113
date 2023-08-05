Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var locale_1 = require("app/locale");
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
var analytics_1 = require("app/utils/analytics");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var EVENT_POLL_RETRIES = 15;
var EVENT_POLL_INTERVAL = 1000;
function latestEventAvailable(api, groupID) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var retries, _a;
        return tslib_1.__generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    retries = 0;
                    _b.label = 1;
                case 1:
                    if (!true) return [3 /*break*/, 7];
                    if (retries > EVENT_POLL_RETRIES) {
                        return [2 /*return*/, { eventCreated: false, retries: retries - 1 }];
                    }
                    return [4 /*yield*/, new Promise(function (resolve) { return setTimeout(resolve, EVENT_POLL_INTERVAL); })];
                case 2:
                    _b.sent();
                    _b.label = 3;
                case 3:
                    _b.trys.push([3, 5, , 6]);
                    return [4 /*yield*/, api.requestPromise("/issues/" + groupID + "/events/latest/")];
                case 4:
                    _b.sent();
                    return [2 /*return*/, { eventCreated: true, retries: retries }];
                case 5:
                    _a = _b.sent();
                    ++retries;
                    return [3 /*break*/, 6];
                case 6: return [3 /*break*/, 1];
                case 7: return [2 /*return*/];
            }
        });
    });
}
var CreateSampleEventButton = /** @class */ (function (_super) {
    tslib_1.__extends(CreateSampleEventButton, _super);
    function CreateSampleEventButton() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            creating: false,
        };
        _this.createSampleGroup = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, organization, project, eventData, url, error_1, t0, _b, eventCreated, retries, t1, duration;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, project = _a.project;
                        if (!project) {
                            return [2 /*return*/];
                        }
                        advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.onboarding_view_sample_event', { platform: project.platform }, organization);
                        indicator_1.addLoadingMessage(locale_1.t('Processing sample event...'), {
                            duration: EVENT_POLL_RETRIES * EVENT_POLL_INTERVAL,
                        });
                        this.setState({ creating: true });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        url = "/projects/" + organization.slug + "/" + project.slug + "/create-sample/";
                        return [4 /*yield*/, api.requestPromise(url, { method: 'POST' })];
                    case 2:
                        eventData = _c.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _c.sent();
                        Sentry.withScope(function (scope) {
                            scope.setExtra('error', error_1);
                            Sentry.captureException(new Error('Failed to create sample event'));
                        });
                        this.setState({ creating: false });
                        indicator_1.clearIndicators();
                        indicator_1.addErrorMessage(locale_1.t('Failed to create a new sample event'));
                        return [2 /*return*/];
                    case 4:
                        t0 = performance.now();
                        return [4 /*yield*/, latestEventAvailable(api, eventData.groupID)];
                    case 5:
                        _b = _c.sent(), eventCreated = _b.eventCreated, retries = _b.retries;
                        t1 = performance.now();
                        indicator_1.clearIndicators();
                        this.setState({ creating: false });
                        duration = Math.ceil(t1 - t0);
                        this.recordAnalytics({ eventCreated: eventCreated, retries: retries, duration: duration });
                        if (!eventCreated) {
                            indicator_1.addErrorMessage(locale_1.t('Failed to load sample event'));
                            Sentry.withScope(function (scope) {
                                scope.setTag('groupID', eventData.groupID);
                                scope.setTag('platform', project.platform || '');
                                scope.setTag('interval', EVENT_POLL_INTERVAL.toString());
                                scope.setTag('retries', retries.toString());
                                scope.setTag('duration', duration.toString());
                                scope.setLevel(Sentry.Severity.Warning);
                                Sentry.captureMessage('Failed to load sample event');
                            });
                            return [2 /*return*/];
                        }
                        react_router_1.browserHistory.push("/organizations/" + organization.slug + "/issues/" + eventData.groupID + "/");
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    CreateSampleEventButton.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, source = _a.source;
        if (!project) {
            return;
        }
        analytics_1.trackAdhocEvent({
            eventKey: 'sample_event.button_viewed',
            org_id: organization.id,
            project_id: project.id,
            source: source,
        });
    };
    CreateSampleEventButton.prototype.recordAnalytics = function (_a) {
        var eventCreated = _a.eventCreated, retries = _a.retries, duration = _a.duration;
        var _b = this.props, organization = _b.organization, project = _b.project, source = _b.source;
        if (!project) {
            return;
        }
        var eventKey = "sample_event." + (eventCreated ? 'created' : 'failed');
        var eventName = "Sample Event " + (eventCreated ? 'Created' : 'Failed');
        analytics_1.trackAnalyticsEvent({
            eventKey: eventKey,
            eventName: eventName,
            organization_id: organization.id,
            project_id: project.id,
            platform: project.platform || '',
            interval: EVENT_POLL_INTERVAL,
            retries: retries,
            duration: duration,
            source: source,
        });
    };
    CreateSampleEventButton.prototype.render = function () {
        var _a = this.props, _api = _a.api, _organization = _a.organization, _project = _a.project, _source = _a.source, props = tslib_1.__rest(_a, ["api", "organization", "project", "source"]);
        var creating = this.state.creating;
        return (<button_1.default {...props} data-test-id="create-sample-event" disabled={props.disabled || creating} onClick={this.createSampleGroup}/>);
    };
    return CreateSampleEventButton;
}(React.Component));
exports.default = withApi_1.default(withOrganization_1.default(CreateSampleEventButton));
//# sourceMappingURL=createSampleEventButton.jsx.map