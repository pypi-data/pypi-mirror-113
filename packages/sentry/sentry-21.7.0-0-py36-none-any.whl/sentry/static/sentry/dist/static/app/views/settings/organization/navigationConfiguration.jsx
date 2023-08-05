Object.defineProperty(exports, "__esModule", { value: true });
var locale_1 = require("app/locale");
var pathPrefix = '/settings/:orgId';
var organizationNavigation = [
    {
        name: locale_1.t('Organization'),
        items: [
            {
                path: pathPrefix + "/",
                title: locale_1.t('General Settings'),
                index: true,
                description: locale_1.t('Configure general settings for an organization'),
                id: 'general',
            },
            {
                path: pathPrefix + "/projects/",
                title: locale_1.t('Projects'),
                description: locale_1.t("View and manage an organization's projects"),
                id: 'projects',
            },
            {
                path: pathPrefix + "/teams/",
                title: locale_1.t('Teams'),
                description: locale_1.t("Manage an organization's teams"),
                id: 'teams',
            },
            {
                path: pathPrefix + "/members/",
                title: locale_1.t('Members'),
                show: function (_a) {
                    var access = _a.access;
                    return access.has('member:read');
                },
                description: locale_1.t('Manage user membership for an organization'),
                id: 'members',
            },
            {
                path: pathPrefix + "/performance/",
                title: locale_1.t('Performance'),
                show: function (_a) {
                    var features = _a.features;
                    return features.has('performance-view');
                },
                description: locale_1.t('Manage performance settings'),
                id: 'performance',
            },
            {
                path: pathPrefix + "/security-and-privacy/",
                title: locale_1.t('Security & Privacy'),
                description: locale_1.t('Configuration related to dealing with sensitive data and other security settings. (Data Scrubbing, Data Privacy, Data Scrubbing)'),
                id: 'security-and-privacy',
            },
            {
                path: pathPrefix + "/auth/",
                title: locale_1.t('Auth'),
                description: locale_1.t('Configure single sign-on'),
                id: 'sso',
            },
            {
                path: pathPrefix + "/api-keys/",
                title: locale_1.t('API Keys'),
                show: function (_a) {
                    var access = _a.access, features = _a.features;
                    return features.has('api-keys') && access.has('org:admin');
                },
                id: 'api-keys',
            },
            {
                path: pathPrefix + "/audit-log/",
                title: locale_1.t('Audit Log'),
                show: function (_a) {
                    var access = _a.access;
                    return access.has('org:write');
                },
                description: locale_1.t('View the audit log for an organization'),
                id: 'audit-log',
            },
            {
                path: pathPrefix + "/rate-limits/",
                title: locale_1.t('Rate Limits'),
                show: function (_a) {
                    var access = _a.access, features = _a.features;
                    return features.has('legacy-rate-limits') && access.has('org:write');
                },
                description: locale_1.t('Configure rate limits for all projects in the organization'),
                id: 'rate-limits',
            },
            {
                path: pathPrefix + "/relay/",
                title: locale_1.t('Relay'),
                show: function (_a) {
                    var features = _a.features;
                    return features.has('relay');
                },
                description: locale_1.t('Manage relays connected to the organization'),
                id: 'relay',
            },
            {
                path: pathPrefix + "/repos/",
                title: locale_1.t('Repositories'),
                description: locale_1.t('Manage repositories connected to the organization'),
                id: 'repos',
            },
            {
                path: pathPrefix + "/integrations/",
                title: locale_1.t('Integrations'),
                description: locale_1.t('Manage organization-level integrations, including: Slack, Github, Bitbucket, Jira, and Azure DevOps'),
                id: 'integrations',
                recordAnalytics: true,
            },
            {
                path: pathPrefix + "/developer-settings/",
                title: locale_1.t('Developer Settings'),
                description: locale_1.t('Manage developer applications'),
                id: 'developer-settings',
            },
        ],
    },
];
exports.default = organizationNavigation;
//# sourceMappingURL=navigationConfiguration.jsx.map