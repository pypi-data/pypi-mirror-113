Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var locale_1 = require("app/locale");
function NoStackTraceMessage(_a) {
    var message = _a.message;
    return <alert_1.default type="error">{message !== null && message !== void 0 ? message : locale_1.t('No or unknown stacktrace')}</alert_1.default>;
}
exports.default = NoStackTraceMessage;
//# sourceMappingURL=noStackTraceMessage.jsx.map