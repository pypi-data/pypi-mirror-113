Object.defineProperty(exports, "__esModule", { value: true });
exports.IssueListOverview = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var react_1 = require("@sentry/react");
var js_cookie_1 = tslib_1.__importDefault(require("js-cookie"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var mapValues_1 = tslib_1.__importDefault(require("lodash/mapValues"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var pickBy_1 = tslib_1.__importDefault(require("lodash/pickBy"));
var qs = tslib_1.__importStar(require("query-string"));
var members_1 = require("app/actionCreators/members");
var savedSearches_1 = require("app/actionCreators/savedSearches");
var tags_1 = require("app/actionCreators/tags");
var groupActions_1 = tslib_1.__importDefault(require("app/actions/groupActions"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var queryCount_1 = tslib_1.__importDefault(require("app/components/queryCount"));
var group_1 = tslib_1.__importDefault(require("app/components/stream/group"));
var processingIssueList_1 = tslib_1.__importDefault(require("app/components/stream/processingIssueList"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var groupStore_1 = tslib_1.__importDefault(require("app/stores/groupStore"));
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_2 = require("app/utils");
var analytics_1 = require("app/utils/analytics");
var callIfFunction_1 = require("app/utils/callIfFunction");
var cursorPoller_1 = tslib_1.__importDefault(require("app/utils/cursorPoller"));
var dates_1 = require("app/utils/dates");
var getCurrentSentryReactTransaction_1 = tslib_1.__importDefault(require("app/utils/getCurrentSentryReactTransaction"));
var parseApiError_1 = tslib_1.__importDefault(require("app/utils/parseApiError"));
var parseLinkHeader_1 = tslib_1.__importDefault(require("app/utils/parseLinkHeader"));
var streamManager_1 = tslib_1.__importDefault(require("app/utils/streamManager"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withIssueTags_1 = tslib_1.__importDefault(require("app/utils/withIssueTags"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withSavedSearches_1 = tslib_1.__importDefault(require("app/utils/withSavedSearches"));
var actions_1 = tslib_1.__importDefault(require("./actions"));
var filters_1 = tslib_1.__importDefault(require("./filters"));
var header_1 = tslib_1.__importDefault(require("./header"));
var noGroupsHandler_1 = tslib_1.__importDefault(require("./noGroupsHandler"));
var sidebar_1 = tslib_1.__importDefault(require("./sidebar"));
var utils_3 = require("./utils");
var MAX_ITEMS = 25;
var DEFAULT_SORT = utils_3.IssueSortOptions.DATE;
var DEFAULT_DISPLAY = utils_3.IssueDisplayOptions.EVENTS;
// the default period for the graph in each issue row
var DEFAULT_GRAPH_STATS_PERIOD = '24h';
// the allowed period choices for graph in each issue row
var DYNAMIC_COUNTS_STATS_PERIODS = new Set(['14d', '24h', 'auto']);
var IssueListOverview = /** @class */ (function (_super) {
    tslib_1.__extends(IssueListOverview, _super);
    function IssueListOverview() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this._streamManager = new streamManager_1.default(groupStore_1.default);
        _this.getEndpointParams = function () {
            var selection = _this.props.selection;
            var params = tslib_1.__assign({ project: selection.projects, environment: selection.environments, query: _this.getQuery() }, selection.datetime);
            if (selection.datetime.period) {
                delete params.period;
                params.statsPeriod = selection.datetime.period;
            }
            if (params.end) {
                params.end = dates_1.getUtcDateString(params.end);
            }
            if (params.start) {
                params.start = dates_1.getUtcDateString(params.start);
            }
            var sort = _this.getSort();
            if (sort !== DEFAULT_SORT) {
                params.sort = sort;
            }
            var display = _this.getDisplay();
            if (display !== DEFAULT_DISPLAY) {
                params.display = display;
            }
            var groupStatsPeriod = _this.getGroupStatsPeriod();
            if (groupStatsPeriod !== DEFAULT_GRAPH_STATS_PERIOD) {
                params.groupStatsPeriod = groupStatsPeriod;
            }
            // only include defined values.
            return pickBy_1.default(params, function (v) { return utils_2.defined(v); });
        };
        _this.getGlobalSearchProjectIds = function () {
            return _this.props.selection.projects;
        };
        _this.fetchStats = function (groups) {
            // If we have no groups to fetch, just skip stats
            if (!groups.length) {
                _this.setState({ hasSessions: false });
                return;
            }
            var requestParams = tslib_1.__assign(tslib_1.__assign({}, _this.getEndpointParams()), { groups: groups });
            // If no stats period values are set, use default
            if (!requestParams.statsPeriod && !requestParams.start) {
                requestParams.statsPeriod = constants_1.DEFAULT_STATS_PERIOD;
            }
            if (_this.props.organization.features.includes('issue-percent-display')) {
                requestParams.expand = 'sessions';
            }
            _this._lastStatsRequest = _this.props.api.request(_this.getGroupStatsEndpoint(), {
                method: 'GET',
                data: qs.stringify(requestParams),
                success: function (data) {
                    if (!data) {
                        return;
                    }
                    groupActions_1.default.populateStats(groups, data);
                    var hasSessions = data.filter(function (groupStats) { return !groupStats.sessionCount; }).length === 0;
                    if (hasSessions !== _this.state.hasSessions) {
                        _this.setState({
                            hasSessions: hasSessions,
                        });
                    }
                },
                error: function (err) {
                    _this.setState({
                        error: parseApiError_1.default(err),
                    });
                },
                complete: function () {
                    _this._lastStatsRequest = null;
                },
            });
        };
        _this.fetchCounts = function (currentQueryCount, fetchAllCounts) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var organization, _queryCounts, queryCounts, endpointParams, tabQueriesWithCounts, currentTabQuery, requestParams, response, e_1, tab;
            var _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        organization = this.props.organization;
                        _queryCounts = this.state.queryCounts;
                        queryCounts = tslib_1.__assign({}, _queryCounts);
                        endpointParams = this.getEndpointParams();
                        tabQueriesWithCounts = utils_3.getTabsWithCounts(organization);
                        currentTabQuery = tabQueriesWithCounts.includes(endpointParams.query)
                            ? endpointParams.query
                            : null;
                        if (!(fetchAllCounts ||
                            !tabQueriesWithCounts.every(function (tabQuery) { return queryCounts[tabQuery] !== undefined; }))) return [3 /*break*/, 4];
                        requestParams = tslib_1.__assign(tslib_1.__assign({}, omit_1.default(endpointParams, 'query')), { 
                            // fetch the counts for the tabs whose counts haven't been fetched yet
                            query: tabQueriesWithCounts.filter(function (_query) { return _query !== currentTabQuery; }) });
                        // If no stats period values are set, use default
                        if (!requestParams.statsPeriod && !requestParams.start) {
                            requestParams.statsPeriod = constants_1.DEFAULT_STATS_PERIOD;
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.props.api.requestPromise(this.getGroupCountsEndpoint(), {
                                method: 'GET',
                                data: qs.stringify(requestParams),
                            })];
                    case 2:
                        response = _b.sent();
                        // Counts coming from the counts endpoint is limited to 100, for >= 100 we display 99+
                        queryCounts = tslib_1.__assign(tslib_1.__assign({}, queryCounts), mapValues_1.default(response, function (count) { return ({
                            count: count,
                            hasMore: count > utils_3.TAB_MAX_COUNT,
                        }); }));
                        return [3 /*break*/, 4];
                    case 3:
                        e_1 = _b.sent();
                        this.setState({
                            error: parseApiError_1.default(e_1),
                        });
                        return [2 /*return*/];
                    case 4:
                        // Update the count based on the exact number of issues, these shown as is
                        if (currentTabQuery) {
                            queryCounts[currentTabQuery] = {
                                count: currentQueryCount,
                                hasMore: false,
                            };
                            tab = (_a = utils_3.getTabs(organization).find(function (_a) {
                                var _b = tslib_1.__read(_a, 1), tabQuery = _b[0];
                                return currentTabQuery === tabQuery;
                            })) === null || _a === void 0 ? void 0 : _a[1];
                            if (tab && !endpointParams.cursor) {
                                analytics_1.trackAnalyticsEvent({
                                    eventKey: 'issues_tab.viewed',
                                    eventName: 'Viewed Issues Tab',
                                    organization_id: organization.id,
                                    tab: tab.analyticsName,
                                    num_issues: queryCounts[currentTabQuery].count,
                                });
                            }
                        }
                        this.setState({ queryCounts: queryCounts });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.fetchData = function (fetchAllCounts) {
            if (fetchAllCounts === void 0) { fetchAllCounts = false; }
            groupStore_1.default.loadInitialData([]);
            _this._streamManager.reset();
            var transaction = getCurrentSentryReactTransaction_1.default();
            transaction === null || transaction === void 0 ? void 0 : transaction.setTag('query.sort', _this.getSort());
            _this.setState({
                issuesLoading: true,
                queryCount: 0,
                itemsRemoved: 0,
                error: null,
            });
            var requestParams = tslib_1.__assign(tslib_1.__assign({}, _this.getEndpointParams()), { limit: MAX_ITEMS, shortIdLookup: 1 });
            var currentQuery = _this.props.location.query || {};
            if ('cursor' in currentQuery) {
                requestParams.cursor = currentQuery.cursor;
            }
            // If no stats period values are set, use default
            if (!requestParams.statsPeriod && !requestParams.start) {
                requestParams.statsPeriod = constants_1.DEFAULT_STATS_PERIOD;
            }
            requestParams.expand = ['owners', 'inbox'];
            requestParams.collapse = 'stats';
            if (_this._lastRequest) {
                _this._lastRequest.cancel();
            }
            if (_this._lastStatsRequest) {
                _this._lastStatsRequest.cancel();
            }
            _this._poller.disable();
            _this._lastRequest = _this.props.api.request(_this.getGroupListEndpoint(), {
                method: 'GET',
                data: qs.stringify(requestParams),
                success: function (data, _, jqXHR) {
                    if (!jqXHR) {
                        return;
                    }
                    var orgId = _this.props.params.orgId;
                    // If this is a direct hit, we redirect to the intended result directly.
                    if (jqXHR.getResponseHeader('X-Sentry-Direct-Hit') === '1') {
                        var redirect = void 0;
                        if (data[0] && data[0].matchingEventId) {
                            var _a = data[0], id = _a.id, matchingEventId = _a.matchingEventId;
                            redirect = "/organizations/" + orgId + "/issues/" + id + "/events/" + matchingEventId + "/";
                        }
                        else {
                            var id = data[0].id;
                            redirect = "/organizations/" + orgId + "/issues/" + id + "/";
                        }
                        react_router_1.browserHistory.replace({
                            pathname: redirect,
                            query: utils_1.extractSelectionParameters(_this.props.location.query),
                        });
                        return;
                    }
                    _this._streamManager.push(data);
                    _this.fetchStats(data.map(function (group) { return group.id; }));
                    var hits = jqXHR.getResponseHeader('X-Hits');
                    var queryCount = typeof hits !== 'undefined' && hits ? parseInt(hits, 10) || 0 : 0;
                    var maxHits = jqXHR.getResponseHeader('X-Max-Hits');
                    var queryMaxCount = typeof maxHits !== 'undefined' && maxHits ? parseInt(maxHits, 10) || 0 : 0;
                    var pageLinks = jqXHR.getResponseHeader('Link');
                    _this.fetchCounts(queryCount, fetchAllCounts);
                    _this.setState({
                        error: null,
                        issuesLoading: false,
                        queryCount: queryCount,
                        queryMaxCount: queryMaxCount,
                        pageLinks: pageLinks !== null ? pageLinks : '',
                    });
                },
                error: function (err) {
                    analytics_1.trackAnalyticsEvent({
                        eventKey: 'issue_search.failed',
                        eventName: 'Issue Search: Failed',
                        organization_id: _this.props.organization.id,
                        search_type: 'issues',
                        search_source: 'main_search',
                        error: parseApiError_1.default(err),
                    });
                    _this.setState({
                        error: parseApiError_1.default(err),
                        issuesLoading: false,
                    });
                },
                complete: function () {
                    _this._lastRequest = null;
                    _this.resumePolling();
                },
            });
        };
        _this.resumePolling = function () {
            if (!_this.state.pageLinks) {
                return;
            }
            // Only resume polling if we're on the first page of results
            var links = parseLinkHeader_1.default(_this.state.pageLinks);
            if (links && !links.previous.results && _this.state.realtimeActive) {
                // Remove collapse stats from endpoint before supplying to poller
                var issueEndpoint = new URL(links.previous.href, window.location.origin);
                issueEndpoint.searchParams.delete('collapse');
                _this._poller.setEndpoint(decodeURIComponent(issueEndpoint.href));
                _this._poller.enable();
            }
        };
        _this.onRealtimeChange = function (realtime) {
            js_cookie_1.default.set('realtimeActive', realtime.toString());
            _this.setState({ realtimeActive: realtime });
        };
        _this.onSelectStatsPeriod = function (period) {
            if (period !== _this.getGroupStatsPeriod()) {
                _this.transitionTo({ groupStatsPeriod: period });
            }
        };
        _this.onRealtimePoll = function (data, _links) {
            // Note: We do not update state with cursors from polling,
            // `CursorPoller` updates itself with new cursors
            _this._streamManager.unshift(data);
        };
        _this.listener = groupStore_1.default.listen(function () { return _this.onGroupChange(); }, undefined);
        _this.onIssueListSidebarSearch = function (query) {
            analytics_1.analytics('search.searched', {
                org_id: _this.props.organization.id,
                query: query,
                search_type: 'issues',
                search_source: 'search_builder',
            });
            _this.onSearch(query);
        };
        _this.onSearch = function (query) {
            if (query === _this.state.query) {
                // if query is the same, just re-fetch data
                _this.fetchData();
            }
            else {
                // Clear the saved search as the user wants something else.
                _this.transitionTo({ query: query }, null);
            }
        };
        _this.onSortChange = function (sort) {
            _this.transitionTo({ sort: sort });
        };
        _this.onDisplayChange = function (display) {
            _this.transitionTo({ display: display });
        };
        _this.onCursorChange = function (cursor, _path, query, pageDiff) {
            var queryPageInt = parseInt(query.page, 10);
            var nextPage = isNaN(queryPageInt)
                ? pageDiff
                : queryPageInt + pageDiff;
            // unset cursor and page when we navigate back to the first page
            // also reset cursor if somehow the previous button is enabled on
            // first page and user attempts to go backwards
            if (nextPage <= 0) {
                cursor = undefined;
                nextPage = undefined;
            }
            _this.transitionTo({ cursor: cursor, page: nextPage });
        };
        _this.onSidebarToggle = function () {
            var organization = _this.props.organization;
            _this.setState({
                isSidebarVisible: !_this.state.isSidebarVisible,
                renderSidebar: true,
            });
            analytics_1.analytics('issue.search_sidebar_clicked', {
                org_id: parseInt(organization.id, 10),
            });
        };
        _this.transitionTo = function (newParams, savedSearch) {
            if (newParams === void 0) { newParams = {}; }
            if (savedSearch === void 0) { savedSearch = _this.props.savedSearch; }
            var query = tslib_1.__assign(tslib_1.__assign({}, _this.getEndpointParams()), newParams);
            var organization = _this.props.organization;
            var path;
            if (savedSearch && savedSearch.id) {
                path = "/organizations/" + organization.slug + "/issues/searches/" + savedSearch.id + "/";
                // Remove the query as saved searches bring their own query string.
                delete query.query;
                // If we aren't going to another page in the same search
                // drop the query and replace the current project, with the saved search search project
                // if available.
                if (!query.cursor && savedSearch.projectId) {
                    query.project = [savedSearch.projectId];
                }
                if (!query.cursor && !newParams.sort && savedSearch.sort) {
                    query.sort = savedSearch.sort;
                }
            }
            else {
                path = "/organizations/" + organization.slug + "/issues/";
            }
            // Remove inbox tab specific sort
            if (query.sort === utils_3.IssueSortOptions.INBOX && query.query !== utils_3.Query.FOR_REVIEW) {
                delete query.sort;
            }
            if (path !== _this.props.location.pathname ||
                !isEqual_1.default(query, _this.props.location.query)) {
                react_router_1.browserHistory.push({
                    pathname: path,
                    query: query,
                });
                _this.setState({ issuesLoading: true });
            }
        };
        _this.renderGroupNodes = function (ids, groupStatsPeriod) {
            var topIssue = ids[0];
            var memberList = _this.state.memberList;
            var query = _this.getQuery();
            var showInboxTime = _this.getSort() === utils_3.IssueSortOptions.INBOX;
            return ids.map(function (id, index) {
                var hasGuideAnchor = id === topIssue;
                var group = groupStore_1.default.get(id);
                var members;
                if (group === null || group === void 0 ? void 0 : group.project) {
                    members = memberList[group.project.slug];
                }
                var showReprocessingTab = _this.displayReprocessingTab();
                var displayReprocessingLayout = _this.displayReprocessingLayout(showReprocessingTab, query);
                return (<group_1.default index={index} key={id} id={id} statsPeriod={groupStatsPeriod} query={query} hasGuideAnchor={hasGuideAnchor} memberList={members} displayReprocessingLayout={displayReprocessingLayout} useFilteredStats showInboxTime={showInboxTime} display={_this.getDisplay()}/>);
            });
        };
        _this.fetchSavedSearches = function () {
            var _a = _this.props, organization = _a.organization, api = _a.api;
            savedSearches_1.fetchSavedSearches(api, organization.slug);
        };
        _this.onSavedSearchSelect = function (savedSearch) {
            analytics_1.trackAnalyticsEvent({
                eventKey: 'organization_saved_search.selected',
                eventName: 'Organization Saved Search: Selected saved search',
                organization_id: _this.props.organization.id,
                search_type: 'issues',
                id: savedSearch.id ? parseInt(savedSearch.id, 10) : -1,
            });
            _this.setState({ issuesLoading: true }, function () { return _this.transitionTo(undefined, savedSearch); });
        };
        _this.onSavedSearchDelete = function (search) {
            var orgId = _this.props.params.orgId;
            savedSearches_1.deleteSavedSearch(_this.props.api, orgId, search).then(function () {
                _this.setState({
                    issuesLoading: true,
                }, function () { return _this.transitionTo({}, null); });
            });
        };
        _this.onDelete = function () {
            _this.fetchData(true);
        };
        _this.onMarkReviewed = function (itemIds) {
            var _a;
            var query = _this.getQuery();
            if (!utils_3.isForReviewQuery(query)) {
                return;
            }
            var _b = _this.state, queryCounts = _b.queryCounts, itemsRemoved = _b.itemsRemoved;
            var currentQueryCount = queryCounts[query];
            if (itemIds.length && currentQueryCount) {
                var inInboxCount = itemIds.filter(function (id) { var _a; return (_a = groupStore_1.default.get(id)) === null || _a === void 0 ? void 0 : _a.inbox; }).length;
                currentQueryCount.count -= inInboxCount;
                _this.setState({
                    queryCounts: tslib_1.__assign(tslib_1.__assign({}, queryCounts), (_a = {}, _a[query] = currentQueryCount, _a)),
                    itemsRemoved: itemsRemoved + inInboxCount,
                });
            }
        };
        _this.tagValueLoader = function (key, search) {
            var orgId = _this.props.params.orgId;
            var projectIds = _this.getGlobalSearchProjectIds().map(function (id) { return id.toString(); });
            var endpointParams = _this.getEndpointParams();
            return tags_1.fetchTagValues(_this.props.api, orgId, key, search, projectIds, endpointParams);
        };
        return _this;
    }
    IssueListOverview.prototype.getInitialState = function () {
        var realtimeActiveCookie = js_cookie_1.default.get('realtimeActive');
        var realtimeActive = typeof realtimeActiveCookie === 'undefined'
            ? false
            : realtimeActiveCookie === 'true';
        return {
            groupIds: [],
            selectAllActive: false,
            realtimeActive: realtimeActive,
            pageLinks: '',
            itemsRemoved: 0,
            queryCount: 0,
            queryCounts: {},
            queryMaxCount: 0,
            error: null,
            isSidebarVisible: false,
            renderSidebar: false,
            issuesLoading: true,
            tagsLoading: true,
            memberList: {},
            hasSessions: false,
        };
    };
    IssueListOverview.prototype.componentDidMount = function () {
        var _a;
        var links = parseLinkHeader_1.default(this.state.pageLinks);
        this._poller = new cursorPoller_1.default({
            endpoint: ((_a = links.previous) === null || _a === void 0 ? void 0 : _a.href) || '',
            success: this.onRealtimePoll,
        });
        // Start by getting searches first so if the user is on a saved search
        // or they have a pinned search we load the correct data the first time.
        this.fetchSavedSearches();
        this.fetchTags();
        this.fetchMemberList();
    };
    IssueListOverview.prototype.componentDidUpdate = function (prevProps, prevState) {
        var _a;
        // Fire off profiling/metrics first
        if (prevState.issuesLoading && !this.state.issuesLoading) {
            // First Meaningful Paint for /organizations/:orgId/issues/
            if (prevState.queryCount === null) {
                analytics_1.metric.measure({
                    name: 'app.page.perf.issue-list',
                    start: 'page-issue-list-start',
                    data: {
                        // start_type is set on 'page-issue-list-start'
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
            }
        }
        if (prevState.realtimeActive !== this.state.realtimeActive) {
            // User toggled realtime button
            if (this.state.realtimeActive) {
                this.resumePolling();
            }
            else {
                this._poller.disable();
            }
        }
        // If the project selection has changed reload the member list and tag keys
        // allowing autocomplete and tag sidebar to be more accurate.
        if (!isEqual_1.default(prevProps.selection.projects, this.props.selection.projects)) {
            this.fetchMemberList();
            this.fetchTags();
            // Reset display when selecting multiple projects
            var projects = (_a = this.props.selection.projects) !== null && _a !== void 0 ? _a : [];
            var hasMultipleProjects = projects.length !== 1 || projects[0] === -1;
            if (hasMultipleProjects && this.getDisplay() !== DEFAULT_DISPLAY) {
                this.transitionTo({ display: undefined });
            }
        }
        // Wait for saved searches to load before we attempt to fetch stream data
        if (this.props.savedSearchLoading) {
            return;
        }
        else if (prevProps.savedSearchLoading) {
            this.fetchData();
            return;
        }
        var prevQuery = prevProps.location.query;
        var newQuery = this.props.location.query;
        var selectionChanged = !isEqual_1.default(prevProps.selection, this.props.selection);
        // If any important url parameter changed or saved search changed
        // reload data.
        if (selectionChanged ||
            prevQuery.cursor !== newQuery.cursor ||
            prevQuery.sort !== newQuery.sort ||
            prevQuery.query !== newQuery.query ||
            prevQuery.statsPeriod !== newQuery.statsPeriod ||
            prevQuery.groupStatsPeriod !== newQuery.groupStatsPeriod ||
            prevProps.savedSearch !== this.props.savedSearch) {
            this.fetchData(selectionChanged);
        }
        else if (!this._lastRequest &&
            prevState.issuesLoading === false &&
            this.state.issuesLoading) {
            // Reload if we issues are loading or their loading state changed.
            // This can happen when transitionTo is called
            this.fetchData();
        }
    };
    IssueListOverview.prototype.componentWillUnmount = function () {
        this._poller.disable();
        groupStore_1.default.reset();
        this.props.api.clear();
        callIfFunction_1.callIfFunction(this.listener);
        // Reset store when unmounting because we always fetch on mount
        // This means if you navigate away from stream and then back to stream,
        // this component will go from:
        // "ready" ->
        // "loading" (because fetching saved searches) ->
        // "ready"
        //
        // We don't render anything until saved searches is ready, so this can
        // cause weird side effects (e.g. ProcessingIssueList mounting and making
        // a request, but immediately unmounting when fetching saved searches)
        savedSearches_1.resetSavedSearches();
    };
    IssueListOverview.prototype.getQuery = function () {
        var _a = this.props, savedSearch = _a.savedSearch, location = _a.location;
        if (savedSearch) {
            return savedSearch.query;
        }
        var query = location.query.query;
        if (query !== undefined) {
            return query;
        }
        return constants_1.DEFAULT_QUERY;
    };
    IssueListOverview.prototype.getSort = function () {
        var _a = this.props, location = _a.location, savedSearch = _a.savedSearch;
        if (!location.query.sort && (savedSearch === null || savedSearch === void 0 ? void 0 : savedSearch.id)) {
            return savedSearch.sort;
        }
        if (location.query.sort) {
            return location.query.sort;
        }
        return DEFAULT_SORT;
    };
    IssueListOverview.prototype.getDisplay = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        if (organization.features.includes('issue-percent-display')) {
            if (location.query.display &&
                Object.values(utils_3.IssueDisplayOptions).includes(location.query.display)) {
                return location.query.display;
            }
        }
        return DEFAULT_DISPLAY;
    };
    IssueListOverview.prototype.getGroupStatsPeriod = function () {
        var _a;
        var currentPeriod;
        if (typeof ((_a = this.props.location.query) === null || _a === void 0 ? void 0 : _a.groupStatsPeriod) === 'string') {
            currentPeriod = this.props.location.query.groupStatsPeriod;
        }
        else if (this.getSort() === utils_3.IssueSortOptions.TREND) {
            // Default to the larger graph when sorting by relative change
            currentPeriod = 'auto';
        }
        else {
            currentPeriod = DEFAULT_GRAPH_STATS_PERIOD;
        }
        return DYNAMIC_COUNTS_STATS_PERIODS.has(currentPeriod)
            ? currentPeriod
            : DEFAULT_GRAPH_STATS_PERIOD;
    };
    IssueListOverview.prototype.fetchMemberList = function () {
        var _this = this;
        var _a;
        var projectIds = (_a = this.getGlobalSearchProjectIds()) === null || _a === void 0 ? void 0 : _a.map(function (projectId) {
            return String(projectId);
        });
        members_1.fetchOrgMembers(this.props.api, this.props.organization.slug, projectIds).then(function (members) {
            _this.setState({ memberList: members_1.indexMembersByProject(members) });
        });
    };
    IssueListOverview.prototype.fetchTags = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, selection = _a.selection;
        this.setState({ tagsLoading: true });
        tags_1.loadOrganizationTags(this.props.api, organization.slug, selection).then(function () {
            return _this.setState({ tagsLoading: false });
        });
    };
    IssueListOverview.prototype.getGroupListEndpoint = function () {
        var orgId = this.props.params.orgId;
        return "/organizations/" + orgId + "/issues/";
    };
    IssueListOverview.prototype.getGroupCountsEndpoint = function () {
        var orgId = this.props.params.orgId;
        return "/organizations/" + orgId + "/issues-count/";
    };
    IssueListOverview.prototype.getGroupStatsEndpoint = function () {
        var orgId = this.props.params.orgId;
        return "/organizations/" + orgId + "/issues-stats/";
    };
    IssueListOverview.prototype.onGroupChange = function () {
        var _a;
        var groupIds = (_a = this._streamManager.getAllItems().map(function (item) { return item.id; })) !== null && _a !== void 0 ? _a : [];
        if (!isEqual_1.default(groupIds, this.state.groupIds)) {
            this.setState({ groupIds: groupIds });
        }
    };
    /**
     * Returns true if all results in the current query are visible/on this page
     */
    IssueListOverview.prototype.allResultsVisible = function () {
        if (!this.state.pageLinks) {
            return false;
        }
        var links = parseLinkHeader_1.default(this.state.pageLinks);
        return links && !links.previous.results && !links.next.results;
    };
    IssueListOverview.prototype.displayReprocessingTab = function () {
        var _a;
        var organization = this.props.organization;
        var queryCounts = this.state.queryCounts;
        return (organization.features.includes('reprocessing-v2') &&
            !!((_a = queryCounts === null || queryCounts === void 0 ? void 0 : queryCounts[utils_3.Query.REPROCESSING]) === null || _a === void 0 ? void 0 : _a.count));
    };
    IssueListOverview.prototype.displayReprocessingLayout = function (showReprocessingTab, query) {
        return showReprocessingTab && query === utils_3.Query.REPROCESSING;
    };
    IssueListOverview.prototype.renderLoading = function () {
        return (<StyledPageContent>
        <loadingIndicator_1.default />
      </StyledPageContent>);
    };
    IssueListOverview.prototype.renderStreamBody = function () {
        var _a = this.state, issuesLoading = _a.issuesLoading, error = _a.error, groupIds = _a.groupIds;
        if (issuesLoading) {
            return <loadingIndicator_1.default hideMessage/>;
        }
        if (error) {
            return <loadingError_1.default message={error} onRetry={this.fetchData}/>;
        }
        if (groupIds.length > 0) {
            return (<panels_1.PanelBody>
          {this.renderGroupNodes(groupIds, this.getGroupStatsPeriod())}
        </panels_1.PanelBody>);
        }
        var _b = this.props, api = _b.api, organization = _b.organization, selection = _b.selection;
        return (<noGroupsHandler_1.default api={api} organization={organization} query={this.getQuery()} selectedProjectIds={selection.projects} groupIds={groupIds}/>);
    };
    IssueListOverview.prototype.render = function () {
        var _a, _b, _c;
        if (this.props.savedSearchLoading) {
            return this.renderLoading();
        }
        var _d = this.state, renderSidebar = _d.renderSidebar, isSidebarVisible = _d.isSidebarVisible, tagsLoading = _d.tagsLoading, pageLinks = _d.pageLinks, queryCount = _d.queryCount, queryCounts = _d.queryCounts, realtimeActive = _d.realtimeActive, groupIds = _d.groupIds, queryMaxCount = _d.queryMaxCount, itemsRemoved = _d.itemsRemoved, hasSessions = _d.hasSessions;
        var _e = this.props, organization = _e.organization, savedSearch = _e.savedSearch, savedSearches = _e.savedSearches, tags = _e.tags, selection = _e.selection, location = _e.location, router = _e.router;
        var links = parseLinkHeader_1.default(pageLinks);
        var query = this.getQuery();
        var queryPageInt = parseInt(location.query.page, 10);
        // Cursor must be present for the page number to be used
        var page = isNaN(queryPageInt) || !location.query.cursor ? 0 : queryPageInt;
        var pageBasedCount = page * MAX_ITEMS + groupIds.length;
        var pageCount = pageBasedCount > queryCount ? queryCount : pageBasedCount;
        if (!((_a = links === null || links === void 0 ? void 0 : links.next) === null || _a === void 0 ? void 0 : _a.results) || this.allResultsVisible()) {
            // On last available page
            pageCount = queryCount;
        }
        else if (!((_b = links === null || links === void 0 ? void 0 : links.previous) === null || _b === void 0 ? void 0 : _b.results)) {
            // On first available page
            pageCount = groupIds.length;
        }
        // Subtract # items that have been marked reviewed
        pageCount = Math.max(pageCount - itemsRemoved, 0);
        var modifiedQueryCount = Math.max(queryCount - itemsRemoved, 0);
        var displayCount = locale_1.tct('[count] of [total]', {
            count: pageCount,
            total: (<StyledQueryCount hideParens hideIfEmpty={false} count={modifiedQueryCount} max={queryMaxCount || 100}/>),
        });
        // TODO(workflow): When organization:semver flag is removed add semver tags to tagStore
        if (organization.features.includes('semver') && !tags['release.version']) {
            tags['release.version'] = {
                key: 'release.version',
                name: 'release.version',
            };
            tags['release.build'] = {
                key: 'release.build',
                name: 'release.build',
            };
            tags['release.package'] = {
                key: 'release.package',
                name: 'release.package',
            };
        }
        var projectIds = (_c = selection === null || selection === void 0 ? void 0 : selection.projects) === null || _c === void 0 ? void 0 : _c.map(function (p) { return p.toString(); });
        var orgSlug = organization.slug;
        var showReprocessingTab = this.displayReprocessingTab();
        var displayReprocessingActions = this.displayReprocessingLayout(showReprocessingTab, query);
        return (<React.Fragment>
        <header_1.default organization={organization} query={query} sort={this.getSort()} queryCount={queryCount} queryCounts={queryCounts} realtimeActive={realtimeActive} onRealtimeChange={this.onRealtimeChange} projectIds={projectIds} orgSlug={orgSlug} router={router} savedSearchList={savedSearches} onSavedSearchSelect={this.onSavedSearchSelect} onSavedSearchDelete={this.onSavedSearchDelete} displayReprocessingTab={showReprocessingTab}/>

        <StyledPageContent>
          <StreamContent showSidebar={isSidebarVisible}>
            <filters_1.default organization={organization} query={query} savedSearch={savedSearch} sort={this.getSort()} display={this.getDisplay()} onDisplayChange={this.onDisplayChange} onSortChange={this.onSortChange} onSearch={this.onSearch} onSidebarToggle={this.onSidebarToggle} isSearchDisabled={isSidebarVisible} tagValueLoader={this.tagValueLoader} tags={tags} hasSessions={hasSessions} selectedProjects={selection.projects}/>

            <panels_1.Panel>
              <actions_1.default organization={organization} selection={selection} query={query} queryCount={modifiedQueryCount} displayCount={displayCount} onSelectStatsPeriod={this.onSelectStatsPeriod} onMarkReviewed={this.onMarkReviewed} onDelete={this.onDelete} statsPeriod={this.getGroupStatsPeriod()} groupIds={groupIds} allResultsVisible={this.allResultsVisible()} displayReprocessingActions={displayReprocessingActions}/>
              <panels_1.PanelBody>
                <processingIssueList_1.default organization={organization} projectIds={projectIds} showProject/>
                {this.renderStreamBody()}
              </panels_1.PanelBody>
            </panels_1.Panel>
            <PaginationWrapper>
              {(groupIds === null || groupIds === void 0 ? void 0 : groupIds.length) > 0 && (<div>
                  {/* total includes its own space */}
                  {locale_1.tct('Showing [displayCount] issues', {
                    displayCount: displayCount,
                })}
                </div>)}
              <StyledPagination pageLinks={pageLinks} onCursor={this.onCursorChange}/>
            </PaginationWrapper>
          </StreamContent>

          <SidebarContainer showSidebar={isSidebarVisible}>
            {/* Avoid rendering sidebar until first accessed */}
            {renderSidebar && (<sidebar_1.default loading={tagsLoading} tags={tags} query={query} onQueryChange={this.onIssueListSidebarSearch} tagValueLoader={this.tagValueLoader}/>)}
          </SidebarContainer>
        </StyledPageContent>

        {query === utils_3.Query.FOR_REVIEW && <guideAnchor_1.default target="is_inbox_tab"/>}
      </React.Fragment>);
    };
    return IssueListOverview;
}(React.Component));
exports.IssueListOverview = IssueListOverview;
exports.default = withApi_1.default(withGlobalSelection_1.default(withSavedSearches_1.default(withOrganization_1.default(withIssueTags_1.default(react_1.withProfiler(IssueListOverview))))));
// TODO(workflow): Replace PageContent with thirds body
var StyledPageContent = styled_1.default(organization_1.PageContent)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  background-color: ", ";\n\n  @media (max-width: ", ") {\n    /* Matches thirds layout */\n    padding: ", " ", " 0 ", ";\n  }\n"], ["\n  display: flex;\n  flex-direction: row;\n  background-color: ", ";\n\n  @media (max-width: ", ") {\n    /* Matches thirds layout */\n    padding: ", " ", " 0 ", ";\n  }\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.breakpoints[0]; }, space_1.default(2), space_1.default(2), space_1.default(2));
var StreamContent = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  width: ", ";\n  transition: width 0.2s ease-in-out;\n\n  @media (max-width: ", ") {\n    width: 100%;\n  }\n"], ["\n  width: ", ";\n  transition: width 0.2s ease-in-out;\n\n  @media (max-width: ", ") {\n    width: 100%;\n  }\n"])), function (p) { return (p.showSidebar ? '75%' : '100%'); }, function (p) { return p.theme.breakpoints[0]; });
var SidebarContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: ", ";\n  overflow: ", ";\n  height: ", ";\n  width: ", ";\n  transition: width 0.2s ease-in-out;\n  margin-left: 20px;\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  display: ", ";\n  overflow: ", ";\n  height: ", ";\n  width: ", ";\n  transition: width 0.2s ease-in-out;\n  margin-left: 20px;\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return (p.showSidebar ? 'block' : 'none'); }, function (p) { return (p.showSidebar ? 'visible' : 'hidden'); }, function (p) { return (p.showSidebar ? 'auto' : 0); }, function (p) { return (p.showSidebar ? '25%' : 0); }, function (p) { return p.theme.breakpoints[0]; });
var PaginationWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  font-size: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var StyledPagination = styled_1.default(pagination_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin-top: 0;\n  margin-left: ", ";\n"], ["\n  margin-top: 0;\n  margin-left: ", ";\n"])), space_1.default(2));
var StyledQueryCount = styled_1.default(queryCount_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin-left: 0;\n"], ["\n  margin-left: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=overview.jsx.map