Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var keyValueList_1 = tslib_1.__importDefault(require("app/components/events/interfaces/keyValueList"));
var annotated_1 = tslib_1.__importDefault(require("app/components/events/meta/annotated"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var Message = function (_a) {
    var data = _a.data;
    var renderParams = function () {
        var params = data === null || data === void 0 ? void 0 : data.params;
        if (!params || utils_1.objectIsEmpty(params)) {
            return null;
        }
        // NB: Always render params, regardless of whether they appear in the
        // formatted string due to structured logging frameworks, like Serilog. They
        // only format some parameters into the formatted string, but we want to
        // display all of them.
        if (Array.isArray(params)) {
            var arrayData = params.map(function (value, i) {
                var key = "#" + i;
                return {
                    key: key,
                    value: value,
                    subject: key,
                };
            });
            return <keyValueList_1.default data={arrayData} isSorted={false} isContextData/>;
        }
        var objectData = Object.entries(params).map(function (_a) {
            var _b = tslib_1.__read(_a, 2), key = _b[0], value = _b[1];
            return ({
                key: key,
                value: value,
                subject: key,
                meta: metaProxy_1.getMeta(params, key),
            });
        });
        return <keyValueList_1.default data={objectData} isSorted={false} isContextData/>;
    };
    return (<eventDataSection_1.default type="message" title={locale_1.t('Message')}>
      <annotated_1.default object={data} objectKey="formatted">
        {function (value) { return <pre className="plain">{value}</pre>; }}
      </annotated_1.default>
      {renderParams()}
    </eventDataSection_1.default>);
};
exports.default = Message;
//# sourceMappingURL=message.jsx.map