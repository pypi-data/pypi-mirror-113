var _a, _b;
Object.defineProperty(exports, "__esModule", { value: true });
exports.MOBILE_VITAL_DETAILS = exports.WEB_VITAL_DETAILS = void 0;
var locale_1 = require("app/locale");
var fields_1 = require("app/utils/discover/fields");
exports.WEB_VITAL_DETAILS = (_a = {},
    _a[fields_1.WebVital.FP] = {
        slug: 'fp',
        name: locale_1.t('First Paint'),
        acronym: 'FP',
        description: locale_1.t('Render time of the first pixel loaded in the viewport (may overlap with FCP).'),
        poorThreshold: 3000,
        type: fields_1.measurementType(fields_1.WebVital.FP),
    },
    _a[fields_1.WebVital.FCP] = {
        slug: 'fcp',
        name: locale_1.t('First Contentful Paint'),
        acronym: 'FCP',
        description: locale_1.t('Render time of the first image, text or other DOM node in the viewport.'),
        poorThreshold: 3000,
        type: fields_1.measurementType(fields_1.WebVital.FCP),
    },
    _a[fields_1.WebVital.LCP] = {
        slug: 'lcp',
        name: locale_1.t('Largest Contentful Paint'),
        acronym: 'LCP',
        description: locale_1.t('Render time of the largest image, text or other DOM node in the viewport.'),
        poorThreshold: 4000,
        type: fields_1.measurementType(fields_1.WebVital.LCP),
    },
    _a[fields_1.WebVital.FID] = {
        slug: 'fid',
        name: locale_1.t('First Input Delay'),
        acronym: 'FID',
        description: locale_1.t('Response time of the browser to a user interaction (clicking, tapping, etc).'),
        poorThreshold: 300,
        type: fields_1.measurementType(fields_1.WebVital.FID),
    },
    _a[fields_1.WebVital.CLS] = {
        slug: 'cls',
        name: locale_1.t('Cumulative Layout Shift'),
        acronym: 'CLS',
        description: locale_1.t('Sum of layout shift scores that measure the visual stability of the page.'),
        poorThreshold: 0.25,
        type: fields_1.measurementType(fields_1.WebVital.CLS),
    },
    _a[fields_1.WebVital.TTFB] = {
        slug: 'ttfb',
        name: locale_1.t('Time to First Byte'),
        acronym: 'TTFB',
        description: locale_1.t("The time that it takes for a user's browser to receive the first byte of page content."),
        poorThreshold: 600,
        type: fields_1.measurementType(fields_1.WebVital.TTFB),
    },
    _a[fields_1.WebVital.RequestTime] = {
        slug: 'ttfb.requesttime',
        name: locale_1.t('Request Time'),
        acronym: 'RT',
        description: locale_1.t('Captures the time spent making the request and receiving the first byte of the response.'),
        poorThreshold: 600,
        type: fields_1.measurementType(fields_1.WebVital.RequestTime),
    },
    _a);
exports.MOBILE_VITAL_DETAILS = (_b = {},
    _b[fields_1.MobileVital.AppStartCold] = {
        slug: 'app_start_cold',
        name: locale_1.t('App Start Cold'),
        description: locale_1.t('Cold start is a measure of the application start up time from scratch.'),
        type: fields_1.measurementType(fields_1.MobileVital.AppStartCold),
    },
    _b[fields_1.MobileVital.AppStartWarm] = {
        slug: 'app_start_warm',
        name: locale_1.t('App Start Warm'),
        description: locale_1.t('Warm start is a measure of the application start up time while still in memory.'),
        type: fields_1.measurementType(fields_1.MobileVital.AppStartWarm),
    },
    _b[fields_1.MobileVital.FramesTotal] = {
        slug: 'frames_total',
        name: locale_1.t('Total Frames'),
        description: locale_1.t('Total frames is a count of the number of frames recorded within a transaction.'),
        type: fields_1.measurementType(fields_1.MobileVital.FramesTotal),
    },
    _b[fields_1.MobileVital.FramesSlow] = {
        slug: 'frames_slow',
        name: locale_1.t('Slow Frames'),
        description: locale_1.t('Slow frames is a count of the number of slow frames recorded within a transaction.'),
        type: fields_1.measurementType(fields_1.MobileVital.FramesSlow),
    },
    _b[fields_1.MobileVital.FramesFrozen] = {
        slug: 'frames_frozen',
        name: locale_1.t('Frozen Frames'),
        description: locale_1.t('Frozen frames is a count of the number of frozen frames recorded within a transaction.'),
        type: fields_1.measurementType(fields_1.MobileVital.FramesFrozen),
    },
    _b);
//# sourceMappingURL=constants.jsx.map