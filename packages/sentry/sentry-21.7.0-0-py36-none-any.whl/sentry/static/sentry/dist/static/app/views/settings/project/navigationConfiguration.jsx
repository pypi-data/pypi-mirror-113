Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var locale_1 = require("app/locale");
var pathPrefix = '/settings/:orgId/projects/:projectId';
function getConfiguration(_a) {
    var project = _a.project, organization = _a.organization, debugFilesNeedsReview = _a.debugFilesNeedsReview;
    var plugins = ((project && project.plugins) || []).filter(function (plugin) { return plugin.enabled; });
    return [
        {
            name: locale_1.t('Project'),
            items: [
                {
                    path: pathPrefix + "/",
                    index: true,
                    title: locale_1.t('General Settings'),
                    description: locale_1.t('Configure general settings for a project'),
                },
                {
                    path: pathPrefix + "/teams/",
                    title: locale_1.t('Project Teams'),
                    description: locale_1.t('Manage team access for a project'),
                },
                {
                    path: pathPrefix + "/alerts/",
                    title: locale_1.t('Alerts'),
                    description: locale_1.t('Manage alert rules for a project'),
                },
                {
                    path: pathPrefix + "/tags/",
                    title: locale_1.t('Tags'),
                    description: locale_1.t("View and manage a  project's tags"),
                },
                {
                    path: pathPrefix + "/environments/",
                    title: locale_1.t('Environments'),
                    description: locale_1.t('Manage environments in a project'),
                },
                {
                    path: pathPrefix + "/ownership/",
                    title: locale_1.t('Issue Owners'),
                    description: locale_1.t('Manage issue ownership rules for a project'),
                },
                {
                    path: pathPrefix + "/data-forwarding/",
                    title: locale_1.t('Data Forwarding'),
                },
            ],
        },
        {
            name: locale_1.t('Processing'),
            items: [
                {
                    path: pathPrefix + "/filters/",
                    title: locale_1.t('Inbound Filters'),
                    description: locale_1.t("Configure a project's inbound filters (e.g. browsers, messages)"),
                },
                {
                    path: pathPrefix + "/filters-and-sampling/",
                    title: locale_1.t('Filters & Sampling'),
                    show: function () { var _a; return !!((_a = organization === null || organization === void 0 ? void 0 : organization.features) === null || _a === void 0 ? void 0 : _a.includes('filters-and-sampling')); },
                    description: locale_1.t("Manage an organization's inbound data"),
                    badge: function () { return 'new'; },
                },
                {
                    path: pathPrefix + "/security-and-privacy/",
                    title: locale_1.t('Security & Privacy'),
                    description: locale_1.t('Configuration related to dealing with sensitive data and other security settings. (Data Scrubbing, Data Privacy, Data Scrubbing) for a project'),
                },
                {
                    path: pathPrefix + "/issue-grouping/",
                    title: locale_1.t('Issue Grouping'),
                },
                {
                    path: pathPrefix + "/processing-issues/",
                    title: locale_1.t('Processing Issues'),
                    // eslint-disable-next-line no-shadow
                    badge: function (_a) {
                        var project = _a.project;
                        if (!project) {
                            return null;
                        }
                        if (project.processingIssues <= 0) {
                            return null;
                        }
                        return project.processingIssues > 99 ? '99+' : project.processingIssues;
                    },
                },
                {
                    path: pathPrefix + "/debug-symbols/",
                    title: locale_1.t('Debug Files'),
                    badge: debugFilesNeedsReview ? function () { return 'warning'; } : undefined,
                },
                {
                    path: pathPrefix + "/proguard/",
                    title: locale_1.t('ProGuard'),
                },
                {
                    path: pathPrefix + "/source-maps/",
                    title: locale_1.t('Source Maps'),
                },
                {
                    path: pathPrefix + "/performance/",
                    title: locale_1.t('Performance'),
                    badge: function () { return 'beta'; },
                    show: function () { var _a; return !!((_a = organization === null || organization === void 0 ? void 0 : organization.features) === null || _a === void 0 ? void 0 : _a.includes('project-transaction-threshold')); },
                },
            ],
        },
        {
            name: locale_1.t('SDK Setup'),
            items: [
                {
                    path: pathPrefix + "/install/",
                    title: locale_1.t('Instrumentation'),
                },
                {
                    path: pathPrefix + "/keys/",
                    title: locale_1.t('Client Keys (DSN)'),
                    description: locale_1.t("View and manage the project's client keys (DSN)"),
                },
                {
                    path: pathPrefix + "/release-tracking/",
                    title: locale_1.t('Releases'),
                },
                {
                    path: pathPrefix + "/security-headers/",
                    title: locale_1.t('Security Headers'),
                },
                {
                    path: pathPrefix + "/user-feedback/",
                    title: locale_1.t('User Feedback'),
                    description: locale_1.t('Configure user feedback reporting feature'),
                },
            ],
        },
        {
            name: locale_1.t('Legacy Integrations'),
            items: tslib_1.__spreadArray([
                {
                    path: pathPrefix + "/plugins/",
                    title: locale_1.t('Legacy Integrations'),
                    description: locale_1.t('View, enable, and disable all integrations for a project'),
                    id: 'legacy_integrations',
                    recordAnalytics: true,
                }
            ], tslib_1.__read(plugins.map(function (plugin) { return ({
                path: pathPrefix + "/plugins/" + plugin.id + "/",
                title: plugin.name,
                show: function (opts) { var _a; return (_a = opts === null || opts === void 0 ? void 0 : opts.access) === null || _a === void 0 ? void 0 : _a.has('project:write'); },
                id: 'plugin_details',
                recordAnalytics: true,
            }); }))),
        },
    ];
}
exports.default = getConfiguration;
//# sourceMappingURL=navigationConfiguration.jsx.map