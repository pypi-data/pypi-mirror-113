Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var teamStore_1 = tslib_1.__importDefault(require("app/stores/teamStore"));
var badge_1 = tslib_1.__importDefault(require("./badge"));
var TeamBadgeContainer = /** @class */ (function (_super) {
    tslib_1.__extends(TeamBadgeContainer, _super);
    function TeamBadgeContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { team: _this.props.team };
        _this.unlistener = teamStore_1.default.listen(function (team) { return _this.onTeamStoreUpdate(team); }, undefined);
        return _this;
    }
    TeamBadgeContainer.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (this.state.team === nextProps.team) {
            return;
        }
        if (isEqual_1.default(this.state.team, nextProps.team)) {
            return;
        }
        this.setState({ team: nextProps.team });
    };
    TeamBadgeContainer.prototype.componentWillUnmount = function () {
        var _a;
        (_a = this.unlistener) === null || _a === void 0 ? void 0 : _a.call(this);
    };
    TeamBadgeContainer.prototype.onTeamStoreUpdate = function (updatedTeam) {
        if (!updatedTeam.has(this.state.team.id)) {
            return;
        }
        var team = teamStore_1.default.getById(this.state.team.id);
        if (!team || isEqual_1.default(team.avatar, this.state.team.avatar)) {
            return;
        }
        this.setState({ team: team });
    };
    TeamBadgeContainer.prototype.render = function () {
        return <badge_1.default {...this.props} team={this.state.team}/>;
    };
    return TeamBadgeContainer;
}(React.Component));
exports.default = TeamBadgeContainer;
//# sourceMappingURL=index.jsx.map