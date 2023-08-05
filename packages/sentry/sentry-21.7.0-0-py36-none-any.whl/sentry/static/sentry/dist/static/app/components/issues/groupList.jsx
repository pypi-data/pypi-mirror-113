Object.defineProperty(exports, "__esModule", { value: true });
exports.GroupList = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var qs = tslib_1.__importStar(require("query-string"));
var members_1 = require("app/actionCreators/members");
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var group_1 = tslib_1.__importStar(require("app/components/stream/group"));
var locale_1 = require("app/locale");
var groupStore_1 = tslib_1.__importDefault(require("app/stores/groupStore"));
var callIfFunction_1 = require("app/utils/callIfFunction");
var streamManager_1 = tslib_1.__importDefault(require("app/utils/streamManager"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var groupListHeader_1 = tslib_1.__importDefault(require("./groupListHeader"));
var defaultProps = {
    canSelectGroups: true,
    withChart: true,
    withPagination: true,
    useFilteredStats: true,
    useTintRow: true,
    narrowGroups: false,
};
var GroupList = /** @class */ (function (_super) {
    tslib_1.__extends(GroupList, _super);
    function GroupList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: false,
            groups: [],
            pageLinks: null,
        };
        _this.listener = groupStore_1.default.listen(function () { return _this.onGroupChange(); }, undefined);
        _this._streamManager = new streamManager_1.default(groupStore_1.default);
        _this.fetchData = function () {
            groupStore_1.default.loadInitialData([]);
            var _a = _this.props, api = _a.api, orgId = _a.orgId;
            api.clear();
            _this.setState({ loading: true, error: false });
            members_1.fetchOrgMembers(api, orgId).then(function (members) {
                _this.setState({ memberList: members_1.indexMembersByProject(members) });
            });
            var endpoint = _this.getGroupListEndpoint();
            api.request(endpoint, {
                success: function (data, _, jqXHR) {
                    var _a;
                    _this._streamManager.push(data);
                    _this.setState({
                        error: false,
                        loading: false,
                        pageLinks: (_a = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : null,
                    }, function () {
                        var _a, _b;
                        (_b = (_a = _this.props).onFetchSuccess) === null || _b === void 0 ? void 0 : _b.call(_a, _this.state, _this.handleCursorChange);
                    });
                },
                error: function (err) {
                    Sentry.captureException(err);
                    _this.setState({ error: true, loading: false });
                },
            });
        };
        return _this;
    }
    GroupList.prototype.componentDidMount = function () {
        this.fetchData();
    };
    GroupList.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        return (!isEqual_1.default(this.state, nextState) ||
            nextProps.endpointPath !== this.props.endpointPath ||
            nextProps.query !== this.props.query ||
            !isEqual_1.default(nextProps.queryParams, this.props.queryParams));
    };
    GroupList.prototype.componentDidUpdate = function (prevProps) {
        var ignoredQueryParams = ['end'];
        if (prevProps.orgId !== this.props.orgId ||
            prevProps.endpointPath !== this.props.endpointPath ||
            prevProps.query !== this.props.query ||
            !isEqual_1.default(omit_1.default(prevProps.queryParams, ignoredQueryParams), omit_1.default(this.props.queryParams, ignoredQueryParams))) {
            this.fetchData();
        }
    };
    GroupList.prototype.componentWillUnmount = function () {
        groupStore_1.default.reset();
        callIfFunction_1.callIfFunction(this.listener);
    };
    GroupList.prototype.getGroupListEndpoint = function () {
        var _a = this.props, orgId = _a.orgId, endpointPath = _a.endpointPath, queryParams = _a.queryParams;
        var path = endpointPath !== null && endpointPath !== void 0 ? endpointPath : "/organizations/" + orgId + "/issues/";
        var queryParameters = queryParams !== null && queryParams !== void 0 ? queryParams : this.getQueryParams();
        return path + "?" + qs.stringify(queryParameters);
    };
    GroupList.prototype.getQueryParams = function () {
        var _a = this.props, location = _a.location, query = _a.query;
        var queryParams = location.query;
        queryParams.limit = 50;
        queryParams.sort = 'new';
        queryParams.query = query;
        return queryParams;
    };
    GroupList.prototype.handleCursorChange = function (cursor, path, query, pageDiff) {
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
        react_router_1.browserHistory.push({
            pathname: path,
            query: tslib_1.__assign(tslib_1.__assign({}, query), { cursor: cursor, page: nextPage }),
        });
    };
    GroupList.prototype.onGroupChange = function () {
        var groups = this._streamManager.getAllItems();
        if (!isEqual_1.default(groups, this.state.groups)) {
            this.setState({ groups: groups });
        }
    };
    GroupList.prototype.render = function () {
        var _a = this.props, canSelectGroups = _a.canSelectGroups, withChart = _a.withChart, renderEmptyMessage = _a.renderEmptyMessage, withPagination = _a.withPagination, useFilteredStats = _a.useFilteredStats, useTintRow = _a.useTintRow, customStatsPeriod = _a.customStatsPeriod, queryParams = _a.queryParams, queryFilterDescription = _a.queryFilterDescription, narrowGroups = _a.narrowGroups;
        var _b = this.state, loading = _b.loading, error = _b.error, groups = _b.groups, memberList = _b.memberList, pageLinks = _b.pageLinks;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        if (error) {
            return <loadingError_1.default onRetry={this.fetchData}/>;
        }
        if (groups.length === 0) {
            if (typeof renderEmptyMessage === 'function') {
                return renderEmptyMessage();
            }
            return (<panels_1.Panel>
          <panels_1.PanelBody>
            <emptyStateWarning_1.default>
              <p>{locale_1.t("There don't seem to be any events fitting the query.")}</p>
            </emptyStateWarning_1.default>
          </panels_1.PanelBody>
        </panels_1.Panel>);
        }
        var statsPeriod = (queryParams === null || queryParams === void 0 ? void 0 : queryParams.groupStatsPeriod) === 'auto'
            ? queryParams === null || queryParams === void 0 ? void 0 : queryParams.groupStatsPeriod
            : group_1.DEFAULT_STREAM_GROUP_STATS_PERIOD;
        return (<React.Fragment>
        <panels_1.Panel>
          <groupListHeader_1.default withChart={!!withChart} narrowGroups={narrowGroups}/>
          <panels_1.PanelBody>
            {groups.map(function (_a) {
                var id = _a.id, project = _a.project;
                var members = (memberList === null || memberList === void 0 ? void 0 : memberList.hasOwnProperty(project.slug))
                    ? memberList[project.slug]
                    : undefined;
                return (<group_1.default key={id} id={id} canSelect={canSelectGroups} withChart={withChart} memberList={members} useFilteredStats={useFilteredStats} useTintRow={useTintRow} customStatsPeriod={customStatsPeriod} statsPeriod={statsPeriod} queryFilterDescription={queryFilterDescription} narrowGroups={narrowGroups}/>);
            })}
          </panels_1.PanelBody>
        </panels_1.Panel>
        {withPagination && (<pagination_1.default pageLinks={pageLinks} onCursor={this.handleCursorChange}/>)}
      </React.Fragment>);
    };
    GroupList.defaultProps = defaultProps;
    return GroupList;
}(React.Component));
exports.GroupList = GroupList;
exports.default = withApi_1.default(react_router_1.withRouter(GroupList));
//# sourceMappingURL=groupList.jsx.map