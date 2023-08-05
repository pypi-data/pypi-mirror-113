Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectEnvironments = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var listLink_1 = tslib_1.__importDefault(require("app/components/links/listLink"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var panels_1 = require("app/components/panels");
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var environment_1 = require("app/utils/environment");
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/project/permissionAlert"));
var ProjectEnvironments = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectEnvironments, _super);
    function ProjectEnvironments() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            project: null,
            environments: null,
            isLoading: true,
        };
        // Toggle visibility of environment
        _this.toggleEnv = function (env, shouldHide) {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.props.api.request("/projects/" + orgId + "/" + projectId + "/environments/" + environment_1.getUrlRoutingName(env) + "/", {
                method: 'PUT',
                data: {
                    name: env.name,
                    isHidden: shouldHide,
                },
                success: function () {
                    indicator_1.addSuccessMessage(locale_1.tct('Updated [environment]', {
                        environment: environment_1.getDisplayName(env),
                    }));
                },
                error: function () {
                    indicator_1.addErrorMessage(locale_1.tct('Unable to update [environment]', {
                        environment: environment_1.getDisplayName(env),
                    }));
                },
                complete: _this.fetchData.bind(_this),
            });
        };
        return _this;
    }
    ProjectEnvironments.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ProjectEnvironments.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.location.pathname.endsWith('hidden/') !==
            prevProps.location.pathname.endsWith('hidden/')) {
            this.fetchData();
        }
    };
    ProjectEnvironments.prototype.fetchData = function () {
        var _this = this;
        var isHidden = this.props.location.pathname.endsWith('hidden/');
        if (!this.state.isLoading) {
            this.setState({ isLoading: true });
        }
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        this.props.api.request("/projects/" + orgId + "/" + projectId + "/environments/", {
            query: {
                visibility: isHidden ? 'hidden' : 'visible',
            },
            success: function (environments) {
                _this.setState({ environments: environments, isLoading: false });
            },
        });
    };
    ProjectEnvironments.prototype.fetchProjectDetails = function () {
        var _this = this;
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        this.props.api.request("/projects/" + orgId + "/" + projectId + "/", {
            success: function (project) {
                _this.setState({ project: project });
            },
        });
    };
    ProjectEnvironments.prototype.renderEmpty = function () {
        var isHidden = this.props.location.pathname.endsWith('hidden/');
        var message = isHidden
            ? locale_1.t("You don't have any hidden environments.")
            : locale_1.t("You don't have any environments yet.");
        return <emptyMessage_1.default>{message}</emptyMessage_1.default>;
    };
    /**
     * Renders rows for "system" environments:
     * - "All Environments"
     * - "No Environment"
     *
     */
    ProjectEnvironments.prototype.renderAllEnvironmentsSystemRow = function () {
        // Not available in "Hidden" tab
        var isHidden = this.props.location.pathname.endsWith('hidden/');
        if (isHidden) {
            return null;
        }
        return (<EnvironmentRow name={constants_1.ALL_ENVIRONMENTS_KEY} environment={{
                id: constants_1.ALL_ENVIRONMENTS_KEY,
                name: constants_1.ALL_ENVIRONMENTS_KEY,
                displayName: constants_1.ALL_ENVIRONMENTS_KEY,
            }} isSystemRow/>);
    };
    ProjectEnvironments.prototype.renderEnvironmentList = function (envs) {
        var _this = this;
        var isHidden = this.props.location.pathname.endsWith('hidden/');
        var buttonText = isHidden ? locale_1.t('Show') : locale_1.t('Hide');
        return (<react_1.Fragment>
        {this.renderAllEnvironmentsSystemRow()}
        {envs.map(function (env) { return (<EnvironmentRow key={env.id} name={env.name} environment={env} isHidden={isHidden} onHide={_this.toggleEnv} actionText={buttonText} shouldShowAction/>); })}
      </react_1.Fragment>);
    };
    ProjectEnvironments.prototype.renderBody = function () {
        var _a = this.state, environments = _a.environments, isLoading = _a.isLoading;
        if (isLoading) {
            return <loadingIndicator_1.default />;
        }
        return (<panels_1.PanelBody>
        {(environments === null || environments === void 0 ? void 0 : environments.length)
                ? this.renderEnvironmentList(environments)
                : this.renderEmpty()}
      </panels_1.PanelBody>);
    };
    ProjectEnvironments.prototype.render = function () {
        var _a = this.props, routes = _a.routes, params = _a.params, location = _a.location;
        var isHidden = location.pathname.endsWith('hidden/');
        var baseUrl = recreateRoute_1.default('', { routes: routes, params: params, stepBack: -1 });
        return (<div>
        <sentryDocumentTitle_1.default title={locale_1.t('Environments')} projectSlug={params.projectId}/>
        <settingsPageHeader_1.default title={locale_1.t('Manage Environments')} tabs={<navTabs_1.default underlined>
              <listLink_1.default to={baseUrl} index isActive={function () { return !isHidden; }}>
                {locale_1.t('Environments')}
              </listLink_1.default>
              <listLink_1.default to={baseUrl + "hidden/"} index isActive={function () { return isHidden; }}>
                {locale_1.t('Hidden')}
              </listLink_1.default>
            </navTabs_1.default>}/>
        <permissionAlert_1.default />

        <panels_1.Panel>
          <panels_1.PanelHeader>{isHidden ? locale_1.t('Hidden') : locale_1.t('Active Environments')}</panels_1.PanelHeader>
          {this.renderBody()}
        </panels_1.Panel>
      </div>);
    };
    return ProjectEnvironments;
}(react_1.Component));
exports.ProjectEnvironments = ProjectEnvironments;
function EnvironmentRow(_a) {
    var environment = _a.environment, name = _a.name, onHide = _a.onHide, _b = _a.shouldShowAction, shouldShowAction = _b === void 0 ? false : _b, _c = _a.isSystemRow, isSystemRow = _c === void 0 ? false : _c, _d = _a.isHidden, isHidden = _d === void 0 ? false : _d, _e = _a.actionText, actionText = _e === void 0 ? '' : _e;
    return (<EnvironmentItem>
      <Name>{isSystemRow ? locale_1.t('All Environments') : name}</Name>
      <access_1.default access={['project:write']}>
        {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<react_1.Fragment>
            {shouldShowAction && onHide && (<EnvironmentButton size="xsmall" disabled={!hasAccess} onClick={function () { return onHide(environment, !isHidden); }}>
                {actionText}
              </EnvironmentButton>)}
          </react_1.Fragment>);
        }}
      </access_1.default>
    </EnvironmentItem>);
}
var EnvironmentItem = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  align-items: center;\n  justify-content: space-between;\n"])));
var Name = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var EnvironmentButton = styled_1.default(button_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(0.5));
exports.default = withApi_1.default(ProjectEnvironments);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=projectEnvironments.jsx.map