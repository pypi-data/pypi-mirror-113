Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var isNil_1 = tslib_1.__importDefault(require("lodash/isNil"));
var crashContent_1 = tslib_1.__importDefault(require("app/components/events/interfaces/crashContent"));
var pill_1 = tslib_1.__importDefault(require("app/components/pill"));
var pills_1 = tslib_1.__importDefault(require("app/components/pills"));
var locale_1 = require("app/locale");
var noStackTraceMessage_1 = tslib_1.__importDefault(require("../noStackTraceMessage"));
var Content = function (_a) {
    var _b;
    var event = _a.event, projectId = _a.projectId, data = _a.data, stackView = _a.stackView, stackType = _a.stackType, newestFirst = _a.newestFirst, exception = _a.exception, stacktrace = _a.stacktrace, stackTraceNotFound = _a.stackTraceNotFound;
    return (<div className="thread">
    {data && (!isNil_1.default(data === null || data === void 0 ? void 0 : data.id) || !!(data === null || data === void 0 ? void 0 : data.name)) && (<pills_1.default>
        {!isNil_1.default(data.id) && <pill_1.default name={locale_1.t('id')} value={String(data.id)}/>}
        {!!((_b = data.name) === null || _b === void 0 ? void 0 : _b.trim()) && <pill_1.default name={locale_1.t('name')} value={data.name}/>}
        <pill_1.default name={locale_1.t('was active')} value={data.current}/>
        <pill_1.default name={locale_1.t('errored')} className={data.crashed ? 'false' : 'true'}>
          {data.crashed ? locale_1.t('yes') : locale_1.t('no')}
        </pill_1.default>
      </pills_1.default>)}

    {stackTraceNotFound ? (<noStackTraceMessage_1.default message={(data === null || data === void 0 ? void 0 : data.crashed) ? locale_1.t('Thread Errored') : undefined}/>) : (<crashContent_1.default event={event} stackType={stackType} stackView={stackView} newestFirst={newestFirst} projectId={projectId} exception={exception} stacktrace={stacktrace}/>)}
  </div>);
};
exports.default = Content;
//# sourceMappingURL=content.jsx.map