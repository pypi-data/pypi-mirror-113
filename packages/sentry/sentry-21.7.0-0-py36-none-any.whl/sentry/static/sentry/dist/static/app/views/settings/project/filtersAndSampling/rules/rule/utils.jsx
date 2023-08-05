Object.defineProperty(exports, "__esModule", { value: true });
exports.getInnerNameLabel = void 0;
var tslib_1 = require("tslib");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var locale_1 = require("app/locale");
var dynamicSampling_1 = require("app/types/dynamicSampling");
function getInnerNameLabel(name) {
    switch (name) {
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_ENVIRONMENT:
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_ENVIRONMENT:
            return locale_1.t('Environment');
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_RELEASE:
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_RELEASE:
            return locale_1.t('Release');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_USER_ID:
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_USER_ID:
            return locale_1.t('User Id');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_USER_SEGMENT:
        case dynamicSampling_1.DynamicSamplingInnerName.TRACE_USER_SEGMENT:
            return locale_1.t('User Segment');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_BROWSER_EXTENSIONS:
            return locale_1.t('Browser Extensions');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_LOCALHOST:
            return locale_1.t('Localhost');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_WEB_CRAWLERS:
            return locale_1.t('Web Crawlers');
        case dynamicSampling_1.DynamicSamplingInnerName.EVENT_LEGACY_BROWSER:
            return locale_1.t('Legacy Browsers');
        default: {
            Sentry.captureException(new Error('Unknown dynamic sampling condition inner name'));
            return null; // this shall never happen
        }
    }
}
exports.getInnerNameLabel = getInnerNameLabel;
//# sourceMappingURL=utils.jsx.map