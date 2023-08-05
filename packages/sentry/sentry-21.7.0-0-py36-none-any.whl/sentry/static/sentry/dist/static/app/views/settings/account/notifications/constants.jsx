Object.defineProperty(exports, "__esModule", { value: true });
exports.SELF_NOTIFICATION_SETTINGS_TYPES = exports.NOTIFICATION_SETTINGS_TYPES = exports.MIN_PROJECTS_FOR_PAGINATION = exports.MIN_PROJECTS_FOR_SEARCH = exports.VALUE_MAPPING = exports.ALL_PROVIDERS = void 0;
exports.ALL_PROVIDERS = {
    email: 'default',
    slack: 'never',
};
/** These values are stolen from the DB. */
exports.VALUE_MAPPING = {
    default: 0,
    never: 10,
    always: 20,
    subscribe_only: 30,
    committed_only: 40,
};
exports.MIN_PROJECTS_FOR_SEARCH = 3;
exports.MIN_PROJECTS_FOR_PAGINATION = 100;
exports.NOTIFICATION_SETTINGS_TYPES = [
    'alerts',
    'workflow',
    'deploy',
    'reports',
    'email',
];
exports.SELF_NOTIFICATION_SETTINGS_TYPES = [
    'personalActivityNotifications',
    'selfAssignOnResolve',
];
//# sourceMappingURL=constants.jsx.map