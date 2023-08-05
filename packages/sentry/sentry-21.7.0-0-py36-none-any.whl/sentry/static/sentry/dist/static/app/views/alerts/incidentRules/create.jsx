Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var analytics_1 = require("app/utils/analytics");
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var constants_1 = require("app/views/alerts/incidentRules/constants");
var ruleForm_1 = tslib_1.__importDefault(require("./ruleForm"));
/**
 * Show metric rules form with an empty rule. Redirects to alerts list after creation.
 */
var IncidentRulesCreate = /** @class */ (function (_super) {
    tslib_1.__extends(IncidentRulesCreate, _super);
    function IncidentRulesCreate() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmitSuccess = function () {
            var router = _this.props.router;
            var orgId = _this.props.params.orgId;
            analytics_1.metric.endTransaction({ name: 'saveAlertRule' });
            router.push("/organizations/" + orgId + "/alerts/rules/");
        };
        return _this;
    }
    IncidentRulesCreate.prototype.render = function () {
        var _a;
        var _b = this.props, project = _b.project, eventView = _b.eventView, wizardTemplate = _b.wizardTemplate, sessionId = _b.sessionId, teams = _b.teams, props = tslib_1.__rest(_b, ["project", "eventView", "wizardTemplate", "sessionId", "teams"]);
        var defaultRule = eventView
            ? constants_1.createRuleFromEventView(eventView)
            : wizardTemplate
                ? constants_1.createRuleFromWizardTemplate(wizardTemplate)
                : constants_1.createDefaultRule();
        var userTeamIds = teams.filter(function (_a) {
            var isMember = _a.isMember;
            return isMember;
        }).map(function (_a) {
            var id = _a.id;
            return id;
        });
        var projectTeamIds = new Set(project.teams.map(function (_a) {
            var id = _a.id;
            return id;
        }));
        var defaultOwnerId = (_a = userTeamIds.find(function (id) { return projectTeamIds.has(id); })) !== null && _a !== void 0 ? _a : null;
        defaultRule.owner = defaultOwnerId && "team:" + defaultOwnerId;
        return (<ruleForm_1.default onSubmitSuccess={this.handleSubmitSuccess} rule={tslib_1.__assign(tslib_1.__assign({}, defaultRule), { projects: [project.slug] })} sessionId={sessionId} project={project} userTeamIds={userTeamIds} {...props}/>);
    };
    return IncidentRulesCreate;
}(react_1.Component));
exports.default = withTeams_1.default(IncidentRulesCreate);
//# sourceMappingURL=create.jsx.map