Object.defineProperty(exports, "__esModule", { value: true });
exports.OrganizationTeamsContainer = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var projects_1 = require("app/actionCreators/projects");
var utils_1 = require("app/utils");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var organizationTeams_1 = tslib_1.__importDefault(require("./organizationTeams"));
var OrganizationTeamsContainer = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationTeamsContainer, _super);
    function OrganizationTeamsContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationTeamsContainer.prototype.componentDidMount = function () {
        this.fetchStats();
    };
    OrganizationTeamsContainer.prototype.fetchStats = function () {
        projects_1.loadStats(this.props.api, {
            orgId: this.props.params.orgId,
            query: {
                since: (new Date().getTime() / 1000 - 3600 * 24).toString(),
                stat: 'generated',
                group: 'project',
            },
        });
    };
    OrganizationTeamsContainer.prototype.render = function () {
        var _a = this.props, organization = _a.organization, teams = _a.teams;
        if (!organization) {
            return null;
        }
        var allTeams = utils_1.sortArray(teams, function (team) { return team.name; });
        var activeTeams = allTeams.filter(function (team) { return team.isMember; });
        return (<organizationTeams_1.default {...this.props} access={new Set(organization.access)} features={new Set(organization.features)} organization={organization} allTeams={allTeams} activeTeams={activeTeams}/>);
    };
    return OrganizationTeamsContainer;
}(react_1.Component));
exports.OrganizationTeamsContainer = OrganizationTeamsContainer;
exports.default = withApi_1.default(withOrganization_1.default(withTeams_1.default(OrganizationTeamsContainer)));
//# sourceMappingURL=index.jsx.map