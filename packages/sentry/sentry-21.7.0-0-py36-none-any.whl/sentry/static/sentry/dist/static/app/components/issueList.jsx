Object.defineProperty(exports, "__esModule", { value: true });
exports.IssueList = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var compactIssue_1 = tslib_1.__importDefault(require("app/components/issues/compactIssue"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var IssueList = /** @class */ (function (_super) {
    tslib_1.__extends(IssueList, _super);
    function IssueList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.fetchData = function () {
            var _a = _this.props, location = _a.location, api = _a.api, endpoint = _a.endpoint, query = _a.query;
            api.clear();
            api.request(endpoint, {
                method: 'GET',
                query: tslib_1.__assign({ cursor: (location && location.query && location.query.cursor) || '' }, query),
                success: function (data, _, jqXHR) {
                    var _a;
                    _this.setState({
                        data: data,
                        loading: false,
                        error: false,
                        issueIds: data.map(function (item) { return item.id; }),
                        pageLinks: (_a = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : null,
                    });
                },
                error: function () {
                    _this.setState({ loading: false, error: true });
                },
            });
        };
        return _this;
    }
    IssueList.prototype.getInitialState = function () {
        return {
            issueIds: [],
            loading: true,
            error: false,
            pageLinks: null,
            data: [],
        };
    };
    IssueList.prototype.componentWillMount = function () {
        this.fetchData();
    };
    IssueList.prototype.componentWillReceiveProps = function (nextProps) {
        var location = this.props.location;
        var nextLocation = nextProps.location;
        if (!location) {
            return;
        }
        if (location.pathname !== nextLocation.pathname ||
            location.search !== nextLocation.search) {
            this.remountComponent();
        }
    };
    IssueList.prototype.remountComponent = function () {
        this.setState(this.getInitialState(), this.fetchData);
    };
    IssueList.prototype.renderError = function () {
        return (<div style={{ margin: space_1.default(2) + " " + space_1.default(2) + " 0" }}>
        <loadingError_1.default onRetry={this.fetchData}/>
      </div>);
    };
    IssueList.prototype.renderLoading = function () {
        return (<div style={{ margin: '18px 18px 0' }}>
        <loadingIndicator_1.default />
      </div>);
    };
    IssueList.prototype.renderEmpty = function () {
        var emptyText = this.props.emptyText;
        var _a = this.props, noBorder = _a.noBorder, noMargin = _a.noMargin;
        var panelStyle = noBorder ? { border: 0, borderRadius: 0 } : {};
        if (noMargin) {
            panelStyle.marginBottom = 0;
        }
        return (<panels_1.Panel style={panelStyle}>
        <emptyMessage_1.default icon={<icons_1.IconSearch size="xl"/>}>
          {emptyText ? emptyText : locale_1.t('Nothing to show here, move along.')}
        </emptyMessage_1.default>
      </panels_1.Panel>);
    };
    IssueList.prototype.renderResults = function () {
        var _a = this.props, noBorder = _a.noBorder, noMargin = _a.noMargin, renderEmpty = _a.renderEmpty;
        var _b = this.state, loading = _b.loading, error = _b.error, issueIds = _b.issueIds, data = _b.data;
        if (loading) {
            return this.renderLoading();
        }
        if (error) {
            return this.renderError();
        }
        if (issueIds.length > 0) {
            var panelStyle = noBorder
                ? { border: 0, borderRadius: 0 }
                : {};
            if (noMargin) {
                panelStyle.marginBottom = 0;
            }
            return (<panels_1.Panel style={panelStyle}>
          <panels_1.PanelBody className="issue-list">
            {data.map(function (issue) { return (<compactIssue_1.default key={issue.id} id={issue.id} data={issue}/>); })}
          </panels_1.PanelBody>
        </panels_1.Panel>);
        }
        return (renderEmpty === null || renderEmpty === void 0 ? void 0 : renderEmpty()) || this.renderEmpty();
    };
    IssueList.prototype.render = function () {
        var pageLinks = this.state.pageLinks;
        var pagination = this.props.pagination;
        return (<React.Fragment>
        {this.renderResults()}
        {pagination && pageLinks && <pagination_1.default pageLinks={pageLinks} {...this.props}/>}
      </React.Fragment>);
    };
    return IssueList;
}(React.Component));
exports.IssueList = IssueList;
exports.default = react_router_1.withRouter(withApi_1.default(IssueList));
//# sourceMappingURL=issueList.jsx.map