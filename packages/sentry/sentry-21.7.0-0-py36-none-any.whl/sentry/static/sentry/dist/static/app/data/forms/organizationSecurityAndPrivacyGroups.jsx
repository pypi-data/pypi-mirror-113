Object.defineProperty(exports, "__esModule", { value: true });
exports.route = void 0;
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var crashReports_1 = require("app/utils/crashReports");
// Export route to make these forms searchable by label/help
exports.route = '/settings/:orgId/security-and-privacy/';
exports.default = [
    {
        title: locale_1.t('Security & Privacy'),
        fields: [
            {
                name: 'require2FA',
                type: 'boolean',
                label: locale_1.t('Require Two-Factor Authentication'),
                help: locale_1.t('Require and enforce two-factor authentication for all members'),
                confirm: {
                    true: locale_1.t('This will remove all members without two-factor authentication' +
                        ' from your organization. It will also send them an email to setup 2FA' +
                        ' and reinstate their access and settings. Do you want to continue?'),
                    false: locale_1.t('Are you sure you want to allow users to access your organization without having two-factor authentication enabled?'),
                },
            },
            {
                name: 'requireEmailVerification',
                type: 'boolean',
                label: locale_1.t('Require Email Verification'),
                help: locale_1.t('Require and enforce email address verification for all members'),
                visible: function (_a) {
                    var features = _a.features;
                    return features.has('required-email-verification');
                },
                confirm: {
                    true: locale_1.t('This will remove all members whose email addresses are not verified' +
                        ' from your organization. It will also send them an email to verify their address' +
                        ' and reinstate their access and settings. Do you want to continue?'),
                    false: locale_1.t('Are you sure you want to allow users to access your organization without verifying their email address?'),
                },
            },
            {
                name: 'allowSharedIssues',
                type: 'boolean',
                label: locale_1.t('Allow Shared Issues'),
                help: locale_1.t('Enable sharing of limited details on issues to anonymous users'),
                confirm: {
                    true: locale_1.t('Are you sure you want to allow sharing issues to anonymous users?'),
                },
            },
            {
                name: 'enhancedPrivacy',
                type: 'boolean',
                label: locale_1.t('Enhanced Privacy'),
                help: locale_1.t('Enable enhanced privacy controls to limit personally identifiable information (PII) as well as source code in things like notifications'),
                confirm: {
                    false: locale_1.t('Disabling this can have privacy implications for ALL projects, are you sure you want to continue?'),
                },
            },
            {
                name: 'scrapeJavaScript',
                type: 'boolean',
                confirm: {
                    false: locale_1.t("Are you sure you want to disable sourcecode fetching for JavaScript events? This will affect Sentry's ability to aggregate issues if you're not already uploading sourcemaps as artifacts."),
                },
                label: locale_1.t('Allow JavaScript Source Fetching'),
                help: locale_1.t('Allow Sentry to scrape missing JavaScript source context when possible'),
            },
            {
                name: 'storeCrashReports',
                type: 'select',
                label: locale_1.t('Store Native Crash Reports'),
                help: locale_1.t('Store native crash reports such as Minidumps for improved processing and download in issue details'),
                visible: function (_a) {
                    var features = _a.features;
                    return features.has('event-attachments');
                },
                // HACK: some organization can have limit of stored crash reports a number that's not in the options (legacy reasons),
                // we therefore display it in a placeholder
                placeholder: function (_a) {
                    var value = _a.value;
                    return crashReports_1.formatStoreCrashReports(value);
                },
                choices: function () {
                    return crashReports_1.getStoreCrashReportsValues(crashReports_1.SettingScope.Organization).map(function (value) { return [
                        value,
                        crashReports_1.formatStoreCrashReports(value),
                    ]; });
                },
            },
            {
                name: 'allowJoinRequests',
                type: 'boolean',
                label: locale_1.t('Allow Join Requests'),
                help: locale_1.t('Allow users to request to join your organization'),
                confirm: {
                    true: locale_1.t('Are you sure you want to allow users to request to join your organization?'),
                },
                visible: function (_a) {
                    var hasSsoEnabled = _a.hasSsoEnabled;
                    return !hasSsoEnabled;
                },
            },
        ],
    },
    {
        title: locale_1.t('Data Scrubbing'),
        fields: [
            {
                name: 'dataScrubber',
                type: 'boolean',
                label: locale_1.t('Require Data Scrubber'),
                help: locale_1.t('Require server-side data scrubbing be enabled for all projects'),
                confirm: {
                    false: locale_1.t('Disabling this can have privacy implications for ALL projects, are you sure you want to continue?'),
                },
            },
            {
                name: 'dataScrubberDefaults',
                type: 'boolean',
                label: locale_1.t('Require Using Default Scrubbers'),
                help: locale_1.t('Require the default scrubbers be applied to prevent things like passwords and credit cards from being stored for all projects'),
                confirm: {
                    false: locale_1.t('Disabling this can have privacy implications for ALL projects, are you sure you want to continue?'),
                },
            },
            {
                name: 'sensitiveFields',
                type: 'string',
                multiline: true,
                autosize: true,
                maxRows: 10,
                rows: 1,
                placeholder: 'e.g. email',
                label: locale_1.t('Global Sensitive Fields'),
                help: locale_1.t('Additional field names to match against when scrubbing data for all projects. Separate multiple entries with a newline.'),
                extraHelp: locale_1.t('Note: These fields will be used in addition to project specific fields.'),
                getValue: function (val) { return utils_1.extractMultilineFields(val); },
                setValue: function (val) { return utils_1.convertMultilineFieldValue(val); },
            },
            {
                name: 'safeFields',
                type: 'string',
                multiline: true,
                autosize: true,
                maxRows: 10,
                rows: 1,
                placeholder: locale_1.t('e.g. business-email'),
                label: locale_1.t('Global Safe Fields'),
                help: locale_1.t('Field names which data scrubbers should ignore. Separate multiple entries with a newline.'),
                extraHelp: locale_1.t('Note: These fields will be used in addition to project specific fields'),
                getValue: function (val) { return utils_1.extractMultilineFields(val); },
                setValue: function (val) { return utils_1.convertMultilineFieldValue(val); },
            },
            {
                name: 'scrubIPAddresses',
                type: 'boolean',
                label: locale_1.t('Prevent Storing of IP Addresses'),
                help: locale_1.t('Preventing IP addresses from being stored for new events on all projects'),
                confirm: {
                    false: locale_1.t('Disabling this can have privacy implications for ALL projects, are you sure you want to continue?'),
                },
            },
        ],
    },
];
//# sourceMappingURL=organizationSecurityAndPrivacyGroups.jsx.map