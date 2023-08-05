Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var indicator_1 = require("app/actionCreators/indicator");
var teams_1 = require("app/actionCreators/teams");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var panels_1 = require("app/components/panels");
var teamSettingsFields_1 = tslib_1.__importDefault(require("app/data/forms/teamSettingsFields"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var model_1 = tslib_1.__importDefault(require("./model"));
var TeamSettings = /** @class */ (function (_super) {
    tslib_1.__extends(TeamSettings, _super);
    function TeamSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.model = new model_1.default(_this.props.params.orgId, _this.props.params.teamId);
        _this.handleSubmitSuccess = function (resp, model, id) {
            teams_1.updateTeamSuccess(resp.slug, resp);
            if (id === 'slug') {
                indicator_1.addSuccessMessage(locale_1.t('Team name changed'));
                react_router_1.browserHistory.replace("/settings/" + _this.props.params.orgId + "/teams/" + model.getValue(id) + "/settings/");
                _this.setState({ loading: true });
            }
        };
        _this.handleRemoveTeam = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, teams_1.removeTeam(this.api, this.props.params)];
                    case 1:
                        _a.sent();
                        react_router_1.browserHistory.replace("/settings/" + this.props.params.orgId + "/teams/");
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    TeamSettings.prototype.getTitle = function () {
        return 'Team Settings';
    };
    TeamSettings.prototype.getEndpoints = function () {
        return [];
    };
    TeamSettings.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, team = _a.team;
        var access = new Set(organization.access);
        return (<react_1.Fragment>
        <form_1.default model={this.model} apiMethod="PUT" saveOnBlur allowUndo onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={function () { return indicator_1.addErrorMessage(locale_1.t('Unable to save change')); }} initialData={{
                name: team.name,
                slug: team.slug,
            }}>
          <jsonForm_1.default access={access} forms={teamSettingsFields_1.default}/>
        </form_1.default>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Remove Team')}</panels_1.PanelHeader>
          <field_1.default help={locale_1.t("This may affect team members' access to projects and associated alert delivery.")}>
            <div>
              <confirm_1.default disabled={!access.has('team:admin')} onConfirm={this.handleRemoveTeam} priority="danger" message={locale_1.tct('Are you sure you want to remove the team [team]?', {
                team: "#" + team.slug,
            })}>
                <button_1.default icon={<icons_1.IconDelete />} priority="danger" disabled={!access.has('team:admin')}>
                  {locale_1.t('Remove Team')}
                </button_1.default>
              </confirm_1.default>
            </div>
          </field_1.default>
        </panels_1.Panel>
      </react_1.Fragment>);
    };
    return TeamSettings;
}(asyncView_1.default));
exports.default = withOrganization_1.default(TeamSettings);
//# sourceMappingURL=index.jsx.map