Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var uniqBy_1 = tslib_1.__importDefault(require("lodash/uniqBy"));
var memberListStore_1 = tslib_1.__importDefault(require("app/stores/memberListStore"));
var callIfFunction_1 = require("app/utils/callIfFunction");
var isRenderFunc_1 = require("app/utils/isRenderFunc");
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var buildUserId = function (id) { return "user:" + id; };
var buildTeamId = function (id) { return "team:" + id; };
/**
 * Make sure the actionCreator, `fetchOrgMembers`, has been called somewhere
 * higher up the component chain.
 *
 * Will provide a list of users and teams that can be used for @-mentions
 * */
var Mentionables = /** @class */ (function (_super) {
    tslib_1.__extends(Mentionables, _super);
    function Mentionables() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            members: memberListStore_1.default.getAll(),
        };
        _this.listeners = [
            memberListStore_1.default.listen(function (users) {
                _this.handleMemberListUpdate(users);
            }, undefined),
        ];
        _this.handleMemberListUpdate = function (members) {
            if (members === _this.state.members) {
                return;
            }
            _this.setState({
                members: members,
            });
        };
        _this.renderChildren = function (_a) {
            var projects = _a.projects;
            var _b = _this.props, children = _b.children, me = _b.me;
            if (isRenderFunc_1.isRenderFunc(children)) {
                return children({
                    members: _this.getMemberList(_this.state.members, me),
                    teams: _this.getTeams(projects),
                });
            }
            return null;
        };
        return _this;
    }
    Mentionables.prototype.componentWillUnmount = function () {
        this.listeners.forEach(callIfFunction_1.callIfFunction);
    };
    Mentionables.prototype.getMemberList = function (memberList, sessionUser) {
        var members = uniqBy_1.default(memberList, function (_a) {
            var id = _a.id;
            return id;
        }).filter(function (_a) {
            var id = _a.id;
            return !sessionUser || sessionUser.id !== id;
        });
        return members.map(function (member) { return ({
            id: buildUserId(member.id),
            display: member.name,
            email: member.email,
        }); });
    };
    Mentionables.prototype.getTeams = function (projects) {
        var uniqueTeams = uniqBy_1.default(projects
            .map(function (_a) {
            var teams = _a.teams;
            return teams;
        })
            .reduce(function (acc, teams) { return acc.concat(teams || []); }, []), 'id');
        return uniqueTeams.map(function (team) { return ({
            id: buildTeamId(team.id),
            display: "#" + team.slug,
            email: team.id,
        }); });
    };
    Mentionables.prototype.render = function () {
        var _a = this.props, organization = _a.organization, projectSlugs = _a.projectSlugs;
        if (!projectSlugs || !projectSlugs.length) {
            return this.renderChildren({ projects: [] });
        }
        return (<projects_1.default slugs={projectSlugs} orgId={organization.slug}>
        {this.renderChildren}
      </projects_1.default>);
    };
    return Mentionables;
}(React.PureComponent));
exports.default = withOrganization_1.default(Mentionables);
//# sourceMappingURL=mentionables.jsx.map