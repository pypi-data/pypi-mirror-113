Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var utils_1 = require("app/components/events/interfaces/spans/utils");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var spanTree_1 = tslib_1.__importDefault(require("./spanTree"));
var utils_2 = require("./utils");
var TraceView = function (props) {
    var baselineEvent = props.baselineEvent, regressionEvent = props.regressionEvent;
    if (!utils_2.isTransactionEvent(baselineEvent) || !utils_2.isTransactionEvent(regressionEvent)) {
        return (<emptyMessage_1.default>
        <icons_1.IconWarning color="gray300" size="lg"/>
        <p>{locale_1.t('One of the given events is not a transaction.')}</p>
      </emptyMessage_1.default>);
    }
    var baselineTraceContext = utils_1.getTraceContext(baselineEvent);
    var regressionTraceContext = utils_1.getTraceContext(regressionEvent);
    if (!baselineTraceContext || !regressionTraceContext) {
        return (<emptyMessage_1.default>
        <icons_1.IconWarning color="gray300" size="lg"/>
        <p>{locale_1.t('There is no trace found in either of the given transactions.')}</p>
      </emptyMessage_1.default>);
    }
    return <spanTree_1.default baselineEvent={baselineEvent} regressionEvent={regressionEvent}/>;
};
exports.default = TraceView;
//# sourceMappingURL=traceView.jsx.map