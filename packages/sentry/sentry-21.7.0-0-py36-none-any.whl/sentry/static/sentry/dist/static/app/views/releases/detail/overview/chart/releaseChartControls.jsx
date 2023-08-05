Object.defineProperty(exports, "__esModule", { value: true });
exports.PERFORMANCE_AXIS = exports.EventType = exports.YAxis = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var optionSelector_1 = tslib_1.__importDefault(require("app/components/charts/optionSelector"));
var styles_1 = require("app/components/charts/styles");
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var notAvailableMessages_1 = tslib_1.__importDefault(require("app/constants/notAvailableMessages"));
var locale_1 = require("app/locale");
var fields_1 = require("app/utils/discover/fields");
var constants_1 = require("app/utils/performance/vitals/constants");
var YAxis;
(function (YAxis) {
    YAxis["SESSIONS"] = "sessions";
    YAxis["USERS"] = "users";
    YAxis["CRASH_FREE"] = "crashFree";
    YAxis["SESSION_DURATION"] = "sessionDuration";
    YAxis["EVENTS"] = "events";
    YAxis["FAILED_TRANSACTIONS"] = "failedTransactions";
    YAxis["COUNT_DURATION"] = "countDuration";
    YAxis["COUNT_VITAL"] = "countVital";
})(YAxis = exports.YAxis || (exports.YAxis = {}));
var EventType;
(function (EventType) {
    EventType["ALL"] = "all";
    EventType["CSP"] = "csp";
    EventType["DEFAULT"] = "default";
    EventType["ERROR"] = "error";
    EventType["TRANSACTION"] = "transaction";
})(EventType = exports.EventType || (exports.EventType = {}));
exports.PERFORMANCE_AXIS = [
    YAxis.FAILED_TRANSACTIONS,
    YAxis.COUNT_DURATION,
    YAxis.COUNT_VITAL,
];
var ReleaseChartControls = function (_a) {
    var summary = _a.summary, yAxis = _a.yAxis, onYAxisChange = _a.onYAxisChange, organization = _a.organization, hasHealthData = _a.hasHealthData, hasDiscover = _a.hasDiscover, hasPerformance = _a.hasPerformance, _b = _a.eventType, eventType = _b === void 0 ? EventType.ALL : _b, onEventTypeChange = _a.onEventTypeChange, _c = _a.vitalType, vitalType = _c === void 0 ? fields_1.WebVital.LCP : _c, onVitalTypeChange = _a.onVitalTypeChange;
    var noHealthDataTooltip = !hasHealthData
        ? notAvailableMessages_1.default.releaseHealth
        : undefined;
    var noDiscoverTooltip = !hasDiscover ? notAvailableMessages_1.default.discover : undefined;
    var noPerformanceTooltip = !hasPerformance
        ? notAvailableMessages_1.default.performance
        : undefined;
    var yAxisOptions = [
        {
            value: YAxis.SESSIONS,
            label: locale_1.t('Session Count'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.SESSION_DURATION,
            label: locale_1.t('Session Duration'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.USERS,
            label: locale_1.t('User Count'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.CRASH_FREE,
            label: locale_1.t('Crash Free Rate'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.FAILED_TRANSACTIONS,
            label: locale_1.t('Failure Count'),
            disabled: !hasPerformance,
            tooltip: noPerformanceTooltip,
        },
        {
            value: YAxis.COUNT_DURATION,
            label: locale_1.t('Slow Duration Count'),
            disabled: !hasPerformance,
            tooltip: noPerformanceTooltip,
        },
        {
            value: YAxis.COUNT_VITAL,
            label: locale_1.t('Slow Vital Count'),
            disabled: !hasPerformance,
            tooltip: noPerformanceTooltip,
        },
        {
            value: YAxis.EVENTS,
            label: locale_1.t('Event Count'),
            disabled: !hasDiscover && !hasPerformance,
            tooltip: noDiscoverTooltip,
        },
    ];
    var getSummaryHeading = function () {
        switch (yAxis) {
            case YAxis.USERS:
                return locale_1.t('Total Active Users');
            case YAxis.CRASH_FREE:
                return locale_1.t('Average Rate');
            case YAxis.SESSION_DURATION:
                return locale_1.t('Median Duration');
            case YAxis.EVENTS:
                return locale_1.t('Total Events');
            case YAxis.FAILED_TRANSACTIONS:
                return locale_1.t('Failed Transactions');
            case YAxis.COUNT_DURATION:
                return locale_1.t('Count over %sms', organization.apdexThreshold);
            case YAxis.COUNT_VITAL:
                return vitalType !== fields_1.WebVital.CLS
                    ? locale_1.t('Count over %sms', constants_1.WEB_VITAL_DETAILS[vitalType].poorThreshold)
                    : locale_1.t('Count over %s', constants_1.WEB_VITAL_DETAILS[vitalType].poorThreshold);
            case YAxis.SESSIONS:
            default:
                return locale_1.t('Total Sessions');
        }
    };
    return (<styles_1.ChartControls>
      <styles_1.InlineContainer>
        <styles_1.SectionHeading key="total-label">
          {getSummaryHeading()}
          <questionTooltip_1.default position="top" size="sm" title={locale_1.t('This value includes only the current release.')}/>
        </styles_1.SectionHeading>
        <styles_1.SectionValue key="total-value">{summary}</styles_1.SectionValue>
      </styles_1.InlineContainer>
      <styles_1.InlineContainer>
        <SecondarySelector yAxis={yAxis} eventType={eventType} onEventTypeChange={onEventTypeChange} vitalType={vitalType} onVitalTypeChange={onVitalTypeChange}/>
        <optionSelector_1.default title={locale_1.t('Display')} selected={yAxis} options={yAxisOptions} onChange={onYAxisChange}/>
      </styles_1.InlineContainer>
    </styles_1.ChartControls>);
};
var eventTypeOptions = [
    { value: EventType.ALL, label: locale_1.t('All') },
    { value: EventType.CSP, label: locale_1.t('CSP') },
    { value: EventType.DEFAULT, label: locale_1.t('Default') },
    { value: EventType.ERROR, label: 'Error' },
    { value: EventType.TRANSACTION, label: locale_1.t('Transaction') },
];
var vitalTypeOptions = [
    fields_1.WebVital.FP,
    fields_1.WebVital.FCP,
    fields_1.WebVital.LCP,
    fields_1.WebVital.FID,
    fields_1.WebVital.CLS,
].map(function (vital) { return ({ value: vital, label: constants_1.WEB_VITAL_DETAILS[vital].name }); });
function SecondarySelector(_a) {
    var yAxis = _a.yAxis, eventType = _a.eventType, onEventTypeChange = _a.onEventTypeChange, vitalType = _a.vitalType, onVitalTypeChange = _a.onVitalTypeChange;
    switch (yAxis) {
        case YAxis.EVENTS:
            return (<optionSelector_1.default title={locale_1.t('Event Type')} selected={eventType} options={eventTypeOptions} onChange={onEventTypeChange}/>);
        case YAxis.COUNT_VITAL:
            return (<optionSelector_1.default title={locale_1.t('Vital')} selected={vitalType} options={vitalTypeOptions} onChange={onVitalTypeChange}/>);
        default:
            return null;
    }
}
exports.default = ReleaseChartControls;
//# sourceMappingURL=releaseChartControls.jsx.map