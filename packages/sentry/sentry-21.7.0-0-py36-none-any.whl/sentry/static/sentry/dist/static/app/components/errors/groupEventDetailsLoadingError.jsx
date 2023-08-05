Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var detailedError_1 = tslib_1.__importDefault(require("app/components/errors/detailedError"));
var locale_1 = require("app/locale");
var GroupEventDetailsLoadingError = function (_a) {
    var onRetry = _a.onRetry, environments = _a.environments;
    var reasons = [
        locale_1.t('The events are still processing and are on their way'),
        locale_1.t('The events have been deleted'),
        locale_1.t('There is an internal systems error or active issue'),
    ];
    var message;
    if (environments.length === 0) {
        // All Environments case
        message = (<div>
        <p>{locale_1.t('This could be due to a handful of reasons:')}</p>
        <ol className="detailed-error-list">
          {reasons.map(function (reason, i) { return (<li key={i}>{reason}</li>); })}
        </ol>
      </div>);
    }
    else {
        message = (<div>{locale_1.t('No events were found for the currently selected environments')}</div>);
    }
    return (<detailedError_1.default className="group-event-details-error" onRetry={environments.length === 0 ? onRetry : undefined} heading={locale_1.t('Sorry, the events for this issue could not be found.')} message={message}/>);
};
exports.default = GroupEventDetailsLoadingError;
//# sourceMappingURL=groupEventDetailsLoadingError.jsx.map