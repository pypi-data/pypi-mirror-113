Object.defineProperty(exports, "__esModule", { value: true });
exports.TransactionsListOption = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var release_1 = require("app/actionCreators/release");
var api_1 = require("app/api");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var transactionsList_1 = tslib_1.__importDefault(require("app/components/discover/transactionsList"));
var thirds_1 = require("app/components/layouts/thirds");
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var pageTimeRangeSelector_1 = tslib_1.__importDefault(require("app/components/organizations/timeRangeSelector/pageTimeRangeSelector"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var dates_1 = require("app/utils/dates");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var fields_1 = require("app/utils/discover/fields");
var formatters_1 = require("app/utils/formatters");
var queryString_1 = require("app/utils/queryString");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var charts_1 = require("app/views/performance/transactionSummary/charts");
var utils_1 = require("app/views/performance/transactionSummary/utils");
var types_1 = require("app/views/performance/trends/types");
var utils_2 = require("../../utils");
var __1 = require("..");
var chart_1 = tslib_1.__importDefault(require("./chart/"));
var releaseChartControls_1 = require("./chart/releaseChartControls");
var commitAuthorBreakdown_1 = tslib_1.__importDefault(require("./commitAuthorBreakdown"));
var deploys_1 = tslib_1.__importDefault(require("./deploys"));
var issues_1 = tslib_1.__importDefault(require("./issues"));
var otherProjects_1 = tslib_1.__importDefault(require("./otherProjects"));
var projectReleaseDetails_1 = tslib_1.__importDefault(require("./projectReleaseDetails"));
var releaseAdoption_1 = tslib_1.__importDefault(require("./releaseAdoption"));
var releaseArchivedNotice_1 = tslib_1.__importDefault(require("./releaseArchivedNotice"));
var releaseComparisonChart_1 = tslib_1.__importDefault(require("./releaseComparisonChart"));
var releaseDetailsRequest_1 = tslib_1.__importDefault(require("./releaseDetailsRequest"));
var releaseStats_1 = tslib_1.__importDefault(require("./releaseStats"));
var totalCrashFreeUsers_1 = tslib_1.__importDefault(require("./totalCrashFreeUsers"));
var RELEASE_PERIOD_KEY = 'release';
var TransactionsListOption;
(function (TransactionsListOption) {
    TransactionsListOption["FAILURE_COUNT"] = "failure_count";
    TransactionsListOption["TPM"] = "tpm";
    TransactionsListOption["SLOW"] = "slow";
    TransactionsListOption["SLOW_LCP"] = "slow_lcp";
    TransactionsListOption["REGRESSION"] = "regression";
    TransactionsListOption["IMPROVEMENT"] = "improved";
})(TransactionsListOption = exports.TransactionsListOption || (exports.TransactionsListOption = {}));
var ReleaseOverview = /** @class */ (function (_super) {
    tslib_1.__extends(ReleaseOverview, _super);
    function ReleaseOverview() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleYAxisChange = function (yAxis, project) {
            var _a = _this.props, location = _a.location, router = _a.router, organization = _a.organization;
            var _b = location.query, eventType = _b.eventType, vitalType = _b.vitalType, query = tslib_1.__rest(_b, ["eventType", "vitalType"]);
            analytics_1.trackAnalyticsEvent({
                eventKey: "release_detail.change_chart",
                eventName: "Release Detail: Change Chart",
                organization_id: parseInt(organization.id, 10),
                display: yAxis,
                eventType: eventType,
                vitalType: vitalType,
                platform: project.platform,
            });
            router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, query), { yAxis: yAxis }) }));
        };
        _this.handleEventTypeChange = function (eventType, project) {
            var _a = _this.props, location = _a.location, router = _a.router, organization = _a.organization;
            analytics_1.trackAnalyticsEvent({
                eventKey: "release_detail.change_chart",
                eventName: "Release Detail: Change Chart",
                organization_id: parseInt(organization.id, 10),
                display: releaseChartControls_1.YAxis.EVENTS,
                eventType: eventType,
                platform: project.platform,
            });
            router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { eventType: eventType }) }));
        };
        _this.handleVitalTypeChange = function (vitalType, project) {
            var _a = _this.props, location = _a.location, router = _a.router, organization = _a.organization;
            analytics_1.trackAnalyticsEvent({
                eventKey: "release_detail.change_chart",
                eventName: "Release Detail: Change Chart",
                organization_id: parseInt(organization.id, 10),
                display: releaseChartControls_1.YAxis.COUNT_VITAL,
                vitalType: vitalType,
                platform: project.platform,
            });
            router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { vitalType: vitalType }) }));
        };
        _this.handleRestore = function (project, successCallback) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, params, organization, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, params = _a.params, organization = _a.organization;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, release_1.restoreRelease(new api_1.Client(), {
                                orgSlug: organization.slug,
                                projectSlug: project.slug,
                                releaseVersion: params.release,
                            })];
                    case 2:
                        _c.sent();
                        successCallback();
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleTransactionsListSortChange = function (value) {
            var location = _this.props.location;
            var target = {
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { showTransactions: value, transactionCursor: undefined }),
            };
            react_router_1.browserHistory.push(target);
        };
        _this.handleDateChange = function (datetime) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var start = datetime.start, end = datetime.end, relative = datetime.relative, utc = datetime.utc;
            if (start && end) {
                var parser = utc ? moment_1.default.utc : moment_1.default;
                router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { pageStatsPeriod: undefined, pageStart: parser(start).format(), pageEnd: parser(end).format(), pageUtc: utc !== null && utc !== void 0 ? utc : undefined }) }));
                return;
            }
            router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { pageStatsPeriod: relative === RELEASE_PERIOD_KEY ? undefined : relative, pageStart: undefined, pageEnd: undefined, pageUtc: undefined }) }));
        };
        return _this;
    }
    ReleaseOverview.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, organization = _a.organization;
        return routeTitle_1.default(locale_1.t('Release %s', formatters_1.formatVersion(params.release)), organization.slug, false);
    };
    ReleaseOverview.prototype.getYAxis = function (hasHealthData, hasPerformance) {
        var yAxis = this.props.location.query.yAxis;
        if (typeof yAxis === 'string') {
            if (Object.values(releaseChartControls_1.YAxis).includes(yAxis)) {
                return yAxis;
            }
        }
        if (hasHealthData) {
            return releaseChartControls_1.YAxis.SESSIONS;
        }
        if (hasPerformance) {
            return releaseChartControls_1.YAxis.FAILED_TRANSACTIONS;
        }
        return releaseChartControls_1.YAxis.EVENTS;
    };
    ReleaseOverview.prototype.getEventType = function (yAxis) {
        if (yAxis === releaseChartControls_1.YAxis.EVENTS) {
            var eventType = this.props.location.query.eventType;
            if (typeof eventType === 'string') {
                if (Object.values(releaseChartControls_1.EventType).includes(eventType)) {
                    return eventType;
                }
            }
        }
        return releaseChartControls_1.EventType.ALL;
    };
    ReleaseOverview.prototype.getVitalType = function (yAxis) {
        if (yAxis === releaseChartControls_1.YAxis.COUNT_VITAL) {
            var vitalType = this.props.location.query.vitalType;
            if (typeof vitalType === 'string') {
                if (Object.values(fields_1.WebVital).includes(vitalType)) {
                    return vitalType;
                }
            }
        }
        return fields_1.WebVital.LCP;
    };
    ReleaseOverview.prototype.getReleaseEventView = function (version, projectId, selectedSort, releaseBounds, defaultStatsPeriod) {
        var _a = this.props, selection = _a.selection, location = _a.location, organization = _a.organization;
        var environments = selection.environments;
        var _b = utils_2.getReleaseParams({
            location: location,
            releaseBounds: releaseBounds,
            defaultStatsPeriod: defaultStatsPeriod,
            allowEmptyPeriod: organization.features.includes('release-comparison'),
        }), start = _b.start, end = _b.end, statsPeriod = _b.statsPeriod;
        var baseQuery = {
            id: undefined,
            version: 2,
            name: "Release " + formatters_1.formatVersion(version),
            query: "event.type:transaction release:" + version,
            fields: ['transaction', 'failure_count()', 'epm()', 'p50()'],
            orderby: '-failure_count',
            range: statsPeriod || undefined,
            environment: environments,
            projects: [projectId],
            start: start ? dates_1.getUtcDateString(start) : undefined,
            end: end ? dates_1.getUtcDateString(end) : undefined,
        };
        switch (selectedSort.value) {
            case TransactionsListOption.SLOW_LCP:
                return eventView_1.default.fromSavedQuery(tslib_1.__assign(tslib_1.__assign({}, baseQuery), { query: "event.type:transaction release:" + version + " epm():>0.01 has:measurements.lcp", fields: ['transaction', 'failure_count()', 'epm()', 'p75(measurements.lcp)'], orderby: 'p75_measurements_lcp' }));
            case TransactionsListOption.SLOW:
                return eventView_1.default.fromSavedQuery(tslib_1.__assign(tslib_1.__assign({}, baseQuery), { query: "event.type:transaction release:" + version + " epm():>0.01" }));
            case TransactionsListOption.FAILURE_COUNT:
                return eventView_1.default.fromSavedQuery(tslib_1.__assign(tslib_1.__assign({}, baseQuery), { query: "event.type:transaction release:" + version + " failure_count():>0" }));
            default:
                return eventView_1.default.fromSavedQuery(baseQuery);
        }
    };
    ReleaseOverview.prototype.getReleaseTrendView = function (version, projectId, versionDate, releaseBounds, defaultStatsPeriod) {
        var _a = this.props, selection = _a.selection, location = _a.location, organization = _a.organization;
        var environments = selection.environments;
        var _b = utils_2.getReleaseParams({
            location: location,
            releaseBounds: releaseBounds,
            defaultStatsPeriod: defaultStatsPeriod,
            allowEmptyPeriod: organization.features.includes('release-comparison'),
        }), start = _b.start, end = _b.end, statsPeriod = _b.statsPeriod;
        var trendView = eventView_1.default.fromSavedQuery({
            id: undefined,
            version: 2,
            name: "Release " + formatters_1.formatVersion(version),
            fields: ['transaction'],
            query: 'tpm():>0.01 trend_percentage():>0%',
            range: statsPeriod || undefined,
            environment: environments,
            projects: [projectId],
            start: start ? dates_1.getUtcDateString(start) : undefined,
            end: end ? dates_1.getUtcDateString(end) : undefined,
        });
        trendView.middle = versionDate;
        return trendView;
    };
    Object.defineProperty(ReleaseOverview.prototype, "pageDateTime", {
        get: function () {
            var query = this.props.location.query;
            var _a = getParams_1.getParams(query, {
                allowEmptyPeriod: true,
                allowAbsoluteDatetime: true,
                allowAbsolutePageDatetime: true,
            }), start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod;
            if (statsPeriod) {
                return { period: statsPeriod };
            }
            if (start && end) {
                return {
                    start: moment_1.default.utc(start).format(),
                    end: moment_1.default.utc(end).format(),
                };
            }
            return {};
        },
        enumerable: false,
        configurable: true
    });
    ReleaseOverview.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, selection = _a.selection, location = _a.location, api = _a.api, router = _a.router;
        var _b = this.pageDateTime, start = _b.start, end = _b.end, period = _b.period, utc = _b.utc;
        return (<__1.ReleaseContext.Consumer>
        {function (_a) {
                var release = _a.release, project = _a.project, deploys = _a.deploys, releaseMeta = _a.releaseMeta, refetchData = _a.refetchData, defaultStatsPeriod = _a.defaultStatsPeriod, isHealthLoading = _a.isHealthLoading, getHealthData = _a.getHealthData, hasHealthData = _a.hasHealthData, releaseBounds = _a.releaseBounds;
                var commitCount = release.commitCount, version = release.version;
                var hasDiscover = organization.features.includes('discover-basic');
                var hasPerformance = organization.features.includes('performance-view');
                var yAxis = _this.getYAxis(hasHealthData, hasPerformance);
                var eventType = _this.getEventType(yAxis);
                var vitalType = _this.getVitalType(yAxis);
                var _b = getTransactionsListSort(location), selectedSort = _b.selectedSort, sortOptions = _b.sortOptions;
                var releaseEventView = _this.getReleaseEventView(version, project.id, selectedSort, releaseBounds, defaultStatsPeriod);
                var titles = selectedSort.value !== TransactionsListOption.SLOW_LCP
                    ? [locale_1.t('transaction'), locale_1.t('failure_count()'), locale_1.t('tpm()'), locale_1.t('p50()')]
                    : [locale_1.t('transaction'), locale_1.t('failure_count()'), locale_1.t('tpm()'), locale_1.t('p75(lcp)')];
                var releaseTrendView = _this.getReleaseTrendView(version, project.id, releaseMeta.released, releaseBounds, defaultStatsPeriod);
                var generateLink = {
                    transaction: generateTransactionLink(version, project.id, selection, location.query.showTransactions),
                };
                return (<releaseDetailsRequest_1.default organization={organization} location={location} disable={!organization.features.includes('release-comparison')} version={version} releaseBounds={releaseBounds}>
              {function (_a) {
                        var thisRelease = _a.thisRelease, allReleases = _a.allReleases, loading = _a.loading, reloading = _a.reloading, errored = _a.errored;
                        return (<thirds_1.Body>
                  <thirds_1.Main>
                    {utils_2.isReleaseArchived(release) && (<releaseArchivedNotice_1.default onRestore={function () { return _this.handleRestore(project, refetchData); }}/>)}
                    <feature_1.default features={['release-comparison']}>
                      {function (_a) {
                                var _b;
                                var hasFeature = _a.hasFeature;
                                return hasFeature ? (<react_1.Fragment>
                            <StyledPageTimeRangeSelector organization={organization} relative={period !== null && period !== void 0 ? period : ''} start={start !== null && start !== void 0 ? start : null} end={end !== null && end !== void 0 ? end : null} utc={utc !== null && utc !== void 0 ? utc : null} onUpdate={_this.handleDateChange} relativeOptions={tslib_1.__assign((_b = {}, _b[RELEASE_PERIOD_KEY] = (<react_1.Fragment>
                                    {locale_1.t('Entire Release Period')} (
                                    <dateTime_1.default date={releaseBounds.releaseStart} timeAndDate/>{' '}
                                    -{' '}
                                    <dateTime_1.default date={releaseBounds.releaseEnd} timeAndDate/>
                                    )
                                  </react_1.Fragment>), _b), constants_1.DEFAULT_RELATIVE_PERIODS)} defaultPeriod={RELEASE_PERIOD_KEY}/>
                            <releaseComparisonChart_1.default release={release} releaseSessions={thisRelease} allSessions={allReleases} platform={project.platform} location={location} loading={loading} reloading={reloading} errored={errored} project={project} organization={organization} api={api}/>
                          </react_1.Fragment>) : ((hasDiscover || hasPerformance || hasHealthData) && (<chart_1.default releaseMeta={releaseMeta} selection={selection} yAxis={yAxis} onYAxisChange={function (display) {
                                        return _this.handleYAxisChange(display, project);
                                    }} eventType={eventType} onEventTypeChange={function (type) {
                                        return _this.handleEventTypeChange(type, project);
                                    }} vitalType={vitalType} onVitalTypeChange={function (type) {
                                        return _this.handleVitalTypeChange(type, project);
                                    }} router={router} organization={organization} hasHealthData={hasHealthData} location={location} api={api} version={version} hasDiscover={hasDiscover} hasPerformance={hasPerformance} platform={project.platform} defaultStatsPeriod={defaultStatsPeriod} projectSlug={project.slug}/>));
                            }}
                    </feature_1.default>

                    <issues_1.default organization={organization} selection={selection} version={version} location={location} defaultStatsPeriod={defaultStatsPeriod} releaseBounds={releaseBounds} queryFilterDescription={locale_1.t('In this release')} withChart/>
                    <feature_1.default features={['performance-view']}>
                      <transactionsList_1.default location={location} organization={organization} eventView={releaseEventView} trendView={releaseTrendView} selected={selectedSort} options={sortOptions} handleDropdownChange={_this.handleTransactionsListSortChange} titles={titles} generateLink={generateLink}/>
                    </feature_1.default>
                  </thirds_1.Main>
                  <thirds_1.Side>
                    <releaseStats_1.default organization={organization} release={release} project={project} location={location} selection={selection} hasHealthData={hasHealthData} getHealthData={getHealthData} isHealthLoading={isHealthLoading}/>
                    <feature_1.default features={['release-comparison']}>
                      <releaseAdoption_1.default releaseSessions={thisRelease} allSessions={allReleases} loading={loading} reloading={reloading} errored={errored} release={release} project={project}/>
                    </feature_1.default>
                    <projectReleaseDetails_1.default release={release} releaseMeta={releaseMeta} orgSlug={organization.slug} projectSlug={project.slug}/>
                    {commitCount > 0 && (<commitAuthorBreakdown_1.default version={version} orgId={organization.slug} projectSlug={project.slug}/>)}
                    {releaseMeta.projects.length > 1 && (<otherProjects_1.default projects={releaseMeta.projects.filter(function (p) { return p.slug !== project.slug; })} location={location} version={version} organization={organization}/>)}
                    {hasHealthData && (<totalCrashFreeUsers_1.default organization={organization} version={version} projectSlug={project.slug} location={location}/>)}
                    {deploys.length > 0 && (<deploys_1.default version={version} orgSlug={organization.slug} deploys={deploys} projectId={project.id}/>)}
                  </thirds_1.Side>
                </thirds_1.Body>);
                    }}
            </releaseDetailsRequest_1.default>);
            }}
      </__1.ReleaseContext.Consumer>);
    };
    return ReleaseOverview;
}(asyncView_1.default));
function generateTransactionLink(version, projectId, selection, value) {
    return function (organization, tableRow, _query) {
        var transaction = tableRow.transaction;
        var trendTransaction = ['regression', 'improved'].includes(value);
        var environments = selection.environments, datetime = selection.datetime;
        var start = datetime.start, end = datetime.end, period = datetime.period;
        return utils_1.transactionSummaryRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transaction,
            query: {
                query: trendTransaction ? '' : "release:" + version,
                environment: environments,
                start: start ? dates_1.getUtcDateString(start) : undefined,
                end: end ? dates_1.getUtcDateString(end) : undefined,
                statsPeriod: period,
            },
            projectID: projectId.toString(),
            display: trendTransaction ? charts_1.DisplayModes.TREND : charts_1.DisplayModes.DURATION,
        });
    };
}
function getDropdownOptions() {
    return [
        {
            sort: { kind: 'desc', field: 'failure_count' },
            value: TransactionsListOption.FAILURE_COUNT,
            label: locale_1.t('Failing Transactions'),
        },
        {
            sort: { kind: 'desc', field: 'epm' },
            value: TransactionsListOption.TPM,
            label: locale_1.t('Frequent Transactions'),
        },
        {
            sort: { kind: 'desc', field: 'p50' },
            value: TransactionsListOption.SLOW,
            label: locale_1.t('Slow Transactions'),
        },
        {
            sort: { kind: 'desc', field: 'p75_measurements_lcp' },
            value: TransactionsListOption.SLOW_LCP,
            label: locale_1.t('Slow LCP'),
        },
        {
            sort: { kind: 'desc', field: 'trend_percentage()' },
            query: [['t_test()', '<-6']],
            trendType: types_1.TrendChangeType.REGRESSION,
            value: TransactionsListOption.REGRESSION,
            label: locale_1.t('Trending Regressions'),
        },
        {
            sort: { kind: 'asc', field: 'trend_percentage()' },
            query: [['t_test()', '>6']],
            trendType: types_1.TrendChangeType.IMPROVED,
            value: TransactionsListOption.IMPROVEMENT,
            label: locale_1.t('Trending Improvements'),
        },
    ];
}
function getTransactionsListSort(location) {
    var sortOptions = getDropdownOptions();
    var urlParam = queryString_1.decodeScalar(location.query.showTransactions, TransactionsListOption.FAILURE_COUNT);
    var selectedSort = sortOptions.find(function (opt) { return opt.value === urlParam; }) || sortOptions[0];
    return { selectedSort: selectedSort, sortOptions: sortOptions };
}
var StyledPageTimeRangeSelector = styled_1.default(pageTimeRangeSelector_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(1.5));
exports.default = withApi_1.default(withGlobalSelection_1.default(withOrganization_1.default(ReleaseOverview)));
var templateObject_1;
//# sourceMappingURL=index.jsx.map