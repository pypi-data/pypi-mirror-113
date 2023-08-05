Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var projects_1 = require("app/actionCreators/projects");
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var teamSelect_1 = tslib_1.__importDefault(require("app/views/settings/components/teamSelect"));
var ProjectTeams = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectTeams, _super);
    function ProjectTeams() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.canCreateTeam = function () {
            var organization = _this.props.organization;
            var access = new Set(organization.access);
            return (access.has('org:write') && access.has('team:write') && access.has('project:write'));
        };
        _this.handleRemove = function (teamSlug) {
            if (_this.state.loading) {
                return;
            }
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            projects_1.removeTeamFromProject(_this.api, orgId, projectId, teamSlug)
                .then(function () { return _this.handleRemovedTeam(teamSlug); })
                .catch(function () {
                indicator_1.addErrorMessage(locale_1.t('Could not remove the %s team', teamSlug));
                _this.setState({ loading: false });
            });
        };
        _this.handleRemovedTeam = function (teamSlug) {
            _this.setState(function (prevState) { return ({
                projectTeams: tslib_1.__spreadArray([], tslib_1.__read((prevState.projectTeams || []).filter(function (team) { return team.slug !== teamSlug; }))),
            }); });
        };
        _this.handleAddedTeam = function (team) {
            _this.setState(function (prevState) { return ({
                projectTeams: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read((prevState.projectTeams || []))), [team]),
            }); });
        };
        _this.handleAdd = function (team) {
            if (_this.state.loading) {
                return;
            }
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            projects_1.addTeamToProject(_this.api, orgId, projectId, team).then(function () {
                _this.handleAddedTeam(team);
            }, function () {
                _this.setState({
                    error: true,
                    loading: false,
                });
            });
        };
        _this.handleCreateTeam = function (e) {
            var _a = _this.props, project = _a.project, organization = _a.organization;
            if (!_this.canCreateTeam()) {
                return;
            }
            e.stopPropagation();
            e.preventDefault();
            modal_1.openCreateTeamModal({
                project: project,
                organization: organization,
                onClose: function (data) {
                    projects_1.addTeamToProject(_this.api, organization.slug, project.slug, data).then(_this.remountComponent, _this.remountComponent);
                },
            });
        };
        return _this;
    }
    ProjectTeams.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['projectTeams', "/projects/" + orgId + "/" + projectId + "/teams/"]];
    };
    ProjectTeams.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitle_1.default(locale_1.t('Project Teams'), projectId, false);
    };
    ProjectTeams.prototype.renderBody = function () {
        var _a = this.props, params = _a.params, organization = _a.organization;
        var canCreateTeam = this.canCreateTeam();
        var hasAccess = organization.access.includes('project:write');
        var confirmRemove = locale_1.t('This is the last team with access to this project. Removing it will mean ' +
            'only organization owners and managers will be able to access the project pages. Are ' +
            'you sure you want to remove this team from the project %s?', params.projectId);
        var projectTeams = this.state.projectTeams;
        var menuHeader = (<StyledTeamsLabel>
        {locale_1.t('Teams')}
        <tooltip_1.default disabled={canCreateTeam} title={locale_1.t('You must be a project admin to create teams')} position="top">
          <StyledCreateTeamLink to="" disabled={!canCreateTeam} onClick={this.handleCreateTeam}>
            {locale_1.t('Create Team')}
          </StyledCreateTeamLink>
        </tooltip_1.default>
      </StyledTeamsLabel>);
        return (<div>
        <settingsPageHeader_1.default title={locale_1.t('%s Teams', params.projectId)}/>
        <teamSelect_1.default organization={organization} selectedTeams={projectTeams !== null && projectTeams !== void 0 ? projectTeams : []} onAddTeam={this.handleAdd} onRemoveTeam={this.handleRemove} menuHeader={menuHeader} confirmLastTeamRemoveMessage={confirmRemove} disabled={!hasAccess}/>
      </div>);
    };
    return ProjectTeams;
}(asyncView_1.default));
var StyledTeamsLabel = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: 0.875em;\n  padding: ", " 0px;\n  text-transform: uppercase;\n"], ["\n  font-size: 0.875em;\n  padding: ", " 0px;\n  text-transform: uppercase;\n"])), space_1.default(0.5));
var StyledCreateTeamLink = styled_1.default(link_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  float: right;\n  text-transform: none;\n  ", ";\n"], ["\n  float: right;\n  text-transform: none;\n  ", ";\n"])), function (p) {
    return p.disabled && react_1.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n      cursor: not-allowed;\n      color: ", ";\n      opacity: 0.6;\n    "], ["\n      cursor: not-allowed;\n      color: ", ";\n      opacity: 0.6;\n    "])), p.theme.gray300);
});
exports.default = ProjectTeams;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=projectTeams.jsx.map