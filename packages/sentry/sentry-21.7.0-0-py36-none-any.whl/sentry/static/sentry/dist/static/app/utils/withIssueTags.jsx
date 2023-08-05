Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var assign_1 = tslib_1.__importDefault(require("lodash/assign"));
var memberListStore_1 = tslib_1.__importDefault(require("app/stores/memberListStore"));
var tagStore_1 = tslib_1.__importDefault(require("app/stores/tagStore"));
var teamStore_1 = tslib_1.__importDefault(require("app/stores/teamStore"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
var uuidPattern = /[0-9a-f]{32}$/;
var getUsername = function (_a) {
    var isManaged = _a.isManaged, username = _a.username, email = _a.email;
    // Users created via SAML receive unique UUID usernames. Use
    // their email in these cases, instead.
    if (username && uuidPattern.test(username)) {
        return email;
    }
    else {
        return !isManaged && username ? username : email;
    }
};
/**
 * HOC for getting tags and many useful issue attributes as 'tags' for use
 * in autocomplete selectors or condition builders.
 */
function withIssueTags(WrappedComponent) {
    var WithIssueTags = /** @class */ (function (_super) {
        tslib_1.__extends(WithIssueTags, _super);
        function WithIssueTags(props, context) {
            var _this = _super.call(this, props, context) || this;
            _this.unsubscribeMembers = memberListStore_1.default.listen(function (users) {
                _this.setState({ users: users });
                _this.setAssigned();
            }, undefined);
            _this.unsubscribeTeams = teamStore_1.default.listen(function () {
                _this.setState({ teams: teamStore_1.default.getAll() });
                _this.setAssigned();
            }, undefined);
            _this.unsubscribeTags = tagStore_1.default.listen(function (storeTags) {
                var tags = assign_1.default({}, storeTags, tagStore_1.default.getIssueAttributes(), tagStore_1.default.getBuiltInTags());
                _this.setState({ tags: tags });
                _this.setAssigned();
            }, undefined);
            var tags = assign_1.default({}, tagStore_1.default.getAllTags(), tagStore_1.default.getIssueAttributes(), tagStore_1.default.getBuiltInTags());
            var users = memberListStore_1.default.getAll();
            var teams = teamStore_1.default.getAll();
            _this.state = { tags: tags, users: users, teams: teams };
            return _this;
        }
        WithIssueTags.prototype.componentWillUnmount = function () {
            this.unsubscribeMembers();
            this.unsubscribeTeams();
            this.unsubscribeTags();
        };
        WithIssueTags.prototype.setAssigned = function () {
            var _a = this.state, tags = _a.tags, users = _a.users, teams = _a.teams;
            var usernames = users.map(getUsername);
            var teamnames = teams
                .filter(function (team) { return team.isMember; })
                .map(function (team) { return "#" + team.slug; });
            var allAssigned = tslib_1.__spreadArray(['[me, none]'], tslib_1.__read(usernames.concat(teamnames)));
            allAssigned.unshift('me');
            usernames.unshift('me');
            this.setState({
                tags: tslib_1.__assign(tslib_1.__assign({}, tags), { assigned: tslib_1.__assign(tslib_1.__assign({}, tags.assigned), { values: allAssigned }), bookmarks: tslib_1.__assign(tslib_1.__assign({}, tags.bookmarks), { values: usernames }), assigned_or_suggested: tslib_1.__assign(tslib_1.__assign({}, tags.assigned_or_suggested), { values: allAssigned }) }),
            });
        };
        WithIssueTags.prototype.render = function () {
            var _a = this.props, tags = _a.tags, props = tslib_1.__rest(_a, ["tags"]);
            return <WrappedComponent {...tslib_1.__assign({ tags: tags !== null && tags !== void 0 ? tags : this.state.tags }, props)}/>;
        };
        WithIssueTags.displayName = "withIssueTags(" + getDisplayName_1.default(WrappedComponent) + ")";
        return WithIssueTags;
    }(React.Component));
    return WithIssueTags;
}
exports.default = withIssueTags;
//# sourceMappingURL=withIssueTags.jsx.map