Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var queryString = tslib_1.__importStar(require("query-string"));
var groupingActions_1 = tslib_1.__importDefault(require("app/actions/groupingActions"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var groupingStore_1 = tslib_1.__importDefault(require("app/stores/groupingStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var callIfFunction_1 = require("app/utils/callIfFunction");
var list_1 = tslib_1.__importDefault(require("./list"));
var SimilarStackTrace = /** @class */ (function (_super) {
    tslib_1.__extends(SimilarStackTrace, _super);
    function SimilarStackTrace() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            similarItems: [],
            filteredSimilarItems: [],
            similarLinks: null,
            loading: true,
            error: false,
            v2: false,
        };
        _this.onGroupingChange = function (_a) {
            var mergedParent = _a.mergedParent, similarItems = _a.similarItems, similarLinks = _a.similarLinks, filteredSimilarItems = _a.filteredSimilarItems, loading = _a.loading, error = _a.error;
            if (similarItems) {
                _this.setState({
                    similarItems: similarItems,
                    similarLinks: similarLinks,
                    filteredSimilarItems: filteredSimilarItems,
                    loading: loading !== null && loading !== void 0 ? loading : false,
                    error: error !== null && error !== void 0 ? error : false,
                });
                return;
            }
            if (!mergedParent) {
                return;
            }
            if (mergedParent !== _this.props.params.groupId) {
                var params = _this.props.params;
                // Merge success, since we can't specify target, we need to redirect to new parent
                react_router_1.browserHistory.push("/organizations/" + params.orgId + "/issues/" + mergedParent + "/similar/");
                return;
            }
            return;
        };
        _this.listener = groupingStore_1.default.listen(_this.onGroupingChange, undefined);
        _this.handleMerge = function () {
            var _a = _this.props, params = _a.params, location = _a.location;
            var query = location.query;
            if (!params) {
                return;
            }
            // You need at least 1 similarItem OR filteredSimilarItems to be able to merge,
            // so `firstIssue` should always exist from one of those lists.
            //
            // Similar issues API currently does not return issues across projects,
            // so we can assume that the first issues project slug is the project in
            // scope
            var _b = tslib_1.__read(_this.state.similarItems.length
                ? _this.state.similarItems
                : _this.state.filteredSimilarItems, 1), firstIssue = _b[0];
            groupingActions_1.default.merge({
                params: params,
                query: query,
                projectId: firstIssue.issue.project.slug,
            });
        };
        _this.toggleSimilarityVersion = function () {
            _this.setState(function (prevState) { return ({ v2: !prevState.v2 }); }, _this.fetchData);
        };
        return _this;
    }
    SimilarStackTrace.prototype.componentDidMount = function () {
        this.fetchData();
    };
    SimilarStackTrace.prototype.componentWillReceiveProps = function (nextProps) {
        if (nextProps.params.groupId !== this.props.params.groupId ||
            nextProps.location.search !== this.props.location.search) {
            this.fetchData();
        }
    };
    SimilarStackTrace.prototype.componentWillUnmount = function () {
        callIfFunction_1.callIfFunction(this.listener);
    };
    SimilarStackTrace.prototype.fetchData = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        this.setState({ loading: true, error: false });
        var reqs = [];
        if (this.hasSimilarityFeature()) {
            var version = this.state.v2 ? '2' : '1';
            reqs.push({
                endpoint: "/issues/" + params.groupId + "/similar/?" + queryString.stringify(tslib_1.__assign(tslib_1.__assign({}, location.query), { limit: 50, version: version })),
                dataKey: 'similar',
            });
        }
        groupingActions_1.default.fetch(reqs);
    };
    SimilarStackTrace.prototype.hasSimilarityV2Feature = function () {
        return this.props.project.features.includes('similarity-view-v2');
    };
    SimilarStackTrace.prototype.hasSimilarityFeature = function () {
        return this.props.project.features.includes('similarity-view');
    };
    SimilarStackTrace.prototype.render = function () {
        var _a = this.props, params = _a.params, project = _a.project;
        var orgId = params.orgId, groupId = params.groupId;
        var _b = this.state, similarItems = _b.similarItems, filteredSimilarItems = _b.filteredSimilarItems, loading = _b.loading, error = _b.error, v2 = _b.v2, similarLinks = _b.similarLinks;
        var hasV2 = this.hasSimilarityV2Feature();
        var isLoading = loading;
        var isError = error && !isLoading;
        var isLoadedSuccessfully = !isError && !isLoading;
        var hasSimilarItems = this.hasSimilarityFeature() &&
            (similarItems.length >= 0 || filteredSimilarItems.length >= 0) &&
            isLoadedSuccessfully;
        return (<React.Fragment>
        <alert_1.default type="warning">
          {locale_1.t('This is an experimental feature. Data may not be immediately available while we process merges.')}
        </alert_1.default>
        <HeaderWrapper>
          <Title>{locale_1.t('Issues with a similar stack trace')}</Title>
          {hasV2 && (<buttonBar_1.default merged active={v2 ? 'new' : 'old'}>
              <button_1.default barId="old" size="small" onClick={this.toggleSimilarityVersion}>
                {locale_1.t('Old Algorithm')}
              </button_1.default>
              <button_1.default barId="new" size="small" onClick={this.toggleSimilarityVersion}>
                {locale_1.t('New Algorithm')}
              </button_1.default>
            </buttonBar_1.default>)}
        </HeaderWrapper>
        {isLoading && <loadingIndicator_1.default />}
        {isError && (<loadingError_1.default message={locale_1.t('Unable to load similar issues, please try again later')} onRetry={this.fetchData}/>)}
        {hasSimilarItems && (<list_1.default items={similarItems} filteredItems={filteredSimilarItems} onMerge={this.handleMerge} orgId={orgId} project={project} groupId={groupId} pageLinks={similarLinks} v2={v2}/>)}
      </React.Fragment>);
    };
    return SimilarStackTrace;
}(React.Component));
exports.default = SimilarStackTrace;
var Title = styled_1.default('h4')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var HeaderWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), space_1.default(2));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map