Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var organizationAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/organizationAvatar"));
var projectAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/projectAvatar"));
var teamAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/teamAvatar"));
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var Avatar = React.forwardRef(function Avatar(_a, ref) {
    var _b = _a.hasTooltip, hasTooltip = _b === void 0 ? false : _b, user = _a.user, team = _a.team, project = _a.project, organization = _a.organization, props = tslib_1.__rest(_a, ["hasTooltip", "user", "team", "project", "organization"]);
    var commonProps = tslib_1.__assign({ hasTooltip: hasTooltip, forwardedRef: ref }, props);
    if (user) {
        return <userAvatar_1.default user={user} {...commonProps}/>;
    }
    if (team) {
        return <teamAvatar_1.default team={team} {...commonProps}/>;
    }
    if (project) {
        return <projectAvatar_1.default project={project} {...commonProps}/>;
    }
    return <organizationAvatar_1.default organization={organization} {...commonProps}/>;
});
exports.default = Avatar;
//# sourceMappingURL=index.jsx.map