Object.defineProperty(exports, "__esModule", { value: true });
exports.IssueListContainer = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("app/components/organizations/globalSelectionHeader"));
var analytics_1 = require("app/utils/analytics");
var withOrganization_1 = tslib_1.__importStar(require("app/utils/withOrganization"));
var IssueListContainer = /** @class */ (function (_super) {
    tslib_1.__extends(IssueListContainer, _super);
    function IssueListContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    IssueListContainer.prototype.componentDidMount = function () {
        // Setup here as render() may be expensive
        this.startMetricCollection();
    };
    /**
     * The user can (1) land on IssueList as the first page as they enter Sentry,
     * or (2) navigate into IssueList with the stores preloaded with data.
     *
     * Case (1) will be slower and we can easily identify it as it uses the
     * lightweight organization
     */
    IssueListContainer.prototype.startMetricCollection = function () {
        var isLightWeight = withOrganization_1.isLightweightOrganization(this.props.organization);
        var startType = isLightWeight ? 'cold-start' : 'warm-start';
        analytics_1.metric.mark({ name: 'page-issue-list-start', data: { start_type: startType } });
    };
    IssueListContainer.prototype.getTitle = function () {
        return "Issues - " + this.props.organization.slug + " - Sentry";
    };
    IssueListContainer.prototype.render = function () {
        var _a = this.props, organization = _a.organization, children = _a.children;
        return (<react_document_title_1.default title={this.getTitle()}>
        <globalSelectionHeader_1.default>
          <lightWeightNoProjectMessage_1.default organization={organization}>
            {children}
          </lightWeightNoProjectMessage_1.default>
        </globalSelectionHeader_1.default>
      </react_document_title_1.default>);
    };
    return IssueListContainer;
}(react_1.Component));
exports.IssueListContainer = IssueListContainer;
exports.default = withOrganization_1.default(IssueListContainer);
//# sourceMappingURL=container.jsx.map