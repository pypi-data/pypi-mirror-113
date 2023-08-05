Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var memberBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/memberBadge"));
var organizationBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/organizationBadge"));
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var badge_1 = tslib_1.__importDefault(require("app/components/idBadge/teamBadge/badge"));
var userBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/userBadge"));
function getBadge(_a) {
    var organization = _a.organization, team = _a.team, project = _a.project, user = _a.user, member = _a.member, props = tslib_1.__rest(_a, ["organization", "team", "project", "user", "member"]);
    if (organization) {
        return <organizationBadge_1.default organization={organization} {...props}/>;
    }
    if (team) {
        return <badge_1.default team={team} {...props}/>;
    }
    if (project) {
        return <projectBadge_1.default project={project} {...props}/>;
    }
    if (user) {
        return <userBadge_1.default user={user} {...props}/>;
    }
    if (member) {
        return <memberBadge_1.default member={member} {...props}/>;
    }
    return null;
}
exports.default = getBadge;
//# sourceMappingURL=getBadge.jsx.map