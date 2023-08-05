var _a;
Object.defineProperty(exports, "__esModule", { value: true });
exports.getMatchFieldPlaceholder = exports.isLegacyBrowser = exports.Transaction = exports.LEGACY_BROWSER_LIST = exports.modalCss = void 0;
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var locale_1 = require("app/locale");
var dynamicSampling_1 = require("app/types/dynamicSampling");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
exports.modalCss = react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  [role='document'] {\n    overflow: initial;\n  }\n\n  @media (min-width: ", ") {\n    width: 100%;\n    max-width: 700px;\n  }\n"], ["\n  [role='document'] {\n    overflow: initial;\n  }\n\n  @media (min-width: ", ") {\n    width: 100%;\n    max-width: 700px;\n  }\n"])), theme_1.default.breakpoints[0]);
exports.LEGACY_BROWSER_LIST = (_a = {},
    _a[dynamicSampling_1.LegacyBrowser.IE_PRE_9] = {
        icon: 'internet-explorer',
        title: locale_1.t('Internet Explorer Version 8 and lower'),
    },
    _a[dynamicSampling_1.LegacyBrowser.IE9] = {
        icon: 'internet-explorer',
        title: locale_1.t('Internet Explorer Version 9'),
    },
    _a[dynamicSampling_1.LegacyBrowser.IE10] = {
        icon: 'internet-explorer',
        title: locale_1.t('Internet Explorer Version 10'),
    },
    _a[dynamicSampling_1.LegacyBrowser.IE11] = {
        icon: 'internet-explorer',
        title: locale_1.t('Internet Explorer Version 11'),
    },
    _a[dynamicSampling_1.LegacyBrowser.SAFARI_PRE_6] = {
        icon: 'safari',
        title: locale_1.t('Safari Version 5 and lower'),
    },
    _a[dynamicSampling_1.LegacyBrowser.OPERA_PRE_15] = {
        icon: 'opera',
        title: locale_1.t('Opera Version 14 and lower'),
    },
    _a[dynamicSampling_1.LegacyBrowser.OPERA_MINI_PRE_8] = {
        icon: 'opera',
        title: locale_1.t('Opera Mini Version 8 and lower'),
    },
    _a[dynamicSampling_1.LegacyBrowser.ANDROID_PRE_4] = {
        icon: 'android',
        title: locale_1.t('Android Version 3 and lower'),
    },
    _a);
var Transaction;
(function (Transaction) {
    Transaction["ALL"] = "all";
    Transaction["MATCH_CONDITIONS"] = "match-conditions";
})(Transaction = exports.Transaction || (exports.Transaction = {}));
function isLegacyBrowser(maybe) {
    return maybe.every(function (m) { return !!exports.LEGACY_BROWSER_LIST[m]; });
}
exports.isLegacyBrowser = isLegacyBrowser;
function getMatchFieldPlaceholder(category) {
    switch (category) {
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_LEGACY_BROWSER:
            return locale_1.t('Match all selected legacy browsers below');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_BROWSER_EXTENSIONS:
            return locale_1.t('Match all browser extensions');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_LOCALHOST:
            return locale_1.t('Match all localhosts');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_WEB_CRAWLERS:
            return locale_1.t('Match all web crawlers');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_USER_ID:
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_USER_ID:
            return locale_1.t('ex. 4711 (Multiline)');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_USER_SEGMENT:
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_USER_SEGMENT:
            return locale_1.t('ex. paid, common (Multiline)');
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_ENVIRONMENT:
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_ENVIRONMENT:
            return locale_1.t('ex. prod or dev (Multiline)');
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_RELEASE:
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_RELEASE:
            return locale_1.t('ex. 1* or [I3].[0-9].* (Multiline)');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_IP_ADDRESSES:
            return locale_1.t('ex. 127.0.0.1 or 10.0.0.0/8 (Multiline)');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_CSP:
            return locale_1.t('ex. file://* or example.com (Multiline)');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_ERROR_MESSAGES:
            return locale_1.t('ex. TypeError* (Multiline)');
        default:
            return '';
    }
}
exports.getMatchFieldPlaceholder = getMatchFieldPlaceholder;
var templateObject_1;
//# sourceMappingURL=utils.jsx.map