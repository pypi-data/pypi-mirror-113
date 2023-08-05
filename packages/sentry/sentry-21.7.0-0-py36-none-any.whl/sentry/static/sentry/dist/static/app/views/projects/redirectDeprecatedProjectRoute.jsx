Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isString_1 = tslib_1.__importDefault(require("lodash/isString"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var getRouteStringFromRoutes_1 = tslib_1.__importDefault(require("app/utils/getRouteStringFromRoutes"));
var redirect_1 = tslib_1.__importDefault(require("app/utils/redirect"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var ProjectDetailsInner = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectDetailsInner, _super);
    function ProjectDetailsInner() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: null,
            project: null,
        };
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, orgId, projectSlug, project, error_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.setState({
                            loading: true,
                            error: null,
                        });
                        _a = this.props, orgId = _a.orgId, projectSlug = _a.projectSlug;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.props.api.requestPromise("/projects/" + orgId + "/" + projectSlug + "/")];
                    case 2:
                        project = _b.sent();
                        this.setState({
                            loading: false,
                            error: null,
                            project: project,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.setState({
                            loading: false,
                            error: error_1,
                            project: null,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ProjectDetailsInner.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ProjectDetailsInner.prototype.getProjectId = function () {
        if (this.state.project) {
            return this.state.project.id;
        }
        return null;
    };
    ProjectDetailsInner.prototype.hasProjectId = function () {
        var projectID = this.getProjectId();
        return isString_1.default(projectID) && projectID.length > 0;
    };
    ProjectDetailsInner.prototype.getOrganizationId = function () {
        if (this.state.project) {
            return this.state.project.organization.id;
        }
        return null;
    };
    ProjectDetailsInner.prototype.render = function () {
        var childrenProps = tslib_1.__assign(tslib_1.__assign({}, this.state), { projectId: this.getProjectId(), hasProjectId: this.hasProjectId(), organizationId: this.getOrganizationId() });
        return this.props.children(childrenProps);
    };
    return ProjectDetailsInner;
}(React.Component));
var ProjectDetails = withApi_1.default(ProjectDetailsInner);
var redirectDeprecatedProjectRoute = function (generateRedirectRoute) {
    var RedirectDeprecatedProjectRoute = /** @class */ (function (_super) {
        tslib_1.__extends(RedirectDeprecatedProjectRoute, _super);
        function RedirectDeprecatedProjectRoute() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.trackRedirect = function (organizationId, nextRoute) {
                var payload = {
                    feature: 'global_views',
                    url: getRouteStringFromRoutes_1.default(_this.props.routes),
                    org_id: parseInt(organizationId, 10),
                };
                // track redirects of deprecated URLs for analytics
                analytics_1.analytics('deprecated_urls.redirect', payload);
                return nextRoute;
            };
            return _this;
        }
        RedirectDeprecatedProjectRoute.prototype.render = function () {
            var _this = this;
            var params = this.props.params;
            var orgId = params.orgId;
            return (<Wrapper>
          <ProjectDetails orgId={orgId} projectSlug={params.projectId}>
            {function (_a) {
                    var loading = _a.loading, error = _a.error, hasProjectId = _a.hasProjectId, projectId = _a.projectId, organizationId = _a.organizationId;
                    if (loading) {
                        return <loadingIndicator_1.default />;
                    }
                    if (!hasProjectId || !organizationId) {
                        if (error && error.status === 404) {
                            return (<alert_1.default type="error">
                      {locale_1.t('The project you were looking for was not found.')}
                    </alert_1.default>);
                        }
                        return <loadingError_1.default />;
                    }
                    var routeProps = {
                        orgId: orgId,
                        projectId: projectId,
                        router: { params: params },
                    };
                    return (<redirect_1.default router={_this.props.router} to={_this.trackRedirect(organizationId, generateRedirectRoute(routeProps))}/>);
                }}
          </ProjectDetails>
        </Wrapper>);
        };
        return RedirectDeprecatedProjectRoute;
    }(React.Component));
    return RedirectDeprecatedProjectRoute;
};
exports.default = redirectDeprecatedProjectRoute;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  padding: ", ";\n"], ["\n  flex: 1;\n  padding: ", ";\n"])), space_1.default(3));
var templateObject_1;
//# sourceMappingURL=redirectDeprecatedProjectRoute.jsx.map