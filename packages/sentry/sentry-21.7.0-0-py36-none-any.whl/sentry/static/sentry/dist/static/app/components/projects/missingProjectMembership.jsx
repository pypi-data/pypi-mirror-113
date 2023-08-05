Object.defineProperty(exports, "__esModule", { value: true });
exports.MissingProjectMembership = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var teams_1 = require("app/actionCreators/teams");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var teamStore_1 = tslib_1.__importDefault(require("app/stores/teamStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var MissingProjectMembership = /** @class */ (function (_super) {
    tslib_1.__extends(MissingProjectMembership, _super);
    function MissingProjectMembership(props) {
        var _a;
        var _this = _super.call(this, props) || this;
        _this.handleChangeTeam = function (teamObj) {
            var team = teamObj ? teamObj.value : null;
            _this.setState({ team: team });
        };
        _this.getPendingTeamOption = function (team) {
            return {
                value: team,
                label: <DisabledLabel>{locale_1.t("#" + team)}</DisabledLabel>,
            };
        };
        var _b = _this.props, organization = _b.organization, projectSlug = _b.projectSlug;
        var project = (_a = organization.projects) === null || _a === void 0 ? void 0 : _a.find(function (p) { return p.slug === projectSlug; });
        _this.state = {
            loading: false,
            error: false,
            project: project,
            team: '',
        };
        return _this;
    }
    MissingProjectMembership.prototype.joinTeam = function (teamSlug) {
        var _this = this;
        this.setState({
            loading: true,
        });
        teams_1.joinTeam(this.props.api, {
            orgId: this.props.organization.slug,
            teamId: teamSlug,
        }, {
            success: function () {
                _this.setState({
                    loading: false,
                    error: false,
                });
                indicator_1.addSuccessMessage(locale_1.t('Request to join team sent.'));
            },
            error: function () {
                _this.setState({
                    loading: false,
                    error: true,
                });
                indicator_1.addErrorMessage(locale_1.t('There was an error while trying to request access.'));
            },
        });
    };
    MissingProjectMembership.prototype.renderJoinTeam = function (teamSlug, features) {
        var team = teamStore_1.default.getBySlug(teamSlug);
        if (!team) {
            return null;
        }
        if (this.state.loading) {
            if (features.has('open-membership')) {
                return <button_1.default busy>{locale_1.t('Join Team')}</button_1.default>;
            }
            return <button_1.default busy>{locale_1.t('Request Access')}</button_1.default>;
        }
        else if (team === null || team === void 0 ? void 0 : team.isPending) {
            return <button_1.default disabled>{locale_1.t('Request Pending')}</button_1.default>;
        }
        else if (features.has('open-membership')) {
            return (<button_1.default priority="primary" type="button" onClick={this.joinTeam.bind(this, teamSlug)}>
          {locale_1.t('Join Team')}
        </button_1.default>);
        }
        return (<button_1.default priority="primary" type="button" onClick={this.joinTeam.bind(this, teamSlug)}>
        {locale_1.t('Request Access')}
      </button_1.default>);
    };
    MissingProjectMembership.prototype.getTeamsForAccess = function () {
        var _a, _b;
        var request = [];
        var pending = [];
        var teams = (_b = (_a = this.state.project) === null || _a === void 0 ? void 0 : _a.teams) !== null && _b !== void 0 ? _b : [];
        teams.forEach(function (_a) {
            var slug = _a.slug;
            var team = teamStore_1.default.getBySlug(slug);
            if (!team) {
                return;
            }
            team.isPending ? pending.push(team.slug) : request.push(team.slug);
        });
        return [request, pending];
    };
    MissingProjectMembership.prototype.render = function () {
        var _this = this;
        var _a, _b;
        var organization = this.props.organization;
        var teamSlug = this.state.team;
        var teams = (_b = (_a = this.state.project) === null || _a === void 0 ? void 0 : _a.teams) !== null && _b !== void 0 ? _b : [];
        var features = new Set(organization.features);
        var teamAccess = [
            {
                label: locale_1.t('Request Access'),
                options: this.getTeamsForAccess()[0].map(function (request) { return ({
                    value: request,
                    label: locale_1.t("#" + request),
                }); }),
            },
            {
                label: locale_1.t('Pending Requests'),
                options: this.getTeamsForAccess()[1].map(function (pending) {
                    return _this.getPendingTeamOption(pending);
                }),
            },
        ];
        return (<StyledPanel>
        {!teams.length ? (<emptyMessage_1.default icon={<icons_1.IconFlag size="xl"/>}>
            {locale_1.t('No teams have access to this project yet. Ask an admin to add your team to this project.')}
          </emptyMessage_1.default>) : (<emptyMessage_1.default icon={<icons_1.IconFlag size="xl"/>} title={locale_1.t("You're not a member of this project.")} description={locale_1.t("You'll need to join a team with access before you can view this data.")} action={<Field>
                <StyledSelectControl name="select" placeholder={locale_1.t('Select a Team')} options={teamAccess} onChange={this.handleChangeTeam}/>
                {teamSlug ? (this.renderJoinTeam(teamSlug, features)) : (<button_1.default disabled>{locale_1.t('Select a Team')}</button_1.default>)}
              </Field>}/>)}
      </StyledPanel>);
    };
    return MissingProjectMembership;
}(react_1.Component));
exports.MissingProjectMembership = MissingProjectMembership;
var StyledPanel = styled_1.default(panels_1.Panel)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: ", " 0;\n"], ["\n  margin: ", " 0;\n"])), space_1.default(2));
var Field = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  gap: ", ";\n  text-align: left;\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  gap: ", ";\n  text-align: left;\n"])), space_1.default(2));
var StyledSelectControl = styled_1.default(selectControl_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  width: 250px;\n"], ["\n  width: 250px;\n"])));
var DisabledLabel = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  opacity: 0.5;\n  overflow: hidden;\n"], ["\n  display: flex;\n  opacity: 0.5;\n  overflow: hidden;\n"])));
exports.default = withApi_1.default(MissingProjectMembership);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=missingProjectMembership.jsx.map