Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var userFeedback_1 = tslib_1.__importDefault(require("app/components/events/userFeedback"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var userFeedbackEmpty_1 = tslib_1.__importDefault(require("app/views/userFeedback/userFeedbackEmpty"));
var utils_1 = require("./utils");
var GroupUserFeedback = /** @class */ (function (_super) {
    tslib_1.__extends(GroupUserFeedback, _super);
    function GroupUserFeedback() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: false,
            reportList: [],
            pageLinks: '',
        };
        _this.fetchData = function () {
            _this.setState({
                loading: true,
                error: false,
            });
            utils_1.fetchGroupUserReports(_this.props.group.id, tslib_1.__assign(tslib_1.__assign({}, _this.props.params), { cursor: _this.props.location.query.cursor || '' }))
                .then(function (_a) {
                var _b = tslib_1.__read(_a, 3), data = _b[0], _ = _b[1], jqXHR = _b[2];
                _this.setState({
                    error: false,
                    loading: false,
                    reportList: data,
                    pageLinks: jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.getResponseHeader('Link'),
                });
            })
                .catch(function () {
                _this.setState({
                    error: true,
                    loading: false,
                });
            });
        };
        return _this;
    }
    GroupUserFeedback.prototype.componentDidMount = function () {
        this.fetchData();
    };
    GroupUserFeedback.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual_1.default(prevProps.params, this.props.params) ||
            prevProps.location.pathname !== this.props.location.pathname ||
            prevProps.location.search !== this.props.location.search) {
            this.fetchData();
        }
    };
    GroupUserFeedback.prototype.render = function () {
        var _a = this.state, reportList = _a.reportList, loading = _a.loading, error = _a.error;
        var _b = this.props, organization = _b.organization, group = _b.group;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        if (error) {
            return <loadingError_1.default onRetry={this.fetchData}/>;
        }
        if (reportList.length) {
            return (<div className="row">
          <div className="col-md-9">
            {reportList.map(function (item, idx) { return (<userFeedback_1.default key={idx} report={item} orgId={organization.slug} issueId={group.id}/>); })}
            <pagination_1.default pageLinks={this.state.pageLinks} {...this.props}/>
          </div>
        </div>);
        }
        return <userFeedbackEmpty_1.default projectIds={[group.project.id]}/>;
    };
    return GroupUserFeedback;
}(react_1.Component));
exports.default = withOrganization_1.default(GroupUserFeedback);
//# sourceMappingURL=groupUserFeedback.jsx.map