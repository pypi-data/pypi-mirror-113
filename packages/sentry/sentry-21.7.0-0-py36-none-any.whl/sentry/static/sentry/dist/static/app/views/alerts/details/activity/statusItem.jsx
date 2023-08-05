Object.defineProperty(exports, "__esModule", { value: true });
exports.getTriggerName = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var item_1 = tslib_1.__importDefault(require("app/components/activity/item"));
var locale_1 = require("app/locale");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var types_1 = require("../../types");
/**
 * StatusItem renders status changes for Alerts
 *
 * For example: incident detected, or closed
 *
 * Note `activity.dateCreated` refers to when the activity was created vs.
 * `incident.dateStarted` which is when an incident was first detected or created
 */
var StatusItem = /** @class */ (function (_super) {
    tslib_1.__extends(StatusItem, _super);
    function StatusItem() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    StatusItem.prototype.render = function () {
        var _a = this.props, activity = _a.activity, authorName = _a.authorName, incident = _a.incident, showTime = _a.showTime;
        var isDetected = activity.type === types_1.IncidentActivityType.DETECTED;
        var isStarted = activity.type === types_1.IncidentActivityType.STARTED;
        var isClosed = activity.type === types_1.IncidentActivityType.STATUS_CHANGE &&
            activity.value === "" + types_1.IncidentStatus.CLOSED;
        var isTriggerChange = activity.type === types_1.IncidentActivityType.STATUS_CHANGE && !isClosed;
        // Unknown activity, don't render anything
        if (!isStarted && !isDetected && !isClosed && !isTriggerChange) {
            return null;
        }
        var currentTrigger = getTriggerName(activity.value);
        var previousTrigger = getTriggerName(activity.previousValue);
        return (<item_1.default showTime={showTime} author={{
                type: activity.user ? 'user' : 'system',
                user: activity.user || undefined,
            }} header={<div>
            {isTriggerChange &&
                    previousTrigger &&
                    locale_1.tct('Alert status changed from [previousTrigger] to [currentTrigger]', {
                        previousTrigger: previousTrigger,
                        currentTrigger: <StatusValue>{currentTrigger}</StatusValue>,
                    })}
            {isTriggerChange &&
                    !previousTrigger &&
                    locale_1.tct('Alert status changed to [currentTrigger]', {
                        currentTrigger: <StatusValue>{currentTrigger}</StatusValue>,
                    })}
            {isClosed &&
                    (incident === null || incident === void 0 ? void 0 : incident.statusMethod) === types_1.IncidentStatusMethod.RULE_UPDATED &&
                    locale_1.t('This alert has been auto-resolved because the rule that triggered it has been modified or deleted.')}
            {isClosed &&
                    (incident === null || incident === void 0 ? void 0 : incident.statusMethod) !== types_1.IncidentStatusMethod.RULE_UPDATED &&
                    locale_1.tct('[user] resolved the alert', {
                        user: <StatusValue>{authorName}</StatusValue>,
                    })}
            {isDetected &&
                    ((incident === null || incident === void 0 ? void 0 : incident.alertRule)
                        ? locale_1.t('Alert was created')
                        : locale_1.tct('[user] created an alert', {
                            user: <StatusValue>{authorName}</StatusValue>,
                        }))}
            {isStarted && locale_1.t('Trigger conditions were met for the interval')}
          </div>} date={getDynamicText_1.default({ value: activity.dateCreated, fixed: new Date(0) })} interval={isStarted ? incident === null || incident === void 0 ? void 0 : incident.alertRule.timeWindow : undefined}/>);
    };
    return StatusItem;
}(react_1.Component));
exports.default = StatusItem;
var StatusValue = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
function getTriggerName(value) {
    if (value === "" + types_1.IncidentStatus.WARNING) {
        return locale_1.t('Warning');
    }
    if (value === "" + types_1.IncidentStatus.CRITICAL) {
        return locale_1.t('Critical');
    }
    // Otherwise, activity type is not status change
    return '';
}
exports.getTriggerName = getTriggerName;
var templateObject_1;
//# sourceMappingURL=statusItem.jsx.map