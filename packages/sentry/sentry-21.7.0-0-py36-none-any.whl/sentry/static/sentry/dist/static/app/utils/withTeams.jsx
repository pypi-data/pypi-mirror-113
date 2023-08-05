Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var teamStore_1 = tslib_1.__importDefault(require("app/stores/teamStore"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
/**
 * Higher order component that uses TeamStore and provides a list of teams
 */
function withTeams(WrappedComponent) {
    var WithTeams = /** @class */ (function (_super) {
        tslib_1.__extends(WithTeams, _super);
        function WithTeams() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = {
                teams: teamStore_1.default.getAll(),
            };
            _this.unsubscribe = teamStore_1.default.listen(function () { return _this.setState({ teams: teamStore_1.default.getAll() }); }, undefined);
            return _this;
        }
        WithTeams.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithTeams.prototype.render = function () {
            return (<WrappedComponent {...this.props} teams={this.state.teams}/>);
        };
        WithTeams.displayName = "withTeams(" + getDisplayName_1.default(WrappedComponent) + ")";
        return WithTeams;
    }(React.Component));
    return WithTeams;
}
exports.default = withTeams;
//# sourceMappingURL=withTeams.jsx.map