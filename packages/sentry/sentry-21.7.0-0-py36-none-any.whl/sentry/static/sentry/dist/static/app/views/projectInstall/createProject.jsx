Object.defineProperty(exports, "__esModule", { value: true });
exports.CreateProject = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var platformicons_1 = require("platformicons");
var modal_1 = require("app/actionCreators/modal");
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var pageHeading_1 = tslib_1.__importDefault(require("app/components/pageHeading"));
var platformPicker_1 = tslib_1.__importDefault(require("app/components/platformPicker"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var platformCategories_1 = tslib_1.__importDefault(require("app/data/platformCategories"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var input_1 = require("app/styles/input");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var getPlatformName_1 = tslib_1.__importDefault(require("app/utils/getPlatformName"));
var slugify_1 = tslib_1.__importDefault(require("app/utils/slugify"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var issueAlertOptions_1 = tslib_1.__importDefault(require("app/views/projectInstall/issueAlertOptions"));
var getCategoryName = function (category) { var _a; return (_a = platformCategories_1.default.find(function (_a) {
    var id = _a.id;
    return id === category;
})) === null || _a === void 0 ? void 0 : _a.id; };
var CreateProject = /** @class */ (function (_super) {
    tslib_1.__extends(CreateProject, _super);
    function CreateProject(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.createProject = function (e) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, organization, api, _b, projectName, platform, team, dataFragment, slug, _c, shouldCreateCustomRule, name, conditions, actions, actionMatch, frequency, defaultRules, projectData, ruleId, ruleData, platformKey, nextUrl, err_1;
            var _this = this;
            return tslib_1.__generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        e.preventDefault();
                        _a = this.props, organization = _a.organization, api = _a.api;
                        _b = this.state, projectName = _b.projectName, platform = _b.platform, team = _b.team, dataFragment = _b.dataFragment;
                        slug = organization.slug;
                        _c = dataFragment || {}, shouldCreateCustomRule = _c.shouldCreateCustomRule, name = _c.name, conditions = _c.conditions, actions = _c.actions, actionMatch = _c.actionMatch, frequency = _c.frequency, defaultRules = _c.defaultRules;
                        this.setState({ inFlight: true });
                        if (!projectName) {
                            Sentry.withScope(function (scope) {
                                scope.setExtra('props', _this.props);
                                scope.setExtra('state', _this.state);
                                Sentry.captureMessage('No project name');
                            });
                        }
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 5, , 6]);
                        return [4 /*yield*/, api.requestPromise("/teams/" + slug + "/" + team + "/projects/", {
                                method: 'POST',
                                data: {
                                    name: projectName,
                                    platform: platform,
                                    default_rules: defaultRules !== null && defaultRules !== void 0 ? defaultRules : true,
                                },
                            })];
                    case 2:
                        projectData = _d.sent();
                        ruleId = void 0;
                        if (!shouldCreateCustomRule) return [3 /*break*/, 4];
                        return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + projectData.slug + "/rules/", {
                                method: 'POST',
                                data: {
                                    name: name,
                                    conditions: conditions,
                                    actions: actions,
                                    actionMatch: actionMatch,
                                    frequency: frequency,
                                },
                            })];
                    case 3:
                        ruleData = _d.sent();
                        ruleId = ruleData.id;
                        _d.label = 4;
                    case 4:
                        this.trackIssueAlertOptionSelectedEvent(projectData, defaultRules, shouldCreateCustomRule, ruleId);
                        projectActions_1.default.createSuccess(projectData);
                        platformKey = platform || 'other';
                        nextUrl = "/" + organization.slug + "/" + projectData.slug + "/getting-started/" + platformKey + "/";
                        react_router_1.browserHistory.push(nextUrl);
                        return [3 /*break*/, 6];
                    case 5:
                        err_1 = _d.sent();
                        this.setState({
                            inFlight: false,
                            error: err_1.responseJSON.detail,
                        });
                        // Only log this if the error is something other than:
                        // * The user not having access to create a project, or,
                        // * A project with that slug already exists
                        if (err_1.status !== 403 && err_1.status !== 409) {
                            Sentry.withScope(function (scope) {
                                scope.setExtra('err', err_1);
                                scope.setExtra('props', _this.props);
                                scope.setExtra('state', _this.state);
                                Sentry.captureMessage('Project creation failed');
                            });
                        }
                        return [3 /*break*/, 6];
                    case 6: return [2 /*return*/];
                }
            });
        }); };
        _this.setPlatform = function (platformId) {
            return _this.setState(function (_a) {
                var projectName = _a.projectName, platform = _a.platform;
                return ({
                    platform: platformId,
                    projectName: !projectName || (platform && getPlatformName_1.default(platform) === projectName)
                        ? getPlatformName_1.default(platformId) || ''
                        : projectName,
                });
            });
        };
        var query = props.location.query;
        var teams = props.organization.teams;
        var accessTeams = teams.filter(function (team) { return team.hasAccess; });
        var team = query.team || (accessTeams.length && accessTeams[0].slug);
        var platform = getPlatformName_1.default(query.platform) ? query.platform : '';
        _this.state = {
            error: false,
            projectName: getPlatformName_1.default(platform) || '',
            team: team,
            platform: platform,
            inFlight: false,
            dataFragment: undefined,
        };
        return _this;
    }
    Object.defineProperty(CreateProject.prototype, "defaultCategory", {
        get: function () {
            var query = this.props.location.query;
            return getCategoryName(query.category);
        },
        enumerable: false,
        configurable: true
    });
    CreateProject.prototype.renderProjectForm = function () {
        var _this = this;
        var organization = this.props.organization;
        var _a = this.state, projectName = _a.projectName, platform = _a.platform, team = _a.team;
        var teams = this.props.teams.filter(function (filterTeam) { return filterTeam.hasAccess; });
        var createProjectForm = (<CreateProjectForm onSubmit={this.createProject}>
        <div>
          <FormLabel>{locale_1.t('Project name')}</FormLabel>
          <ProjectNameInput>
            <StyledPlatformIcon platform={platform !== null && platform !== void 0 ? platform : ''}/>
            <input type="text" name="name" placeholder={locale_1.t('Project name')} autoComplete="off" value={projectName} onChange={function (e) { return _this.setState({ projectName: slugify_1.default(e.target.value) }); }}/>
          </ProjectNameInput>
        </div>
        <div>
          <FormLabel>{locale_1.t('Team')}</FormLabel>
          <TeamSelectInput>
            <selectControl_1.default name="select-team" clearable={false} value={team} placeholder={locale_1.t('Select a Team')} onChange={function (choice) { return _this.setState({ team: choice.value }); }} options={teams.map(function (_a) {
                var slug = _a.slug;
                return ({
                    label: "#" + slug,
                    value: slug,
                });
            })}/>
            <tooltip_1.default title={locale_1.t('Create a team')}>
              <button_1.default borderless data-test-id="create-team" type="button" icon={<icons_1.IconAdd isCircled/>} onClick={function () {
                return modal_1.openCreateTeamModal({
                    organization: organization,
                    onClose: function (_a) {
                        var slug = _a.slug;
                        return _this.setState({ team: slug });
                    },
                });
            }}/>
            </tooltip_1.default>
          </TeamSelectInput>
        </div>
        <div>
          <button_1.default data-test-id="create-project" priority="primary" disabled={!this.canSubmitForm}>
            {locale_1.t('Create Project')}
          </button_1.default>
        </div>
      </CreateProjectForm>);
        return (<React.Fragment>
        <pageHeading_1.default withMargins>{locale_1.t('Give your project a name')}</pageHeading_1.default>
        {createProjectForm}
      </React.Fragment>);
    };
    Object.defineProperty(CreateProject.prototype, "canSubmitForm", {
        get: function () {
            var _a;
            var _b = this.state, projectName = _b.projectName, team = _b.team, inFlight = _b.inFlight;
            var _c = this.state.dataFragment || {}, shouldCreateCustomRule = _c.shouldCreateCustomRule, conditions = _c.conditions;
            return (!inFlight &&
                team &&
                projectName !== '' &&
                (!shouldCreateCustomRule || ((_a = conditions === null || conditions === void 0 ? void 0 : conditions.every) === null || _a === void 0 ? void 0 : _a.call(conditions, function (condition) { return condition.value; }))));
        },
        enumerable: false,
        configurable: true
    });
    CreateProject.prototype.trackIssueAlertOptionSelectedEvent = function (projectData, isDefaultRules, shouldCreateCustomRule, ruleId) {
        var organization = this.props.organization;
        var data = {
            eventKey: 'new_project.alert_rule_selected',
            eventName: 'New Project Alert Rule Selected',
            organization_id: organization.id,
            project_id: projectData.id,
            rule_type: isDefaultRules
                ? 'Default'
                : shouldCreateCustomRule
                    ? 'Custom'
                    : 'No Rule',
        };
        if (ruleId !== undefined) {
            data = tslib_1.__assign(tslib_1.__assign({}, data), { custom_rule_id: ruleId });
        }
        analytics_1.trackAnalyticsEvent(data);
    };
    CreateProject.prototype.render = function () {
        var _this = this;
        var _a = this.state, platform = _a.platform, error = _a.error;
        return (<React.Fragment>
        {error && <alert_1.default type="error">{error}</alert_1.default>}

        <div data-test-id="onboarding-info">
          <pageHeading_1.default withMargins>{locale_1.t('Create a new Project')}</pageHeading_1.default>
          <HelpText>
            {locale_1.t("Projects allow you to scope error and transaction events to a specific\n               application in your organization. For example, you might have separate\n               projects for your API server and frontend client.")}
          </HelpText>
          <pageHeading_1.default withMargins>{locale_1.t('Choose a platform')}</pageHeading_1.default>
          <platformPicker_1.default platform={platform} defaultCategory={this.defaultCategory} setPlatform={this.setPlatform} organization={this.props.organization} showOther/>
          <issueAlertOptions_1.default onChange={function (updatedData) {
                _this.setState({ dataFragment: updatedData });
            }}/>
          {this.renderProjectForm()}
        </div>
      </React.Fragment>);
    };
    return CreateProject;
}(React.Component));
exports.CreateProject = CreateProject;
exports.default = withApi_1.default(react_router_1.withRouter(withOrganization_1.default(withTeams_1.default(CreateProject))));
var CreateProjectForm = styled_1.default('form')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 300px 250px max-content;\n  grid-gap: ", ";\n  align-items: end;\n  padding: ", " 0;\n  box-shadow: 0 -1px 0 rgba(0, 0, 0, 0.1);\n  background: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 300px 250px max-content;\n  grid-gap: ", ";\n  align-items: end;\n  padding: ", " 0;\n  box-shadow: 0 -1px 0 rgba(0, 0, 0, 0.1);\n  background: ", ";\n"])), space_1.default(2), space_1.default(3), function (p) { return p.theme.background; });
var FormLabel = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space_1.default(1));
var StyledPlatformIcon = styled_1.default(platformicons_1.PlatformIcon)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
var ProjectNameInput = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  ", ";\n  padding: 5px 10px;\n  display: flex;\n  align-items: center;\n\n  input {\n    background: ", ";\n    border: 0;\n    outline: 0;\n    flex: 1;\n  }\n"], ["\n  ", ";\n  padding: 5px 10px;\n  display: flex;\n  align-items: center;\n\n  input {\n    background: ", ";\n    border: 0;\n    outline: 0;\n    flex: 1;\n  }\n"])), function (p) { return input_1.inputStyles(p); }, function (p) { return p.theme.background; });
var TeamSelectInput = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr min-content;\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr min-content;\n  align-items: center;\n"])));
var HelpText = styled_1.default('p')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  max-width: 760px;\n"], ["\n  color: ", ";\n  max-width: 760px;\n"])), function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=createProject.jsx.map