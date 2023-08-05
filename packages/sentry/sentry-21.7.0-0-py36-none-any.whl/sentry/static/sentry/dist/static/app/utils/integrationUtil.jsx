Object.defineProperty(exports, "__esModule", { value: true });
exports.platfromToIntegrationMap = exports.getIntegrationIcon = exports.safeGetQsParam = exports.convertIntegrationTypeToSnakeCase = exports.getIntegrationType = exports.isDocumentIntegration = exports.isPlugin = exports.isSentryApp = exports.getCategoriesForIntegration = exports.getCategories = exports.getSentryAppInstallStatus = exports.getIntegrationFeatureGate = exports.trackIntegrationEvent = void 0;
var tslib_1 = require("tslib");
var capitalize_1 = tslib_1.__importDefault(require("lodash/capitalize"));
var qs = tslib_1.__importStar(require("query-string"));
var icons_1 = require("app/icons");
var hookStore_1 = tslib_1.__importDefault(require("app/stores/hookStore"));
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
var mapIntegrationParams = function (analyticsParams) {
    // Reload expects integration_status even though it's not relevant for non-sentry apps
    // Passing in a dummy value of published in those cases
    var fullParams = tslib_1.__assign({}, analyticsParams);
    if (analyticsParams.integration && analyticsParams.integration_type !== 'sentry_app') {
        fullParams.integration_status = 'published';
    }
    return fullParams;
};
// wrapper around trackAdvancedAnalyticsEvent which has some extra
// data massaging above
function trackIntegrationEvent(eventKey, analyticsParams, org, // integration events should always be tied to an org
options) {
    return advancedAnalytics_1.trackAdvancedAnalyticsEvent(eventKey, analyticsParams, org, options, mapIntegrationParams);
}
exports.trackIntegrationEvent = trackIntegrationEvent;
/**
 * In sentry.io the features list supports rendering plan details. If the hook
 * is not registered for rendering the features list like this simply show the
 * features as a normal list.
 */
var generateFeaturesList = function (p) { return (<ul>
    {p.features.map(function (f, i) { return (<li key={i}>{f.description}</li>); })}
  </ul>); };
var generateIntegrationFeatures = function (p) {
    return p.children({
        disabled: false,
        disabledReason: null,
        ungatedFeatures: p.features,
        gatedFeatureGroups: [],
    });
};
var defaultFeatureGateComponents = {
    IntegrationFeatures: generateIntegrationFeatures,
    IntegrationDirectoryFeatures: generateIntegrationFeatures,
    FeatureList: generateFeaturesList,
    IntegrationDirectoryFeatureList: generateFeaturesList,
};
var getIntegrationFeatureGate = function () {
    var defaultHook = function () { return defaultFeatureGateComponents; };
    var featureHook = hookStore_1.default.get('integrations:feature-gates')[0] || defaultHook;
    return featureHook();
};
exports.getIntegrationFeatureGate = getIntegrationFeatureGate;
var getSentryAppInstallStatus = function (install) {
    if (install) {
        return capitalize_1.default(install.status);
    }
    return 'Not Installed';
};
exports.getSentryAppInstallStatus = getSentryAppInstallStatus;
var getCategories = function (features) {
    var transform = features.map(function (_a) {
        var featureGate = _a.featureGate;
        var feature = featureGate
            .replace(/integrations/g, '')
            .replace(/-/g, ' ')
            .trim();
        switch (feature) {
            case 'actionable notification':
                return 'notification action';
            case 'issue basic':
            case 'issue link':
            case 'issue sync':
                return 'project management';
            case 'commits':
                return 'source code management';
            case 'chat unfurl':
                return 'chat';
            default:
                return feature;
        }
    });
    return tslib_1.__spreadArray([], tslib_1.__read(new Set(transform)));
};
exports.getCategories = getCategories;
var getCategoriesForIntegration = function (integration) {
    if (isSentryApp(integration)) {
        return ['internal', 'unpublished'].includes(integration.status)
            ? [integration.status]
            : exports.getCategories(integration.featureData);
    }
    if (isPlugin(integration)) {
        return exports.getCategories(integration.featureDescriptions);
    }
    if (isDocumentIntegration(integration)) {
        return exports.getCategories(integration.features);
    }
    return exports.getCategories(integration.metadata.features);
};
exports.getCategoriesForIntegration = getCategoriesForIntegration;
function isSentryApp(integration) {
    return !!integration.uuid;
}
exports.isSentryApp = isSentryApp;
function isPlugin(integration) {
    return integration.hasOwnProperty('shortName');
}
exports.isPlugin = isPlugin;
function isDocumentIntegration(integration) {
    return integration.hasOwnProperty('docUrl');
}
exports.isDocumentIntegration = isDocumentIntegration;
var getIntegrationType = function (integration) {
    if (isSentryApp(integration)) {
        return 'sentry_app';
    }
    if (isPlugin(integration)) {
        return 'plugin';
    }
    if (isDocumentIntegration(integration)) {
        return 'document';
    }
    return 'first_party';
};
exports.getIntegrationType = getIntegrationType;
var convertIntegrationTypeToSnakeCase = function (type) {
    switch (type) {
        case 'firstParty':
            return 'first_party';
        case 'sentryApp':
            return 'sentry_app';
        case 'documentIntegration':
            return 'document';
        default:
            return type;
    }
};
exports.convertIntegrationTypeToSnakeCase = convertIntegrationTypeToSnakeCase;
var safeGetQsParam = function (param) {
    try {
        var query = qs.parse(window.location.search) || {};
        return query[param];
    }
    catch (_a) {
        return undefined;
    }
};
exports.safeGetQsParam = safeGetQsParam;
var getIntegrationIcon = function (integrationType, size) {
    var iconSize = size || 'md';
    switch (integrationType) {
        case 'bitbucket':
            return <icons_1.IconBitbucket size={iconSize}/>;
        case 'gitlab':
            return <icons_1.IconGitlab size={iconSize}/>;
        case 'github':
        case 'github_enterprise':
            return <icons_1.IconGithub size={iconSize}/>;
        case 'jira':
        case 'jira_server':
            return <icons_1.IconJira size={iconSize}/>;
        case 'vsts':
            return <icons_1.IconVsts size={iconSize}/>;
        default:
            return <icons_1.IconGeneric size={iconSize}/>;
    }
};
exports.getIntegrationIcon = getIntegrationIcon;
// used for project creation and onboarding
// determines what integration maps to what project platform
exports.platfromToIntegrationMap = {
    'node-awslambda': 'aws_lambda',
    'python-awslambda': 'aws_lambda',
};
//# sourceMappingURL=integrationUtil.jsx.map