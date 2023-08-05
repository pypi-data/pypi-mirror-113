Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var modal_1 = require("app/actionCreators/modal");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var panels_1 = require("app/components/panels");
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var allTeamsList_1 = tslib_1.__importDefault(require("./allTeamsList"));
function OrganizationTeams(_a) {
    var allTeams = _a.allTeams, activeTeams = _a.activeTeams, organization = _a.organization, access = _a.access, features = _a.features, routes = _a.routes, params = _a.params;
    if (!organization) {
        return null;
    }
    var canCreateTeams = access.has('project:admin');
    var action = (<button_1.default priority="primary" size="small" disabled={!canCreateTeams} title={!canCreateTeams ? locale_1.t('You do not have permission to create teams') : undefined} onClick={function () {
            return modal_1.openCreateTeamModal({
                organization: organization,
            });
        }} icon={<icons_1.IconAdd size="xs" isCircled/>}>
      {locale_1.t('Create Team')}
    </button_1.default>);
    var teamRoute = routes.find(function (_a) {
        var path = _a.path;
        return path === 'teams/';
    });
    var urlPrefix = teamRoute
        ? recreateRoute_1.default(teamRoute, { routes: routes, params: params, stepBack: -2 })
        : '';
    var activeTeamIds = new Set(activeTeams.map(function (team) { return team.id; }));
    var otherTeams = allTeams.filter(function (team) { return !activeTeamIds.has(team.id); });
    var title = locale_1.t('Teams');
    return (<div data-test-id="team-list">
      <sentryDocumentTitle_1.default title={title} orgSlug={organization.slug}/>
      <settingsPageHeader_1.default title={title} action={action}/>
      <panels_1.Panel>
        <panels_1.PanelHeader>{locale_1.t('Your Teams')}</panels_1.PanelHeader>
        <panels_1.PanelBody>
          <allTeamsList_1.default urlPrefix={urlPrefix} organization={organization} teamList={activeTeams} access={access} openMembership={false}/>
        </panels_1.PanelBody>
      </panels_1.Panel>
      <panels_1.Panel>
        <panels_1.PanelHeader>{locale_1.t('Other Teams')}</panels_1.PanelHeader>
        <panels_1.PanelBody>
          <allTeamsList_1.default urlPrefix={urlPrefix} organization={organization} teamList={otherTeams} access={access} openMembership={!!(features.has('open-membership') || access.has('org:write'))}/>
        </panels_1.PanelBody>
      </panels_1.Panel>
    </div>);
}
exports.default = OrganizationTeams;
//# sourceMappingURL=organizationTeams.jsx.map