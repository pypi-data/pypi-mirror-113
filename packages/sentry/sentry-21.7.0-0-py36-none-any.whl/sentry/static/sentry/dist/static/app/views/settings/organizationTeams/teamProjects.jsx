Object.defineProperty(exports, "__esModule", { value: true });
exports.TeamProjects = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dropdownAutoComplete_1 = tslib_1.__importDefault(require("app/components/dropdownAutoComplete"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var settingsProjectItem_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsProjectItem"));
var TeamProjects = /** @class */ (function (_super) {
    tslib_1.__extends(TeamProjects, _super);
    function TeamProjects() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            error: false,
            loading: true,
            pageLinks: null,
            unlinkedProjects: [],
            linkedProjects: [],
        };
        _this.fetchAll = function () {
            _this.fetchTeamProjects();
            _this.fetchUnlinkedProjects();
        };
        _this.handleLinkProject = function (project, action) {
            var _a = _this.props.params, orgId = _a.orgId, teamId = _a.teamId;
            _this.props.api.request("/projects/" + orgId + "/" + project.slug + "/teams/" + teamId + "/", {
                method: action === 'add' ? 'POST' : 'DELETE',
                success: function (resp) {
                    _this.fetchAll();
                    projectActions_1.default.updateSuccess(resp);
                    indicator_1.addSuccessMessage(action === 'add'
                        ? locale_1.t('Successfully added project to team.')
                        : locale_1.t('Successfully removed project from team'));
                },
                error: function () {
                    indicator_1.addErrorMessage(locale_1.t("Wasn't able to change project association."));
                },
            });
        };
        _this.handleProjectSelected = function (selection) {
            var project = _this.state.unlinkedProjects.find(function (p) { return p.id === selection.value; });
            if (project) {
                _this.handleLinkProject(project, 'add');
            }
        };
        _this.handleQueryUpdate = function (evt) {
            _this.fetchUnlinkedProjects(evt.target.value);
        };
        return _this;
    }
    TeamProjects.prototype.componentDidMount = function () {
        this.fetchAll();
    };
    TeamProjects.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.params.orgId !== this.props.params.orgId ||
            prevProps.params.teamId !== this.props.params.teamId) {
            this.fetchAll();
        }
        if (prevProps.location !== this.props.location) {
            this.fetchTeamProjects();
        }
    };
    TeamProjects.prototype.fetchTeamProjects = function () {
        var _this = this;
        var _a = this.props, location = _a.location, _b = _a.params, orgId = _b.orgId, teamId = _b.teamId;
        this.setState({ loading: true });
        this.props.api
            .requestPromise("/organizations/" + orgId + "/projects/", {
            query: {
                query: "team:" + teamId,
                cursor: location.query.cursor || '',
            },
            includeAllArgs: true,
        })
            .then(function (_a) {
            var _b;
            var _c = tslib_1.__read(_a, 3), linkedProjects = _c[0], _ = _c[1], jqXHR = _c[2];
            _this.setState({
                loading: false,
                error: false,
                linkedProjects: linkedProjects,
                pageLinks: (_b = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.getResponseHeader('Link')) !== null && _b !== void 0 ? _b : null,
            });
        })
            .catch(function () {
            _this.setState({ loading: false, error: true });
        });
    };
    TeamProjects.prototype.fetchUnlinkedProjects = function (query) {
        var _this = this;
        if (query === void 0) { query = ''; }
        var _a = this.props.params, orgId = _a.orgId, teamId = _a.teamId;
        this.props.api
            .requestPromise("/organizations/" + orgId + "/projects/", {
            query: {
                query: query ? "!team:" + teamId + " " + query : "!team:" + teamId,
            },
        })
            .then(function (unlinkedProjects) {
            _this.setState({ unlinkedProjects: unlinkedProjects });
        });
    };
    TeamProjects.prototype.projectPanelContents = function (projects) {
        var _this = this;
        var organization = this.props.organization;
        var access = new Set(organization.access);
        var canWrite = access.has('org:write');
        return projects.length ? (utils_1.sortProjects(projects).map(function (project) { return (<StyledPanelItem key={project.id}>
          <settingsProjectItem_1.default project={project} organization={organization}/>
          <tooltip_1.default disabled={canWrite} title={locale_1.t('You do not have enough permission to change project association.')}>
            <button_1.default size="small" disabled={!canWrite} icon={<icons_1.IconSubtract isCircled size="xs"/>} onClick={function () {
                _this.handleLinkProject(project, 'remove');
            }}>
              {locale_1.t('Remove')}
            </button_1.default>
          </tooltip_1.default>
        </StyledPanelItem>); })) : (<emptyMessage_1.default size="large" icon={<icons_1.IconFlag size="xl"/>}>
        {locale_1.t("This team doesn't have access to any projects.")}
      </emptyMessage_1.default>);
    };
    TeamProjects.prototype.render = function () {
        var _this = this;
        var _a = this.state, linkedProjects = _a.linkedProjects, unlinkedProjects = _a.unlinkedProjects, error = _a.error, loading = _a.loading;
        if (error) {
            return <loadingError_1.default onRetry={function () { return _this.fetchAll(); }}/>;
        }
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        var access = new Set(this.props.organization.access);
        var otherProjects = unlinkedProjects.map(function (p) { return ({
            value: p.id,
            searchKey: p.slug,
            label: <ProjectListElement>{p.slug}</ProjectListElement>,
        }); });
        return (<React.Fragment>
        <panels_1.Panel>
          <panels_1.PanelHeader hasButtons>
            <div>{locale_1.t('Projects')}</div>
            <div style={{ textTransform: 'none' }}>
              {!access.has('org:write') ? (<dropdownButton_1.default disabled title={locale_1.t('You do not have enough permission to associate a project.')} size="xsmall">
                  {locale_1.t('Add Project')}
                </dropdownButton_1.default>) : (<dropdownAutoComplete_1.default items={otherProjects} onChange={this.handleQueryUpdate} onSelect={this.handleProjectSelected} emptyMessage={locale_1.t('No projects')} alignMenu="right">
                  {function (_a) {
                    var isOpen = _a.isOpen;
                    return (<dropdownButton_1.default isOpen={isOpen} size="xsmall">
                      {locale_1.t('Add Project')}
                    </dropdownButton_1.default>);
                }}
                </dropdownAutoComplete_1.default>)}
            </div>
          </panels_1.PanelHeader>
          <panels_1.PanelBody>{this.projectPanelContents(linkedProjects)}</panels_1.PanelBody>
        </panels_1.Panel>
        <pagination_1.default pageLinks={this.state.pageLinks} {...this.props}/>
      </React.Fragment>);
    };
    return TeamProjects;
}(React.Component));
exports.TeamProjects = TeamProjects;
var StyledPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", ";\n"])), space_1.default(2));
var ProjectListElement = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: ", " 0;\n"], ["\n  padding: ", " 0;\n"])), space_1.default(0.25));
exports.default = withApi_1.default(withOrganization_1.default(TeamProjects));
var templateObject_1, templateObject_2;
//# sourceMappingURL=teamProjects.jsx.map