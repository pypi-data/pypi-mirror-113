Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var groupListHeader_1 = tslib_1.__importDefault(require("app/components/issues/groupListHeader"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var group_1 = tslib_1.__importDefault(require("app/components/stream/group"));
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var locale_1 = require("app/locale");
var groupStore_1 = tslib_1.__importDefault(require("app/stores/groupStore"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var List = /** @class */ (function (_super) {
    tslib_1.__extends(List, _super);
    function List() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            groups: [],
            hasError: false,
            isLoading: true,
        };
        _this.getGroups = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, orgSlug, location, issues, issuesIds, groups, convertedGroups, error_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, orgSlug = _a.orgSlug, location = _a.location, issues = _a.issues;
                        if (!issues.length) {
                            this.setState({ isLoading: false });
                            return [2 /*return*/];
                        }
                        issuesIds = issues.map(function (issue) { return "group=" + issue['issue.id']; }).join('&');
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/organizations/" + orgSlug + "/issues/?" + issuesIds, {
                                method: 'GET',
                                data: tslib_1.__assign({ sort: 'new' }, pick_1.default(location.query, tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(Object.values(globalSelectionHeader_1.URL_PARAM))), ['cursor']))),
                            })];
                    case 2:
                        groups = _b.sent();
                        convertedGroups = this.convertGroupsIntoEventFormat(groups);
                        // this is necessary, because the AssigneeSelector component fetches the group from the GroupStore
                        groupStore_1.default.add(convertedGroups);
                        this.setState({ groups: convertedGroups, isLoading: false });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        Sentry.captureException(error_1);
                        this.setState({ isLoading: false, hasError: true });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        // this little hack is necessary until we factored the groupStore or the EventOrGroupHeader component
        // the goal of this function is to insert the properties eventID and groupID, so then the link rendered
        // in the EventOrGroupHeader component will always have the structure '/organization/:orgSlug/issues/:groupId/event/:eventId/',
        // providing a smooth navigation between issues with the same trace ID
        _this.convertGroupsIntoEventFormat = function (groups) {
            var issues = _this.props.issues;
            return groups
                .map(function (group) {
                // the issue must always be found
                var foundIssue = issues.find(function (issue) { return group.id === String(issue['issue.id']); });
                if (foundIssue) {
                    // the eventID is the reason why we need to use the DiscoverQuery component.
                    // At the moment the /issues/ endpoint above doesn't return this information
                    return tslib_1.__assign(tslib_1.__assign({}, group), { eventID: foundIssue.id, groupID: group.id });
                }
                return undefined;
            })
                .filter(function (event) { return !!event; });
        };
        _this.handleRetry = function () {
            _this.getGroups();
        };
        _this.renderContent = function () {
            var _a = _this.props, issues = _a.issues, period = _a.period, traceID = _a.traceID;
            if (!issues.length) {
                return (<emptyStateWarning_1.default small withIcon={false}>
          {locale_1.tct('No issues with the same trace ID [traceID] were found in the period between [start] and [end]', {
                        traceID: traceID,
                        start: <dateTime_1.default date={period.start} timeAndDate/>,
                        end: <dateTime_1.default date={period.start} timeAndDate/>,
                    })}
        </emptyStateWarning_1.default>);
            }
            return issues.map(function (issue) { return (<group_1.default key={issue.id} id={String(issue['issue.id'])} canSelect={false} withChart={false}/>); });
        };
        return _this;
    }
    List.prototype.componentDidMount = function () {
        this.getGroups();
    };
    List.prototype.handleCursorChange = function (cursor, path, query, pageDiff) {
        react_router_1.browserHistory.push({
            pathname: path,
            query: tslib_1.__assign(tslib_1.__assign({}, query), { cursor: pageDiff <= 0 ? undefined : cursor }),
        });
    };
    List.prototype.render = function () {
        var _a = this.props, pageLinks = _a.pageLinks, traceID = _a.traceID;
        var _b = this.state, isLoading = _b.isLoading, hasError = _b.hasError;
        if (isLoading) {
            return <loadingIndicator_1.default />;
        }
        if (hasError) {
            return (<loadingError_1.default message={locale_1.tct('An error occurred while fetching issues with the trace ID [traceID]', {
                    traceID: traceID,
                })} onRetry={this.handleRetry}/>);
        }
        return (<react_1.Fragment>
        <StyledPanel>
          <groupListHeader_1.default withChart={false}/>
          <panels_1.PanelBody>{this.renderContent()}</panels_1.PanelBody>
        </StyledPanel>
        <StyledPagination pageLinks={pageLinks} onCursor={this.handleCursorChange}/>
      </react_1.Fragment>);
    };
    return List;
}(react_1.Component));
exports.default = withApi_1.default(List);
var StyledPagination = styled_1.default(pagination_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-top: 0;\n"], ["\n  margin-top: 0;\n"])));
var StyledPanel = styled_1.default(panels_1.Panel)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=list.jsx.map