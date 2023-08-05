Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var analytics_1 = require("app/utils/analytics");
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var ruleForm_1 = tslib_1.__importDefault(require("app/views/alerts/incidentRules/ruleForm"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var IncidentRulesDetails = /** @class */ (function (_super) {
    tslib_1.__extends(IncidentRulesDetails, _super);
    function IncidentRulesDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmitSuccess = function () {
            var router = _this.props.router;
            var orgId = _this.props.params.orgId;
            analytics_1.metric.endTransaction({ name: 'saveAlertRule' });
            router.push("/organizations/" + orgId + "/alerts/rules/");
        };
        return _this;
    }
    IncidentRulesDetails.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { actions: new Map() });
    };
    IncidentRulesDetails.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, ruleId = _a.ruleId;
        return [['rule', "/organizations/" + orgId + "/alert-rules/" + ruleId + "/"]];
    };
    IncidentRulesDetails.prototype.onRequestSuccess = function (_a) {
        var stateKey = _a.stateKey, data = _a.data;
        if (stateKey === 'rule' && data.name) {
            this.props.onChangeTitle(data.name);
        }
    };
    IncidentRulesDetails.prototype.renderBody = function () {
        var teams = this.props.teams;
        var ruleId = this.props.params.ruleId;
        var rule = this.state.rule;
        var userTeamIds = teams.filter(function (_a) {
            var isMember = _a.isMember;
            return isMember;
        }).map(function (_a) {
            var id = _a.id;
            return id;
        });
        return (<ruleForm_1.default {...this.props} ruleId={ruleId} rule={rule} onSubmitSuccess={this.handleSubmitSuccess} userTeamIds={userTeamIds}/>);
    };
    return IncidentRulesDetails;
}(asyncView_1.default));
exports.default = withTeams_1.default(IncidentRulesDetails);
//# sourceMappingURL=details.jsx.map