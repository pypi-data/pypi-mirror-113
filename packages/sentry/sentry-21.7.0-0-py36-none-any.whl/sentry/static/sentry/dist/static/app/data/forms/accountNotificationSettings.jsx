Object.defineProperty(exports, "__esModule", { value: true });
exports.fields = exports.route = void 0;
var locale_1 = require("app/locale");
// Export route to make these forms searchable by label/help
exports.route = '/settings/account/notifications/';
exports.fields = {
    subscribeByDefault: {
        name: 'subscribeByDefault',
        type: 'boolean',
        label: locale_1.t('Send Me Alerts'),
        // TODO(billy): Make this a real link
        help: locale_1.t('Enable this to receive notifications for Alerts sent to your teams. You will always receive alerts configured to be sent directly to you.'),
    },
    workflowNotifications: {
        name: 'workflowNotifications',
        type: 'radio',
        label: locale_1.t('Send Me Workflow Notifications'),
        choices: [
            [0, locale_1.t('Always')],
            [1, locale_1.t('Only On Issues I Subscribe To')],
            [2, locale_1.t('Never')],
        ],
        help: locale_1.t('E.g. changes in issue assignment, resolution status, and comments.'),
    },
    weeklyReports: {
        // Form is not visible because currently not implemented
        name: 'weeklyReports',
        type: 'boolean',
        label: locale_1.t('Send Me Weekly Reports'),
        help: locale_1.t("Reports contain a summary of what's happened within your organization."),
        disabled: true,
    },
    deployNotifications: {
        name: 'deployNotifications',
        type: 'radio',
        label: locale_1.t('Send Me Deploy Notifications'),
        choices: [
            [2, locale_1.t('Always')],
            [3, locale_1.t('Only On Deploys With My Commits')],
            [4, locale_1.t('Never')],
        ],
        help: locale_1.t('Deploy emails include release, environment and commit overviews.'),
    },
    personalActivityNotifications: {
        name: 'personalActivityNotifications',
        type: 'boolean',
        label: locale_1.t('Notify Me About My Own Activity'),
        help: locale_1.t('Enable this to receive notifications about your own actions on Sentry.'),
    },
    selfAssignOnResolve: {
        name: 'selfAssignOnResolve',
        type: 'boolean',
        label: locale_1.t("Claim Unassigned Issues I've Resolved"),
        help: locale_1.t("You'll receive notifications about any changes that happen afterwards."),
    },
};
var formGroups = [
    {
        title: locale_1.t('Alerts'),
        fields: [exports.fields.subscribeByDefault],
    },
    {
        title: locale_1.t('Workflow Notifications'),
        fields: [exports.fields.workflowNotifications],
    },
    {
        title: locale_1.t('Email Routing'),
        fields: [],
    },
    {
        title: locale_1.t('Weekly Reports'),
        fields: [],
    },
    {
        title: locale_1.t('Deploy Notifications'),
        fields: [exports.fields.deployNotifications],
    },
    {
        title: locale_1.t('My Activity'),
        fields: [exports.fields.personalActivityNotifications, exports.fields.selfAssignOnResolve],
    },
];
exports.default = formGroups;
//# sourceMappingURL=accountNotificationSettings.jsx.map