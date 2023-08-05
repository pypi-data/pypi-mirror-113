Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
function ErrorMessage(_a) {
    var _b, _c;
    var error = _a.error, groupId = _a.groupId, onRetry = _a.onRetry;
    function getErrorMessage(errorCode) {
        switch (errorCode) {
            case 'merged_issues':
                return {
                    title: locale_1.t('An issue can only contain one fingerprint'),
                    subTitle: locale_1.t('This issue needs to be fully unmerged before grouping levels can be shown'),
                };
            case 'missing_feature':
                return {
                    title: locale_1.t('This project does not have the grouping tree feature'),
                };
            case 'no_events':
                return {
                    title: locale_1.t('This issue has no events'),
                };
            case 'not_hierarchical':
                return {
                    title: locale_1.t('This issue does not have hierarchical grouping'),
                };
            default:
                return undefined;
        }
    }
    if (typeof error === 'string') {
        return <alert_1.default type="warning">{error}</alert_1.default>;
    }
    if (error.status === 403 && ((_b = error.responseJSON) === null || _b === void 0 ? void 0 : _b.detail)) {
        var _d = error.responseJSON.detail, code = _d.code, message = _d.message;
        var errorMessage = getErrorMessage(code);
        return (<panels_1.Panel>
        <emptyMessage_1.default size="large" title={(_c = errorMessage === null || errorMessage === void 0 ? void 0 : errorMessage.title) !== null && _c !== void 0 ? _c : message} description={errorMessage === null || errorMessage === void 0 ? void 0 : errorMessage.subTitle} action={code === 'merged_issues' ? (<button_1.default priority="primary" to={"/organizations/sentry/issues/" + groupId + "/merged/?" + location.search}>
                {locale_1.t('Unmerge issue')}
              </button_1.default>) : undefined}/>
      </panels_1.Panel>);
    }
    return (<loadingError_1.default message={locale_1.t('Unable to load grouping levels, please try again later')} onRetry={onRetry}/>);
}
exports.default = ErrorMessage;
//# sourceMappingURL=errorMessage.jsx.map