Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var annotatedText_1 = tslib_1.__importDefault(require("app/components/events/meta/annotatedText"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var highlight_1 = tslib_1.__importDefault(require("app/components/highlight"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var urls_1 = require("app/utils/discover/urls");
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var summary_1 = tslib_1.__importDefault(require("./summary"));
var Default = function (_a) {
    var breadcrumb = _a.breadcrumb, event = _a.event, orgId = _a.orgId, searchTerm = _a.searchTerm;
    return (<summary_1.default kvData={breadcrumb.data}>
    {(breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.message) && (<annotatedText_1.default value={<FormatMessage searchTerm={searchTerm} event={event} orgId={orgId} breadcrumb={breadcrumb} message={breadcrumb.message}/>} meta={metaProxy_1.getMeta(breadcrumb, 'message')}/>)}
  </summary_1.default>);
};
function isEventId(maybeEventId) {
    // maybeEventId is an event id if it's a hex string of 32 characters long
    return /^[a-fA-F0-9]{32}$/.test(maybeEventId);
}
var FormatMessage = withProjects_1.default(function FormatMessageInner(_a) {
    var searchTerm = _a.searchTerm, event = _a.event, message = _a.message, breadcrumb = _a.breadcrumb, projects = _a.projects, loadingProjects = _a.loadingProjects, orgId = _a.orgId;
    var content = <highlight_1.default text={searchTerm}>{message}</highlight_1.default>;
    if (!loadingProjects &&
        typeof orgId === 'string' &&
        breadcrumb.category === 'sentry.transaction' &&
        isEventId(message)) {
        var maybeProject = projects.find(function (project) {
            return project.id === event.projectID;
        });
        if (!maybeProject) {
            return content;
        }
        var projectSlug = maybeProject.slug;
        var eventSlug = urls_1.generateEventSlug({ project: projectSlug, id: message });
        return <link_1.default to={urls_1.eventDetailsRoute({ orgSlug: orgId, eventSlug: eventSlug })}>{content}</link_1.default>;
    }
    return content;
});
exports.default = Default;
//# sourceMappingURL=default.jsx.map