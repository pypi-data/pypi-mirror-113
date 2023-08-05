Object.defineProperty(exports, "__esModule", { value: true });
exports.getFullLanguageDescription = exports.getRelativeTimeFromEventDateCreated = exports.getSourcePlugin = exports.getContextComponent = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var moment_timezone_1 = tslib_1.__importDefault(require("moment-timezone"));
var locale_1 = require("app/locale");
var plugins_1 = tslib_1.__importDefault(require("app/plugins"));
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var CONTEXT_TYPES = {
    default: require('app/components/events/contexts/default').default,
    app: require('app/components/events/contexts/app/app').default,
    device: require('app/components/events/contexts/device/device').default,
    os: require('app/components/events/contexts/operatingSystem/operatingSystem').default,
    runtime: require('app/components/events/contexts/runtime/runtime').default,
    user: require('app/components/events/contexts/user/user').default,
    gpu: require('app/components/events/contexts/gpu/gpu').default,
    trace: require('app/components/events/contexts/trace/trace').default,
    // 'redux.state' will be replaced with more generic context called 'state'
    'redux.state': require('app/components/events/contexts/redux').default,
    state: require('app/components/events/contexts/state').default,
};
function getContextComponent(type) {
    return CONTEXT_TYPES[type] || plugins_1.default.contexts[type] || CONTEXT_TYPES.default;
}
exports.getContextComponent = getContextComponent;
function getSourcePlugin(pluginContexts, contextType) {
    var e_1, _a;
    if (CONTEXT_TYPES[contextType]) {
        return null;
    }
    try {
        for (var pluginContexts_1 = tslib_1.__values(pluginContexts), pluginContexts_1_1 = pluginContexts_1.next(); !pluginContexts_1_1.done; pluginContexts_1_1 = pluginContexts_1.next()) {
            var plugin = pluginContexts_1_1.value;
            if (plugin.contexts.indexOf(contextType) >= 0) {
                return plugin;
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (pluginContexts_1_1 && !pluginContexts_1_1.done && (_a = pluginContexts_1.return)) _a.call(pluginContexts_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return null;
}
exports.getSourcePlugin = getSourcePlugin;
function getRelativeTimeFromEventDateCreated(eventDateCreated, timestamp, showTimestamp) {
    if (showTimestamp === void 0) { showTimestamp = true; }
    if (!utils_1.defined(timestamp)) {
        return timestamp;
    }
    var dateTime = moment_timezone_1.default(timestamp);
    if (!dateTime.isValid()) {
        return timestamp;
    }
    var relativeTime = "(" + dateTime.from(eventDateCreated, true) + " " + locale_1.t('before this event') + ")";
    if (!showTimestamp) {
        return <RelativeTime>{relativeTime}</RelativeTime>;
    }
    return (<react_1.Fragment>
      {timestamp}
      <RelativeTime>{relativeTime}</RelativeTime>
    </react_1.Fragment>);
}
exports.getRelativeTimeFromEventDateCreated = getRelativeTimeFromEventDateCreated;
// Typescript doesn't have types for DisplayNames yet and that's why the type assertion "any" is needed below.
// There is currently an open PR that intends to introduce the types https://github.com/microsoft/TypeScript/pull/44022
function getFullLanguageDescription(locale) {
    var sentryAppLanguageCode = configStore_1.default.get('languageCode');
    var _a = tslib_1.__read(locale.includes('_')
        ? locale.split('_')
        : locale.split('-'), 2), languageAbbreviation = _a[0], countryAbbreviation = _a[1];
    try {
        var languageNames = new Intl.DisplayNames(sentryAppLanguageCode, {
            type: 'language',
        });
        var languageName = languageNames.of(languageAbbreviation);
        if (countryAbbreviation) {
            var regionNames = new Intl.DisplayNames(sentryAppLanguageCode, {
                type: 'region',
            });
            var countryName = regionNames.of(countryAbbreviation.toUpperCase());
            return languageName + " (" + countryName + ")";
        }
        return languageName;
    }
    catch (_b) {
        return locale;
    }
}
exports.getFullLanguageDescription = getFullLanguageDescription;
var RelativeTime = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-left: ", ";\n"], ["\n  color: ", ";\n  margin-left: ", ";\n"])), function (p) { return p.theme.subText; }, space_1.default(0.5));
var templateObject_1;
//# sourceMappingURL=utils.jsx.map