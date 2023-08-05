Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var sortBy_1 = tslib_1.__importDefault(require("lodash/sortBy"));
var qs = tslib_1.__importStar(require("query-string"));
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var panels_1 = require("app/components/panels");
var repositoryProjectPathConfigForm_1 = tslib_1.__importDefault(require("app/components/repositoryProjectPathConfigForm"));
var repositoryProjectPathConfigRow_1 = tslib_1.__importStar(require("app/components/repositoryProjectPathConfigRow"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var integrationUtil_1 = require("app/utils/integrationUtil");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var IntegrationCodeMappings = /** @class */ (function (_super) {
    tslib_1.__extends(IntegrationCodeMappings, _super);
    function IntegrationCodeMappings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (pathConfig) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var organization, endpoint, pathConfigs, err_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        organization = this.props.organization;
                        endpoint = "/organizations/" + organization.slug + "/code-mappings/" + pathConfig.id + "/";
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(endpoint, {
                                method: 'DELETE',
                            })];
                    case 2:
                        _a.sent();
                        pathConfigs = this.state.pathConfigs;
                        pathConfigs = pathConfigs.filter(function (config) { return config.id !== pathConfig.id; });
                        this.setState({ pathConfigs: pathConfigs });
                        indicator_1.addSuccessMessage(locale_1.t('Deletion successful'));
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _a.sent();
                        indicator_1.addErrorMessage(locale_1.tct('[status]: [text]', {
                            status: err_1.statusText,
                            text: err_1.responseText,
                        }));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleSubmitSuccess = function (pathConfig) {
            integrationUtil_1.trackIntegrationEvent('integrations.stacktrace_complete_setup', {
                setup_type: 'manual',
                view: 'integration_configuration_detail',
                provider: _this.props.integration.provider.key,
            }, _this.props.organization);
            var pathConfigs = _this.state.pathConfigs;
            pathConfigs = pathConfigs.filter(function (config) { return config.id !== pathConfig.id; });
            // our getter handles the order of the configs
            pathConfigs = pathConfigs.concat([pathConfig]);
            _this.setState({ pathConfigs: pathConfigs });
            _this.setState({ pathConfig: undefined });
        };
        _this.openModal = function (pathConfig) {
            var _a = _this.props, organization = _a.organization, integration = _a.integration;
            integrationUtil_1.trackIntegrationEvent('integrations.stacktrace_start_setup', {
                setup_type: 'manual',
                view: 'integration_configuration_detail',
                provider: _this.props.integration.provider.key,
            }, _this.props.organization);
            modal_1.openModal(function (_a) {
                var Body = _a.Body, Header = _a.Header, closeModal = _a.closeModal;
                return (<react_1.Fragment>
        <Header closeButton>{locale_1.t('Configure code path mapping')}</Header>
        <Body>
          <repositoryProjectPathConfigForm_1.default organization={organization} integration={integration} projects={_this.projects} repos={_this.repos} onSubmitSuccess={function (config) {
                        _this.handleSubmitSuccess(config);
                        closeModal();
                    }} existingConfig={pathConfig} onCancel={closeModal}/>
        </Body>
      </react_1.Fragment>);
            });
        };
        return _this;
    }
    IntegrationCodeMappings.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { pathConfigs: [], repos: [] });
    };
    Object.defineProperty(IntegrationCodeMappings.prototype, "integrationId", {
        get: function () {
            return this.props.integration.id;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationCodeMappings.prototype, "projects", {
        get: function () {
            return this.props.organization.projects;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationCodeMappings.prototype, "pathConfigs", {
        get: function () {
            // we want to sort by the project slug and the
            // id of the config
            return sortBy_1.default(this.state.pathConfigs, [
                function (_a) {
                    var projectSlug = _a.projectSlug;
                    return projectSlug;
                },
                function (_a) {
                    var id = _a.id;
                    return parseInt(id, 10);
                },
            ]);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationCodeMappings.prototype, "repos", {
        get: function () {
            var _this = this;
            // endpoint doesn't support loading only the repos for this integration
            // but most people only have one source code repo so this should be fine
            return this.state.repos.filter(function (repo) { return repo.integrationId === _this.integrationId; });
        },
        enumerable: false,
        configurable: true
    });
    IntegrationCodeMappings.prototype.getEndpoints = function () {
        var orgSlug = this.props.organization.slug;
        return [
            [
                'pathConfigs',
                "/organizations/" + orgSlug + "/code-mappings/",
                { query: { integrationId: this.integrationId } },
            ],
            ['repos', "/organizations/" + orgSlug + "/repos/", { query: { status: 'active' } }],
        ];
    };
    IntegrationCodeMappings.prototype.getMatchingProject = function (pathConfig) {
        return this.projects.find(function (project) { return project.id === pathConfig.projectId; });
    };
    IntegrationCodeMappings.prototype.componentDidMount = function () {
        var referrer = (qs.parse(window.location.search) || {}).referrer;
        // We don't start new session if the user was coming from choosing
        // the manual setup option flow from the issue details page
        var startSession = referrer === 'stacktrace-issue-details' ? false : true;
        integrationUtil_1.trackIntegrationEvent('integrations.code_mappings_viewed', {
            integration: this.props.integration.provider.key,
            integration_type: 'first_party',
        }, this.props.organization, { startSession: startSession });
    };
    IntegrationCodeMappings.prototype.renderBody = function () {
        var _this = this;
        var pathConfigs = this.pathConfigs;
        var integration = this.props.integration;
        return (<react_1.Fragment>
        <alert_1.default type="info" icon={<icons_1.IconInfo />}>
          {locale_1.tct('Got feedback? Email [email:ecosystem-feedback@sentry.io].', {
                email: <a href="mailto:ecosystem-feedback@sentry.io"/>,
            })}
        </alert_1.default>
        <textBlock_1.default>
          {locale_1.tct("Code Mappings are used to map stack trace file paths to source code file paths. These mappings are the basis for features like Stack Trace Linking. To learn more, [link: read the docs].", {
                link: (<externalLink_1.default href="https://docs.sentry.io/product/integrations/gitlab/#stack-trace-linking"/>),
            })}
        </textBlock_1.default>

        <panels_1.Panel>
          <panels_1.PanelHeader disablePadding hasButtons>
            <HeaderLayout>
              <repositoryProjectPathConfigRow_1.NameRepoColumn>{locale_1.t('Code Mappings')}</repositoryProjectPathConfigRow_1.NameRepoColumn>
              <repositoryProjectPathConfigRow_1.InputPathColumn>{locale_1.t('Stack Trace Root')}</repositoryProjectPathConfigRow_1.InputPathColumn>
              <repositoryProjectPathConfigRow_1.OutputPathColumn>{locale_1.t('Source Code Root')}</repositoryProjectPathConfigRow_1.OutputPathColumn>
              <repositoryProjectPathConfigRow_1.ButtonColumn>
                <AddButton onClick={function () { return _this.openModal(); }} size="xsmall" icon={<icons_1.IconAdd size="xs" isCircled/>}>
                  {locale_1.t('Add Mapping')}
                </AddButton>
              </repositoryProjectPathConfigRow_1.ButtonColumn>
            </HeaderLayout>
          </panels_1.PanelHeader>
          <panels_1.PanelBody>
            {pathConfigs.length === 0 && (<emptyMessage_1.default icon={integrationUtil_1.getIntegrationIcon(integration.provider.key, 'lg')} action={<button_1.default href={"https://docs.sentry.io/product/integrations/" + integration.provider.key + "/#stack-trace-linking"} size="small" onClick={function () {
                        integrationUtil_1.trackIntegrationEvent('integrations.stacktrace_docs_clicked', {
                            view: 'integration_configuration_detail',
                            provider: _this.props.integration.provider.key,
                        }, _this.props.organization);
                    }}>
                    View Documentation
                  </button_1.default>}>
                Set up stack trace linking by adding a code mapping.
              </emptyMessage_1.default>)}
            {pathConfigs
                .map(function (pathConfig) {
                var project = _this.getMatchingProject(pathConfig);
                // this should never happen since our pathConfig would be deleted
                // if project was deleted
                if (!project) {
                    return null;
                }
                return (<ConfigPanelItem key={pathConfig.id}>
                    <Layout>
                      <repositoryProjectPathConfigRow_1.default pathConfig={pathConfig} project={project} onEdit={_this.openModal} onDelete={_this.handleDelete}/>
                    </Layout>
                  </ConfigPanelItem>);
            })
                .filter(function (item) { return !!item; })}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </react_1.Fragment>);
    };
    return IntegrationCodeMappings;
}(asyncComponent_1.default));
exports.default = withOrganization_1.default(IntegrationCodeMappings);
var AddButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject([""], [""])));
var Layout = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n  grid-template-columns: 4.5fr 2.5fr 2.5fr 1.6fr;\n  grid-template-areas: 'name-repo input-path output-path button';\n"], ["\n  display: grid;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n  grid-template-columns: 4.5fr 2.5fr 2.5fr 1.6fr;\n  grid-template-areas: 'name-repo input-path output-path button';\n"])), space_1.default(1));
var HeaderLayout = styled_1.default(Layout)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n  margin: 0;\n  margin-left: ", ";\n"], ["\n  align-items: center;\n  margin: 0;\n  margin-left: ", ";\n"])), space_1.default(2));
var ConfigPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject([""], [""])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=integrationCodeMappings.jsx.map