Object.defineProperty(exports, "__esModule", { value: true });
exports.AllTeamsRow = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var teams_1 = require("app/actionCreators/teams");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var AllTeamsRow = /** @class */ (function (_super) {
    tslib_1.__extends(AllTeamsRow, _super);
    function AllTeamsRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
            error: false,
        };
        _this.handleRequestAccess = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var team;
            return tslib_1.__generator(this, function (_a) {
                team = this.props.team;
                try {
                    this.joinTeam({
                        successMessage: locale_1.tct('You have requested access to [team]', {
                            team: "#" + team.slug,
                        }),
                        errorMessage: locale_1.tct('Unable to request access to [team]', {
                            team: "#" + team.slug,
                        }),
                    });
                    // TODO: Ideally we would update team so that `isPending` is true
                }
                catch (_err) {
                    // No need to do anything
                }
                return [2 /*return*/];
            });
        }); };
        _this.handleJoinTeam = function () {
            var team = _this.props.team;
            _this.joinTeam({
                successMessage: locale_1.tct('You have joined [team]', {
                    team: "#" + team.slug,
                }),
                errorMessage: locale_1.tct('Unable to join [team]', {
                    team: "#" + team.slug,
                }),
            });
        };
        _this.joinTeam = function (_a) {
            var successMessage = _a.successMessage, errorMessage = _a.errorMessage;
            var _b = _this.props, api = _b.api, organization = _b.organization, team = _b.team;
            _this.setState({
                loading: true,
            });
            return new Promise(function (resolve, reject) {
                return teams_1.joinTeam(api, {
                    orgId: organization.slug,
                    teamId: team.slug,
                }, {
                    success: function () {
                        _this.setState({
                            loading: false,
                            error: false,
                        });
                        indicator_1.addSuccessMessage(successMessage);
                        resolve();
                    },
                    error: function () {
                        _this.setState({
                            loading: false,
                            error: true,
                        });
                        indicator_1.addErrorMessage(errorMessage);
                        reject(new Error('Unable to join team'));
                    },
                });
            });
        };
        _this.handleLeaveTeam = function () {
            var _a = _this.props, api = _a.api, organization = _a.organization, team = _a.team;
            _this.setState({
                loading: true,
            });
            teams_1.leaveTeam(api, {
                orgId: organization.slug,
                teamId: team.slug,
            }, {
                success: function () {
                    _this.setState({
                        loading: false,
                        error: false,
                    });
                    indicator_1.addSuccessMessage(locale_1.tct('You have left [team]', {
                        team: "#" + team.slug,
                    }));
                },
                error: function () {
                    _this.setState({
                        loading: false,
                        error: true,
                    });
                    indicator_1.addErrorMessage(locale_1.tct('Unable to leave [team]', {
                        team: "#" + team.slug,
                    }));
                },
            });
        };
        return _this;
    }
    AllTeamsRow.prototype.render = function () {
        var _a = this.props, team = _a.team, urlPrefix = _a.urlPrefix, openMembership = _a.openMembership;
        var display = (<idBadge_1.default team={team} avatarSize={36} description={locale_1.tn('%s Member', '%s Members', team.memberCount)}/>);
        // You can only view team details if you have access to team -- this should account
        // for your role + org open membership
        var canViewTeam = team.hasAccess;
        return (<TeamPanelItem>
        <TeamNameWrapper>
          {canViewTeam ? (<TeamLink to={urlPrefix + "teams/" + team.slug + "/"}>{display}</TeamLink>) : (display)}
        </TeamNameWrapper>
        <Spacer>
          {this.state.loading ? (<button_1.default size="small" disabled>
              ...
            </button_1.default>) : team.isMember ? (<button_1.default size="small" onClick={this.handleLeaveTeam}>
              {locale_1.t('Leave Team')}
            </button_1.default>) : team.isPending ? (<button_1.default size="small" disabled>
              {locale_1.t('Request Pending')}
            </button_1.default>) : openMembership ? (<button_1.default size="small" onClick={this.handleJoinTeam}>
              {locale_1.t('Join Team')}
            </button_1.default>) : (<button_1.default size="small" onClick={this.handleRequestAccess}>
              {locale_1.t('Request Access')}
            </button_1.default>)}
        </Spacer>
      </TeamPanelItem>);
    };
    return AllTeamsRow;
}(React.Component));
exports.AllTeamsRow = AllTeamsRow;
var TeamLink = styled_1.default(react_router_1.Link)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n\n  &.focus-visible {\n    margin: -", ";\n    padding: ", ";\n    background: #f2eff5;\n    border-radius: 3px;\n    outline: none;\n  }\n"], ["\n  display: inline-block;\n\n  &.focus-visible {\n    margin: -", ";\n    padding: ", ";\n    background: #f2eff5;\n    border-radius: 3px;\n    outline: none;\n  }\n"])), space_1.default(1), space_1.default(1));
exports.default = withApi_1.default(AllTeamsRow);
var TeamPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n  align-items: center;\n"], ["\n  padding: 0;\n  align-items: center;\n"])));
var Spacer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space_1.default(2));
var TeamNameWrapper = styled_1.default(Spacer)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=allTeamsRow.jsx.map