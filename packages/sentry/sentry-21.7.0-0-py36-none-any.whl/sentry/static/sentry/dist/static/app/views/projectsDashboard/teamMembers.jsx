Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var avatarList_1 = tslib_1.__importDefault(require("app/components/avatar/avatarList"));
var TeamMembers = /** @class */ (function (_super) {
    tslib_1.__extends(TeamMembers, _super);
    function TeamMembers() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TeamMembers.prototype.getEndpoints = function () {
        var _a = this.props, orgId = _a.orgId, teamId = _a.teamId;
        return [['members', "/teams/" + orgId + "/" + teamId + "/members/"]];
    };
    TeamMembers.prototype.renderLoading = function () {
        return this.renderBody();
    };
    TeamMembers.prototype.renderBody = function () {
        var members = this.state.members;
        if (!members) {
            return null;
        }
        var users = members.filter(function (_a) {
            var user = _a.user;
            return !!user;
        }).map(function (_a) {
            var user = _a.user;
            return user;
        });
        return <avatarList_1.default users={users}/>;
    };
    return TeamMembers;
}(asyncComponent_1.default));
exports.default = TeamMembers;
//# sourceMappingURL=teamMembers.jsx.map