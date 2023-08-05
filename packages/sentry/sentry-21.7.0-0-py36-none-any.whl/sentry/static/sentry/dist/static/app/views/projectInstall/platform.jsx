Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectInstallPlatform = void 0;
var tslib_1 = require("tslib");
require("prism-sentry/index.css");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var projects_1 = require("app/actionCreators/projects");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var notFound_1 = tslib_1.__importDefault(require("app/components/errors/notFound"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var platformCategories_1 = require("app/data/platformCategories");
var platforms_1 = tslib_1.__importDefault(require("app/data/platforms"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var projects_2 = tslib_1.__importDefault(require("app/utils/projects"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var ProjectInstallPlatform = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectInstallPlatform, _super);
    function ProjectInstallPlatform() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: false,
            html: '',
        };
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, params, orgId, projectId, platform, html, error_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, params = _a.params;
                        orgId = params.orgId, projectId = params.projectId, platform = params.platform;
                        this.setState({ loading: true });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, projects_1.loadDocs(api, orgId, projectId, platform)];
                    case 2:
                        html = (_b.sent()).html;
                        this.setState({ html: html });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.setState({ error: error_1 });
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ loading: false });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ProjectInstallPlatform.prototype.componentDidMount = function () {
        this.fetchData();
        window.scrollTo(0, 0);
        var platform = this.props.params.platform;
        // redirect if platform is not known.
        if (!platform || platform === 'other') {
            this.redirectToNeutralDocs();
        }
    };
    Object.defineProperty(ProjectInstallPlatform.prototype, "isGettingStarted", {
        get: function () {
            return window.location.href.indexOf('getting-started') > 0;
        },
        enumerable: false,
        configurable: true
    });
    ProjectInstallPlatform.prototype.redirectToNeutralDocs = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        var url = "/organizations/" + orgId + "/projects/" + projectId + "/getting-started/";
        react_router_1.browserHistory.push(url);
    };
    ProjectInstallPlatform.prototype.render = function () {
        var _a;
        var params = this.props.params;
        var orgId = params.orgId, projectId = params.projectId;
        var platform = platforms_1.default.find(function (p) { return p.id === params.platform; });
        if (!platform) {
            return <notFound_1.default />;
        }
        var issueStreamLink = "/organizations/" + orgId + "/issues/";
        var performanceOverviewLink = "/organizations/" + orgId + "/performance/";
        var gettingStartedLink = "/organizations/" + orgId + "/projects/" + projectId + "/getting-started/";
        var platformLink = (_a = platform.link) !== null && _a !== void 0 ? _a : undefined;
        return (<react_1.Fragment>
        <StyledPageHeader>
          <h2>{locale_1.t('Configure %(platform)s', { platform: platform.name })}</h2>
          <buttonBar_1.default gap={1}>
            <button_1.default size="small" to={gettingStartedLink}>
              {locale_1.t('< Back')}
            </button_1.default>
            <button_1.default size="small" href={platformLink} external>
              {locale_1.t('Full Documentation')}
            </button_1.default>
          </buttonBar_1.default>
        </StyledPageHeader>

        <div>
          <alert_1.default type="info" icon={<icons_1.IconInfo />}>
            {locale_1.tct("\n             This is a quick getting started guide. For in-depth instructions\n             on integrating Sentry with [platform], view\n             [docLink:our complete documentation].", {
                platform: platform.name,
                docLink: <a href={platformLink}/>,
            })}
          </alert_1.default>

          {this.state.loading ? (<loadingIndicator_1.default />) : this.state.error ? (<loadingError_1.default onRetry={this.fetchData}/>) : (<react_1.Fragment>
              <sentryDocumentTitle_1.default title={locale_1.t('Configure') + " " + platform.name} projectSlug={projectId}/>
              <DocumentationWrapper dangerouslySetInnerHTML={{ __html: this.state.html }}/>
            </react_1.Fragment>)}

          {this.isGettingStarted && (<projects_2.default key={orgId + "-" + projectId} orgId={orgId} slugs={[projectId]} passthroughPlaceholderProject={false}>
              {function (_a) {
                    var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, fetching = _a.fetching, fetchError = _a.fetchError;
                    var projectsLoading = !initiallyLoaded && fetching;
                    var projectFilter = !projectsLoading && !fetchError && projects.length
                        ? {
                            project: projects[0].id,
                        }
                        : {};
                    var showPerformancePrompt = platformCategories_1.performance.includes(platform.id);
                    return (<react_1.Fragment>
                    {showPerformancePrompt && (<feature_1.default features={['performance-view']} hookName="feature-disabled:performance-new-project">
                        {function (_a) {
                                var hasFeature = _a.hasFeature;
                                if (hasFeature) {
                                    return null;
                                }
                                return (<StyledAlert type="info" icon={<icons_1.IconInfo />}>
                              {locale_1.t("Your selected platform supports performance, but your organization does not have performance enabled.")}
                            </StyledAlert>);
                            }}
                      </feature_1.default>)}

                    <StyledButtonBar gap={1}>
                      <button_1.default priority="primary" busy={projectsLoading} to={{
                            pathname: issueStreamLink,
                            query: projectFilter,
                            hash: '#welcome',
                        }}>
                        {locale_1.t('Take me to Issues')}
                      </button_1.default>
                      <button_1.default busy={projectsLoading} to={{
                            pathname: performanceOverviewLink,
                            query: projectFilter,
                        }}>
                        {locale_1.t('Take me to Performance')}
                      </button_1.default>
                    </StyledButtonBar>
                  </react_1.Fragment>);
                }}
            </projects_2.default>)}
        </div>
      </react_1.Fragment>);
    };
    return ProjectInstallPlatform;
}(react_1.Component));
exports.ProjectInstallPlatform = ProjectInstallPlatform;
var DocumentationWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  .gatsby-highlight {\n    margin-bottom: ", ";\n\n    &:last-child {\n      margin-bottom: 0;\n    }\n  }\n\n  .alert {\n    margin-bottom: ", ";\n    border-radius: ", ";\n  }\n\n  p {\n    line-height: 1.5;\n  }\n  pre {\n    word-break: break-all;\n    white-space: pre-wrap;\n  }\n"], ["\n  .gatsby-highlight {\n    margin-bottom: ", ";\n\n    &:last-child {\n      margin-bottom: 0;\n    }\n  }\n\n  .alert {\n    margin-bottom: ", ";\n    border-radius: ", ";\n  }\n\n  p {\n    line-height: 1.5;\n  }\n  pre {\n    word-break: break-all;\n    white-space: pre-wrap;\n  }\n"])), space_1.default(3), space_1.default(3), function (p) { return p.theme.borderRadius; });
var StyledButtonBar = styled_1.default(buttonBar_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  width: max-content;\n\n  @media (max-width: ", ") {\n    width: auto;\n    grid-row-gap: ", ";\n    grid-auto-flow: row;\n  }\n"], ["\n  margin-top: ", ";\n  width: max-content;\n\n  @media (max-width: ", ") {\n    width: auto;\n    grid-row-gap: ", ";\n    grid-auto-flow: row;\n  }\n"])), space_1.default(3), function (p) { return p.theme.breakpoints[0]; }, space_1.default(1));
var StyledPageHeader = styled_1.default(organization_1.PageHeader)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n\n  h2 {\n    margin: 0;\n  }\n\n  @media (max-width: ", ") {\n    flex-direction: column;\n    align-items: flex-start;\n\n    h2 {\n      margin-bottom: ", ";\n    }\n  }\n"], ["\n  margin-bottom: ", ";\n\n  h2 {\n    margin: 0;\n  }\n\n  @media (max-width: ", ") {\n    flex-direction: column;\n    align-items: flex-start;\n\n    h2 {\n      margin-bottom: ", ";\n    }\n  }\n"])), space_1.default(3), function (p) { return p.theme.breakpoints[0]; }, space_1.default(2));
var StyledAlert = styled_1.default(alert_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(2));
exports.default = withApi_1.default(withOrganization_1.default(ProjectInstallPlatform));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=platform.jsx.map