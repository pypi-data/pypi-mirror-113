Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var locale_1 = require("app/locale");
var hookStore_1 = tslib_1.__importDefault(require("app/stores/hookStore"));
var pathPrefix = '/settings/account';
function getConfiguration(_a) {
    var organization = _a.organization;
    return [
        {
            name: locale_1.t('Account'),
            items: [
                {
                    path: pathPrefix + "/details/",
                    title: locale_1.t('Account Details'),
                    description: locale_1.t('Change your account details and preferences (e.g. timezone/clock, avatar, language)'),
                },
                {
                    path: pathPrefix + "/security/",
                    title: locale_1.t('Security'),
                    description: locale_1.t('Change your account password and/or two factor authentication'),
                },
                {
                    path: pathPrefix + "/notifications/",
                    title: locale_1.t('Notifications'),
                    description: locale_1.t('Configure what email notifications to receive'),
                },
                {
                    path: pathPrefix + "/emails/",
                    title: locale_1.t('Email Addresses'),
                    description: locale_1.t('Add or remove secondary emails, change your primary email, verify your emails'),
                },
                {
                    path: pathPrefix + "/subscriptions/",
                    title: locale_1.t('Subscriptions'),
                    description: locale_1.t('Change Sentry marketing subscriptions you are subscribed to (GDPR)'),
                },
                {
                    path: pathPrefix + "/authorizations/",
                    title: locale_1.t('Authorized Applications'),
                    description: locale_1.t('Manage third-party applications that have access to your Sentry account'),
                },
                {
                    path: pathPrefix + "/identities/",
                    title: locale_1.t('Identities'),
                    description: locale_1.t('Manage your third-party identities that are associated to Sentry'),
                },
                {
                    path: pathPrefix + "/close-account/",
                    title: locale_1.t('Close Account'),
                    description: locale_1.t('Permanently close your Sentry account'),
                },
            ],
        },
        {
            name: locale_1.t('API'),
            items: tslib_1.__spreadArray([
                {
                    path: pathPrefix + "/api/applications/",
                    title: locale_1.t('Applications'),
                    description: locale_1.t('Add and configure OAuth2 applications'),
                },
                {
                    path: pathPrefix + "/api/auth-tokens/",
                    title: locale_1.t('Auth Tokens'),
                    description: locale_1.t("Authentication tokens allow you to perform actions against the Sentry API on behalf of your account. They're the easiest way to get started using the API."),
                }
            ], tslib_1.__read(hookStore_1.default.get('settings:api-navigation-config').flatMap(function (cb) {
                return cb(organization);
            }))),
        },
    ];
}
exports.default = getConfiguration;
//# sourceMappingURL=navigationConfiguration.jsx.map