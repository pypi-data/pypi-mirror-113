Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
var react_router_1 = require("react-router");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var getRouteStringFromRoutes_1 = tslib_1.__importDefault(require("app/utils/getRouteStringFromRoutes"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withProject_1 = tslib_1.__importDefault(require("app/utils/withProject"));
var ERROR_NAME = 'Permission Denied';
var PermissionDenied = /** @class */ (function (_super) {
    tslib_1.__extends(PermissionDenied, _super);
    function PermissionDenied() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PermissionDenied.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, routes = _a.routes;
        var route = getRouteStringFromRoutes_1.default(routes);
        Sentry.withScope(function (scope) {
            scope.setFingerprint([ERROR_NAME, route]);
            scope.setExtra('route', route);
            scope.setExtra('orgFeatures', (organization && organization.features) || []);
            scope.setExtra('orgAccess', (organization && organization.access) || []);
            scope.setExtra('projectFeatures', (project && project.features) || []);
            Sentry.captureException(new Error("" + ERROR_NAME + (route ? " : " + route : '')));
        });
    };
    PermissionDenied.prototype.render = function () {
        return (<react_document_title_1.default title={locale_1.t('Permission Denied')}>
        <organization_1.PageContent>
          <loadingError_1.default message={locale_1.tct("Your role does not have the necessary permissions to access this\n               resource, please read more about [link:organizational roles]", {
                link: (<externalLink_1.default href="https://docs.sentry.io/product/accounts/membership/"/>),
            })}/>
        </organization_1.PageContent>
      </react_document_title_1.default>);
    };
    return PermissionDenied;
}(react_1.Component));
exports.default = react_router_1.withRouter(withOrganization_1.default(withProject_1.default(PermissionDenied)));
//# sourceMappingURL=permissionDenied.jsx.map