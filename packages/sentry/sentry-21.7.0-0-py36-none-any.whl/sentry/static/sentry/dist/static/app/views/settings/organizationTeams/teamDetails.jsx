Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var indicator_1 = require("app/actionCreators/indicator");
var teams_1 = require("app/actionCreators/teams");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var listLink_1 = tslib_1.__importDefault(require("app/components/links/listLink"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var teamStore_1 = tslib_1.__importDefault(require("app/stores/teamStore"));
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var TeamDetails = /** @class */ (function (_super) {
    tslib_1.__extends(TeamDetails, _super);
    function TeamDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.handleRequestAccess = function () {
            var _a = _this.props, api = _a.api, params = _a.params;
            var team = _this.state.team;
            if (!team) {
                return;
            }
            _this.setState({
                requesting: true,
            });
            teams_1.joinTeam(api, {
                orgId: params.orgId,
                teamId: team.slug,
            }, {
                success: function () {
                    indicator_1.addSuccessMessage(locale_1.tct('You have requested access to [team]', {
                        team: "#" + team.slug,
                    }));
                    _this.setState({
                        requesting: false,
                    });
                },
                error: function () {
                    indicator_1.addErrorMessage(locale_1.tct('Unable to request access to [team]', {
                        team: "#" + team.slug,
                    }));
                    _this.setState({
                        requesting: false,
                    });
                },
            });
        };
        _this.fetchData = function () {
            _this.setState({
                loading: true,
                error: false,
            });
            teams_1.fetchTeamDetails(_this.props.api, _this.props.params);
        };
        _this.onTeamChange = function (data) {
            var team = _this.state.team;
            if (data.slug !== (team === null || team === void 0 ? void 0 : team.slug)) {
                var orgId = _this.props.params.orgId;
                react_router_1.browserHistory.replace("/organizations/" + orgId + "/teams/" + data.slug + "/settings/");
            }
            else {
                _this.setState({
                    team: tslib_1.__assign(tslib_1.__assign({}, team), data),
                });
            }
        };
        return _this;
    }
    TeamDetails.prototype.getInitialState = function () {
        var team = teamStore_1.default.getBySlug(this.props.params.teamId);
        return {
            loading: !teamStore_1.default.initialized,
            error: false,
            requesting: false,
            team: team,
        };
    };
    TeamDetails.prototype.componentDidUpdate = function (prevProps) {
        var params = this.props.params;
        if (prevProps.params.teamId !== params.teamId ||
            prevProps.params.orgId !== params.orgId) {
            this.fetchData();
        }
        if (!isEqual_1.default(this.props.teams, prevProps.teams)) {
            this.setActiveTeam();
        }
    };
    TeamDetails.prototype.setActiveTeam = function () {
        var team = teamStore_1.default.getBySlug(this.props.params.teamId);
        var loading = !teamStore_1.default.initialized;
        var error = !loading && !team;
        this.setState({ team: team, loading: loading, error: error });
    };
    TeamDetails.prototype.render = function () {
        var _a = this.props, params = _a.params, routes = _a.routes, children = _a.children;
        var _b = this.state, team = _b.team, loading = _b.loading, requesting = _b.requesting, error = _b.error;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        if (!team || !team.hasAccess) {
            return (<alert_1.default type="warning">
          {team ? (<RequestAccessWrapper>
              {locale_1.tct('You do not have access to the [teamSlug] team.', {
                        teamSlug: <strong>{"#" + team.slug}</strong>,
                    })}
              <button_1.default disabled={requesting || team.isPending} size="small" onClick={this.handleRequestAccess}>
                {team.isPending ? locale_1.t('Request Pending') : locale_1.t('Request Access')}
              </button_1.default>
            </RequestAccessWrapper>) : (<div>{locale_1.t('You do not have access to this team.')}</div>)}
        </alert_1.default>);
        }
        if (error) {
            return <loadingError_1.default onRetry={this.fetchData}/>;
        }
        var routePrefix = recreateRoute_1.default('', { routes: routes, params: params, stepBack: -1 }); // `/organizations/${orgId}/teams/${teamId}`;
        return (<div>
        <sentryDocumentTitle_1.default title={locale_1.t('Team Details')} orgSlug={params.orgId}/>
        <h3>
          <idBadge_1.default hideAvatar team={team} avatarSize={36}/>
        </h3>

        <navTabs_1.default underlined>
          <listLink_1.default to={routePrefix + "members/"}>{locale_1.t('Members')}</listLink_1.default>
          <listLink_1.default to={routePrefix + "projects/"}>{locale_1.t('Projects')}</listLink_1.default>
          <listLink_1.default to={routePrefix + "settings/"}>{locale_1.t('Settings')}</listLink_1.default>
        </navTabs_1.default>

        {React.isValidElement(children) &&
                React.cloneElement(children, {
                    team: team,
                    onTeamChange: this.onTeamChange,
                })}
      </div>);
    };
    return TeamDetails;
}(React.Component));
exports.default = withApi_1.default(withTeams_1.default(TeamDetails));
var RequestAccessWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"])));
var templateObject_1;
//# sourceMappingURL=teamDetails.jsx.map