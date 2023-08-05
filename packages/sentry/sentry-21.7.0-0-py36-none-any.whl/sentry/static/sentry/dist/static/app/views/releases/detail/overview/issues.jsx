Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var qs = tslib_1.__importStar(require("query-string"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var button_1 = tslib_1.__importStar(require("app/components/button"));
var buttonBar_1 = tslib_1.__importStar(require("app/components/buttonBar"));
var discoverButton_1 = tslib_1.__importDefault(require("app/components/discoverButton"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var groupList_1 = tslib_1.__importDefault(require("app/components/issues/groupList"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var queryCount_1 = tslib_1.__importDefault(require("app/components/queryCount"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var utils_1 = require("app/views/issueList/utils");
var utils_2 = require("../../utils");
var emptyState_1 = tslib_1.__importDefault(require("../emptyState"));
var utils_3 = require("./chart/utils");
var IssuesType;
(function (IssuesType) {
    IssuesType["NEW"] = "new";
    IssuesType["UNHANDLED"] = "unhandled";
    IssuesType["RESOLVED"] = "resolved";
    IssuesType["ALL"] = "all";
})(IssuesType || (IssuesType = {}));
var IssuesQuery;
(function (IssuesQuery) {
    IssuesQuery["NEW"] = "first-release";
    IssuesQuery["UNHANDLED"] = "error.handled:0";
    IssuesQuery["RESOLVED"] = "is:resolved";
    IssuesQuery["ALL"] = "release";
})(IssuesQuery || (IssuesQuery = {}));
var defaultProps = {
    withChart: false,
};
var Issues = /** @class */ (function (_super) {
    tslib_1.__extends(Issues, _super);
    function Issues() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.handleIssuesTypeSelection = function (issuesType) {
            var location = _this.props.location;
            var issuesTypeQuery = issuesType === IssuesType.ALL
                ? IssuesType.ALL
                : issuesType === IssuesType.NEW
                    ? IssuesType.NEW
                    : issuesType === IssuesType.RESOLVED
                        ? IssuesType.RESOLVED
                        : issuesType === IssuesType.UNHANDLED
                            ? IssuesType.UNHANDLED
                            : '';
            var to = tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { issuesType: issuesTypeQuery }) });
            react_router_1.browserHistory.replace(to);
            _this.setState({ issuesType: issuesType });
        };
        _this.handleFetchSuccess = function (groupListState, onCursor) {
            _this.setState({ pageLinks: groupListState.pageLinks, onCursor: onCursor });
        };
        _this.renderEmptyMessage = function () {
            var _a = _this.props, location = _a.location, releaseBounds = _a.releaseBounds, defaultStatsPeriod = _a.defaultStatsPeriod, organization = _a.organization;
            var issuesType = _this.state.issuesType;
            var hasReleaseComparison = organization.features.includes('release-comparison');
            var isEntireReleasePeriod = hasReleaseComparison &&
                !location.query.pageStatsPeriod &&
                !location.query.pageStart;
            var statsPeriod = utils_2.getReleaseParams({
                location: location,
                releaseBounds: releaseBounds,
                defaultStatsPeriod: defaultStatsPeriod,
                allowEmptyPeriod: hasReleaseComparison,
            }).statsPeriod;
            var selectedTimePeriod = statsPeriod ? constants_1.DEFAULT_RELATIVE_PERIODS[statsPeriod] : null;
            var displayedPeriod = selectedTimePeriod
                ? selectedTimePeriod.toLowerCase()
                : locale_1.t('given timeframe');
            return (<emptyState_1.default>
        {issuesType === IssuesType.NEW
                    ? isEntireReleasePeriod
                        ? locale_1.t('No new issues in this release.')
                        : locale_1.tct('No new issues for the [timePeriod].', {
                            timePeriod: displayedPeriod,
                        })
                    : null}
        {issuesType === IssuesType.UNHANDLED
                    ? isEntireReleasePeriod
                        ? locale_1.t('No unhandled issues in this release.')
                        : locale_1.tct('No unhandled issues for the [timePeriod].', {
                            timePeriod: displayedPeriod,
                        })
                    : null}
        {issuesType === IssuesType.RESOLVED && locale_1.t('No resolved issues in this release.')}
        {issuesType === IssuesType.ALL
                    ? isEntireReleasePeriod
                        ? locale_1.t('No issues in this release')
                        : locale_1.tct('No issues for the [timePeriod].', {
                            timePeriod: displayedPeriod,
                        })
                    : null}
      </emptyState_1.default>);
        };
        return _this;
    }
    Issues.prototype.getInitialState = function () {
        var location = this.props.location;
        var query = location.query ? location.query.issuesType : null;
        var issuesTypeState = !query
            ? IssuesType.NEW
            : query.includes(IssuesType.NEW)
                ? IssuesType.NEW
                : query.includes(IssuesType.UNHANDLED)
                    ? IssuesType.UNHANDLED
                    : query.includes(IssuesType.RESOLVED)
                        ? IssuesType.RESOLVED
                        : query.includes(IssuesType.ALL)
                            ? IssuesType.ALL
                            : IssuesType.ALL;
        return {
            issuesType: issuesTypeState,
            count: {
                new: null,
                all: null,
                resolved: null,
                unhandled: null,
            },
        };
    };
    Issues.prototype.componentDidMount = function () {
        this.fetchIssuesCount();
    };
    Issues.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual_1.default(utils_2.getReleaseParams({
            location: this.props.location,
            releaseBounds: this.props.releaseBounds,
            defaultStatsPeriod: this.props.defaultStatsPeriod,
            allowEmptyPeriod: this.props.organization.features.includes('release-comparison'),
        }), utils_2.getReleaseParams({
            location: prevProps.location,
            releaseBounds: prevProps.releaseBounds,
            defaultStatsPeriod: prevProps.defaultStatsPeriod,
            allowEmptyPeriod: prevProps.organization.features.includes('release-comparison'),
        }))) {
            this.fetchIssuesCount();
        }
    };
    Issues.prototype.getDiscoverUrl = function () {
        var _a = this.props, version = _a.version, organization = _a.organization, selection = _a.selection;
        var discoverView = utils_3.getReleaseEventView(selection, version);
        return discoverView.getResultsViewUrlTarget(organization.slug);
    };
    Issues.prototype.getIssuesUrl = function () {
        var _a = this.props, version = _a.version, organization = _a.organization;
        var issuesType = this.state.issuesType;
        var queryParams = this.getIssuesEndpoint().queryParams;
        var query = new tokenizeSearch_1.QueryResults([]);
        switch (issuesType) {
            case IssuesType.NEW:
                query.setTagValues('firstRelease', [version]);
                break;
            case IssuesType.UNHANDLED:
                query.setTagValues('release', [version]);
                query.setTagValues('error.handled', ['0']);
                break;
            case IssuesType.RESOLVED:
            case IssuesType.ALL:
            default:
                query.setTagValues('release', [version]);
        }
        return {
            pathname: "/organizations/" + organization.slug + "/issues/",
            query: tslib_1.__assign(tslib_1.__assign({}, queryParams), { limit: undefined, cursor: undefined, query: query.formatString() }),
        };
    };
    Issues.prototype.getIssuesEndpoint = function () {
        var _a = this.props, version = _a.version, organization = _a.organization, location = _a.location, defaultStatsPeriod = _a.defaultStatsPeriod, releaseBounds = _a.releaseBounds;
        var issuesType = this.state.issuesType;
        var queryParams = tslib_1.__assign(tslib_1.__assign({}, utils_2.getReleaseParams({
            location: location,
            releaseBounds: releaseBounds,
            defaultStatsPeriod: defaultStatsPeriod,
            allowEmptyPeriod: organization.features.includes('release-comparison'),
        })), { limit: 10, sort: utils_1.IssueSortOptions.FREQ, groupStatsPeriod: 'auto' });
        switch (issuesType) {
            case IssuesType.ALL:
                return {
                    path: "/organizations/" + organization.slug + "/issues/",
                    queryParams: tslib_1.__assign(tslib_1.__assign({}, queryParams), { query: new tokenizeSearch_1.QueryResults([IssuesQuery.ALL + ":" + version]).formatString() }),
                };
            case IssuesType.RESOLVED:
                return {
                    path: "/organizations/" + organization.slug + "/releases/" + version + "/resolved/",
                    queryParams: tslib_1.__assign(tslib_1.__assign({}, queryParams), { query: '' }),
                };
            case IssuesType.UNHANDLED:
                return {
                    path: "/organizations/" + organization.slug + "/issues/",
                    queryParams: tslib_1.__assign(tslib_1.__assign({}, queryParams), { query: new tokenizeSearch_1.QueryResults([
                            IssuesQuery.ALL + ":" + version,
                            IssuesQuery.UNHANDLED,
                        ]).formatString() }),
                };
            case IssuesType.NEW:
            default:
                return {
                    path: "/organizations/" + organization.slug + "/issues/",
                    queryParams: tslib_1.__assign(tslib_1.__assign({}, queryParams), { query: new tokenizeSearch_1.QueryResults([IssuesQuery.NEW + ":" + version]).formatString() }),
                };
        }
    };
    Issues.prototype.fetchIssuesCount = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, organization, version, issueCountEndpoint, resolvedEndpoint, _b;
            var _this = this;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, version = _a.version;
                        issueCountEndpoint = this.getIssueCountEndpoint();
                        resolvedEndpoint = "/organizations/" + organization.slug + "/releases/" + version + "/resolved/";
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, Promise.all([
                                api.requestPromise(issueCountEndpoint),
                                api.requestPromise(resolvedEndpoint),
                            ]).then(function (_a) {
                                var _b = tslib_1.__read(_a, 2), issueResponse = _b[0], resolvedResponse = _b[1];
                                _this.setState({
                                    count: {
                                        all: issueResponse[IssuesQuery.ALL + ":" + version] || 0,
                                        new: issueResponse[IssuesQuery.NEW + ":" + version] || 0,
                                        resolved: resolvedResponse.length,
                                        unhandled: issueResponse[IssuesQuery.UNHANDLED + " " + IssuesQuery.ALL + ":" + version] ||
                                            0,
                                    },
                                });
                            })];
                    case 2:
                        _c.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    Issues.prototype.getIssueCountEndpoint = function () {
        var _a = this.props, organization = _a.organization, version = _a.version, location = _a.location, releaseBounds = _a.releaseBounds, defaultStatsPeriod = _a.defaultStatsPeriod;
        var issuesCountPath = "/organizations/" + organization.slug + "/issues-count/";
        var params = [
            IssuesQuery.NEW + ":" + version,
            IssuesQuery.ALL + ":" + version,
            IssuesQuery.UNHANDLED + " " + IssuesQuery.ALL + ":" + version,
        ];
        var queryParams = params.map(function (param) { return param; });
        var queryParameters = tslib_1.__assign(tslib_1.__assign({}, utils_2.getReleaseParams({
            location: location,
            releaseBounds: releaseBounds,
            defaultStatsPeriod: defaultStatsPeriod,
            allowEmptyPeriod: organization.features.includes('release-comparison'),
        })), { query: queryParams });
        return issuesCountPath + "?" + qs.stringify(queryParameters);
    };
    Issues.prototype.render = function () {
        var _this = this;
        var _a = this.state, issuesType = _a.issuesType, count = _a.count, pageLinks = _a.pageLinks, onCursor = _a.onCursor;
        var _b = this.props, organization = _b.organization, queryFilterDescription = _b.queryFilterDescription, withChart = _b.withChart;
        var _c = this.getIssuesEndpoint(), path = _c.path, queryParams = _c.queryParams;
        var hasReleaseComparison = organization.features.includes('release-comparison');
        var issuesTypes = [
            { value: IssuesType.ALL, label: locale_1.t('All Issues'), issueCount: count.all },
            { value: IssuesType.NEW, label: locale_1.t('New Issues'), issueCount: count.new },
            {
                value: IssuesType.UNHANDLED,
                label: locale_1.t('Unhandled Issues'),
                issueCount: count.unhandled,
            },
            {
                value: IssuesType.RESOLVED,
                label: locale_1.t('Resolved Issues'),
                issueCount: count.resolved,
            },
        ];
        return (<react_1.Fragment>
        <ControlsWrapper>
          {hasReleaseComparison ? (<StyledButtonBar active={issuesType} merged>
              {issuesTypes.map(function (_a) {
                    var value = _a.value, label = _a.label, issueCount = _a.issueCount;
                    return (<button_1.default key={value} barId={value} size="small" onClick={function () { return _this.handleIssuesTypeSelection(value); }}>
                  {label}
                  <queryCount_1.default count={issueCount} max={99} hideParens hideIfEmpty={false}/>
                </button_1.default>);
                })}
            </StyledButtonBar>) : (<dropdownControl_1.default button={function (_a) {
                    var _b;
                    var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
                    return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} prefix={locale_1.t('Filter')} size="small">
                  {(_b = issuesTypes.find(function (i) { return i.value === issuesType; })) === null || _b === void 0 ? void 0 : _b.label}
                </StyledDropdownButton>);
                }}>
              {issuesTypes.map(function (_a) {
                    var value = _a.value, label = _a.label;
                    return (<StyledDropdownItem key={value} onSelect={_this.handleIssuesTypeSelection} data-test-id={"filter-" + value} eventKey={value} isActive={value === issuesType}>
                  {label}
                </StyledDropdownItem>);
                })}
            </dropdownControl_1.default>)}

          <OpenInButtonBar gap={1}>
            <button_1.default to={this.getIssuesUrl()} size="small" data-test-id="issues-button">
              {locale_1.t('Open in Issues')}
            </button_1.default>

            {!hasReleaseComparison && (<guideAnchor_1.default target="release_issues_open_in_discover">
                <discoverButton_1.default to={this.getDiscoverUrl()} size="small" data-test-id="discover-button">
                  {locale_1.t('Open in Discover')}
                </discoverButton_1.default>
              </guideAnchor_1.default>)}
            {!hasReleaseComparison && (<StyledPagination pageLinks={pageLinks} onCursor={onCursor}/>)}
          </OpenInButtonBar>
        </ControlsWrapper>
        <div data-test-id="release-wrapper">
          <groupList_1.default orgId={organization.slug} endpointPath={path} queryParams={queryParams} query="" canSelectGroups={false} queryFilterDescription={queryFilterDescription} withChart={withChart} narrowGroups renderEmptyMessage={this.renderEmptyMessage} withPagination={false} onFetchSuccess={this.handleFetchSuccess}/>
        </div>
      </react_1.Fragment>);
    };
    Issues.defaultProps = defaultProps;
    return Issues;
}(react_1.Component));
var ControlsWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n    ", " {\n      overflow: auto;\n    }\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n    ", " {\n      overflow: auto;\n    }\n  }\n"])), space_1.default(1), function (p) { return p.theme.breakpoints[0]; }, buttonBar_1.ButtonGrid);
var OpenInButtonBar = styled_1.default(buttonBar_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"], ["\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space_1.default(1));
var StyledButtonBar = styled_1.default(buttonBar_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: repeat(4, 1fr);\n  ", " {\n    white-space: nowrap;\n    grid-gap: ", ";\n    span:last-child {\n      color: ", ";\n    }\n  }\n  .active {\n    ", " {\n      span:last-child {\n        color: ", ";\n      }\n    }\n  }\n"], ["\n  grid-template-columns: repeat(4, 1fr);\n  ", " {\n    white-space: nowrap;\n    grid-gap: ", ";\n    span:last-child {\n      color: ", ";\n    }\n  }\n  .active {\n    ", " {\n      span:last-child {\n        color: ", ";\n      }\n    }\n  }\n"])), button_1.ButtonLabel, space_1.default(0.5), function (p) { return p.theme.buttonCount; }, button_1.ButtonLabel, function (p) { return p.theme.buttonCountActive; });
var StyledDropdownButton = styled_1.default(dropdownButton_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  min-width: 145px;\n"], ["\n  min-width: 145px;\n"])));
var StyledDropdownItem = styled_1.default(dropdownControl_1.DropdownItem)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
var StyledPagination = styled_1.default(pagination_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
exports.default = withApi_1.default(withOrganization_1.default(Issues));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=issues.jsx.map