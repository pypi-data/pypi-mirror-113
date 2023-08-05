Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var processingIssues_1 = require("app/actionCreators/processingIssues");
var api_1 = require("app/api");
var processingIssueHint_1 = tslib_1.__importDefault(require("app/components/stream/processingIssueHint"));
var defaultProps = {
    showProject: false,
};
var ProcessingIssueList = /** @class */ (function (_super) {
    tslib_1.__extends(ProcessingIssueList, _super);
    function ProcessingIssueList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            issues: [],
        };
        _this.api = new api_1.Client();
        return _this;
    }
    ProcessingIssueList.prototype.componentDidMount = function () {
        this.fetchIssues();
    };
    ProcessingIssueList.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual_1.default(prevProps.projectIds, this.props.projectIds)) {
            this.fetchIssues();
        }
    };
    ProcessingIssueList.prototype.componentWillUnmount = function () {
        this.api.clear();
    };
    ProcessingIssueList.prototype.fetchIssues = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, projectIds = _a.projectIds;
        var promise = processingIssues_1.fetchProcessingIssues(this.api, organization.slug, projectIds);
        promise.then(function (data) {
            var hasIssues = data === null || data === void 0 ? void 0 : data.some(function (p) { return p.hasIssues || p.resolveableIssues > 0 || p.issuesProcessing > 0; });
            if (data && hasIssues) {
                _this.setState({ issues: data });
            }
        }, function () {
            // this is okay. it's just a ui hint
        });
    };
    ProcessingIssueList.prototype.render = function () {
        var issues = this.state.issues;
        var _a = this.props, organization = _a.organization, showProject = _a.showProject;
        return (<react_1.Fragment>
        {issues.map(function (p, idx) { return (<processingIssueHint_1.default key={idx} issue={p} projectId={p.project} orgId={organization.slug} showProject={showProject}/>); })}
      </react_1.Fragment>);
    };
    ProcessingIssueList.defaultProps = defaultProps;
    return ProcessingIssueList;
}(react_1.Component));
exports.default = ProcessingIssueList;
//# sourceMappingURL=processingIssueList.jsx.map