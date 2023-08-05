Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var analytics_1 = require("app/utils/analytics");
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importStar(require("app/utils/withOrganization"));
var groupDetails_1 = tslib_1.__importDefault(require("./groupDetails"));
var OrganizationGroupDetails = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationGroupDetails, _super);
    function OrganizationGroupDetails(props) {
        var _this = _super.call(this, props) || this;
        // Setup in the constructor as render() may be expensive
        _this.startMetricCollection();
        return _this;
    }
    OrganizationGroupDetails.prototype.componentDidMount = function () {
        analytics_1.analytics('issue_page.viewed', {
            group_id: parseInt(this.props.params.groupId, 10),
            org_id: parseInt(this.props.organization.id, 10),
        });
    };
    /**
     * See "page-issue-list-start" for explanation on hot/cold-starts
     */
    OrganizationGroupDetails.prototype.startMetricCollection = function () {
        var startType = withOrganization_1.isLightweightOrganization(this.props.organization)
            ? 'cold-start'
            : 'warm-start';
        analytics_1.metric.mark({ name: 'page-issue-details-start', data: { start_type: startType } });
    };
    OrganizationGroupDetails.prototype.render = function () {
        var _a = this.props, selection = _a.selection, props = tslib_1.__rest(_a, ["selection"]);
        return (<groupDetails_1.default key={this.props.params.groupId + "-envs:" + selection.environments.join(',')} environments={selection.environments} {...props}/>);
    };
    return OrganizationGroupDetails;
}(React.Component));
exports.default = withOrganization_1.default(withGlobalSelection_1.default(OrganizationGroupDetails));
//# sourceMappingURL=index.jsx.map