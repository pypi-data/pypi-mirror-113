Object.defineProperty(exports, "__esModule", { value: true });
exports.GroupMergedView = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var queryString = tslib_1.__importStar(require("query-string"));
var groupingActions_1 = tslib_1.__importDefault(require("app/actions/groupingActions"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var groupingStore_1 = tslib_1.__importDefault(require("app/stores/groupingStore"));
var callIfFunction_1 = require("app/utils/callIfFunction");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var mergedList_1 = tslib_1.__importDefault(require("./mergedList"));
var GroupMergedView = /** @class */ (function (_super) {
    tslib_1.__extends(GroupMergedView, _super);
    function GroupMergedView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            mergedItems: [],
            loading: true,
            error: false,
            query: _this.props.location.query.query || '',
        };
        _this.onGroupingChange = function (_a) {
            var mergedItems = _a.mergedItems, mergedLinks = _a.mergedLinks, loading = _a.loading, error = _a.error;
            if (mergedItems) {
                _this.setState({
                    mergedItems: mergedItems,
                    mergedLinks: mergedLinks,
                    loading: typeof loading !== 'undefined' ? loading : false,
                    error: typeof error !== 'undefined' ? error : false,
                });
            }
        };
        _this.listener = groupingStore_1.default.listen(_this.onGroupingChange, undefined);
        _this.fetchData = function () {
            groupingActions_1.default.fetch([
                {
                    endpoint: _this.getEndpoint(),
                    dataKey: 'merged',
                    queryParams: _this.props.location.query,
                },
            ]);
        };
        _this.handleUnmerge = function () {
            groupingActions_1.default.unmerge({
                groupId: _this.props.params.groupId,
                loadingMessage: locale_1.t('Unmerging events\u2026'),
                successMessage: locale_1.t('Events successfully queued for unmerging.'),
                errorMessage: locale_1.t('Unable to queue events for unmerging.'),
            });
        };
        return _this;
    }
    GroupMergedView.prototype.componentDidMount = function () {
        this.fetchData();
    };
    GroupMergedView.prototype.componentWillReceiveProps = function (nextProps) {
        if (nextProps.params.groupId !== this.props.params.groupId ||
            nextProps.location.search !== this.props.location.search) {
            var queryParams = nextProps.location.query;
            this.setState({
                query: queryParams.query,
            }, this.fetchData);
        }
    };
    GroupMergedView.prototype.componentWillUnmount = function () {
        callIfFunction_1.callIfFunction(this.listener);
    };
    GroupMergedView.prototype.getEndpoint = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        var groupId = params.groupId;
        var queryParams = tslib_1.__assign(tslib_1.__assign({}, location.query), { limit: 50, query: this.state.query });
        return "/issues/" + groupId + "/hashes/?" + queryString.stringify(queryParams);
    };
    GroupMergedView.prototype.render = function () {
        var _a = this.props, project = _a.project, params = _a.params;
        var groupId = params.groupId;
        var _b = this.state, isLoading = _b.loading, error = _b.error, mergedItems = _b.mergedItems, mergedLinks = _b.mergedLinks;
        var isError = error && !isLoading;
        var isLoadedSuccessfully = !isError && !isLoading;
        return (<react_1.Fragment>
        <alert_1.default type="warning">
          {locale_1.t('This is an experimental feature. Data may not be immediately available while we process unmerges.')}
        </alert_1.default>

        {isLoading && <loadingIndicator_1.default />}
        {isError && (<loadingError_1.default message={locale_1.t('Unable to load merged events, please try again later')} onRetry={this.fetchData}/>)}

        {isLoadedSuccessfully && (<mergedList_1.default project={project} fingerprints={mergedItems} pageLinks={mergedLinks} groupId={groupId} onUnmerge={this.handleUnmerge} onToggleCollapse={groupingActions_1.default.toggleCollapseFingerprints}/>)}
      </react_1.Fragment>);
    };
    return GroupMergedView;
}(react_1.Component));
exports.GroupMergedView = GroupMergedView;
exports.default = withOrganization_1.default(GroupMergedView);
//# sourceMappingURL=index.jsx.map