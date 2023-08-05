Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
var getProjectsByTeams_1 = tslib_1.__importDefault(require("app/utils/getProjectsByTeams"));
var analytics_1 = require("./analytics");
var withTeamsForUser = function (WrappedComponent) { var _a; return _a = /** @class */ (function (_super) {
        tslib_1.__extends(class_1, _super);
        function class_1() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = {
                teams: [],
                loadingTeams: true,
                error: null,
            };
            return _this;
        }
        class_1.prototype.componentDidMount = function () {
            this.fetchTeams();
        };
        class_1.prototype.fetchTeams = function () {
            return tslib_1.__awaiter(this, void 0, void 0, function () {
                var teamsWithProjects, error_1;
                var _this = this;
                return tslib_1.__generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            this.setState({
                                loadingTeams: true,
                            });
                            _a.label = 1;
                        case 1:
                            _a.trys.push([1, 3, , 4]);
                            analytics_1.metric.mark({ name: 'user-teams-fetch-start' });
                            return [4 /*yield*/, this.props.api.requestPromise(this.getUsersTeamsEndpoint())];
                        case 2:
                            teamsWithProjects = _a.sent();
                            this.setState({
                                teams: teamsWithProjects,
                                loadingTeams: false,
                            }, function () {
                                analytics_1.metric.measure({
                                    name: 'app.component.perf',
                                    start: 'user-teams-fetch-start',
                                    data: {
                                        name: 'user-teams',
                                        route: '/organizations/:orgid/user-teams',
                                        organization_id: parseInt(_this.props.organization.id, 10),
                                    },
                                });
                            });
                            return [3 /*break*/, 4];
                        case 3:
                            error_1 = _a.sent();
                            this.setState({
                                error: error_1,
                                loadingTeams: false,
                            });
                            return [3 /*break*/, 4];
                        case 4: return [2 /*return*/];
                    }
                });
            });
        };
        class_1.prototype.populateTeamsWithProjects = function (teams, projects) {
            var isSuperuser = configStore_1.default.get('user').isSuperuser;
            var projectsByTeam = getProjectsByTeams_1.default(teams, projects, isSuperuser).projectsByTeam;
            var teamsWithProjects = teams.map(function (team) {
                var teamProjects = projectsByTeam[team.slug] || [];
                return tslib_1.__assign(tslib_1.__assign({}, team), { projects: teamProjects });
            });
            this.setState({
                teams: teamsWithProjects,
                loadingTeams: false,
            });
        };
        class_1.prototype.getUsersTeamsEndpoint = function () {
            return "/organizations/" + this.props.organization.slug + "/user-teams/";
        };
        class_1.prototype.render = function () {
            return <WrappedComponent {...this.props} {...this.state}/>;
        };
        return class_1;
    }(React.Component)),
    _a.displayName = "withUsersTeams(" + getDisplayName_1.default(WrappedComponent) + ")",
    _a; };
exports.default = withTeamsForUser;
//# sourceMappingURL=withTeamsForUser.jsx.map