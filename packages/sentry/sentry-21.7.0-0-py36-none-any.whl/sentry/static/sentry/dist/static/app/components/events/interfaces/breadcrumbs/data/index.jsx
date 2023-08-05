Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var breadcrumbs_1 = require("app/types/breadcrumbs");
var default_1 = tslib_1.__importDefault(require("./default"));
var exception_1 = tslib_1.__importDefault(require("./exception"));
var http_1 = tslib_1.__importDefault(require("./http"));
var Data = function (_a) {
    var breadcrumb = _a.breadcrumb, event = _a.event, orgId = _a.orgId, searchTerm = _a.searchTerm;
    if (breadcrumb.type === breadcrumbs_1.BreadcrumbType.HTTP) {
        return <http_1.default breadcrumb={breadcrumb} searchTerm={searchTerm}/>;
    }
    if (breadcrumb.type === breadcrumbs_1.BreadcrumbType.WARNING ||
        breadcrumb.type === breadcrumbs_1.BreadcrumbType.ERROR) {
        return <exception_1.default breadcrumb={breadcrumb} searchTerm={searchTerm}/>;
    }
    return (<default_1.default event={event} orgId={orgId} breadcrumb={breadcrumb} searchTerm={searchTerm}/>);
};
exports.default = Data;
//# sourceMappingURL=index.jsx.map