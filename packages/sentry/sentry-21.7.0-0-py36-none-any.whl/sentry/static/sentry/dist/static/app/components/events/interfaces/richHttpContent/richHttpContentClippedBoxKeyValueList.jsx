Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var clippedBox_1 = tslib_1.__importDefault(require("app/components/clippedBox"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var keyValueList_1 = tslib_1.__importDefault(require("app/components/events/interfaces/keyValueList"));
var getTransformedData_1 = tslib_1.__importDefault(require("./getTransformedData"));
var RichHttpContentClippedBoxKeyValueList = function (_a) {
    var data = _a.data, title = _a.title, _b = _a.defaultCollapsed, defaultCollapsed = _b === void 0 ? false : _b, _c = _a.isContextData, isContextData = _c === void 0 ? false : _c, meta = _a.meta;
    var getContent = function (transformedData) {
        // Sentry API abbreviates long query string values, sometimes resulting in
        // an un-parsable querystring ... stay safe kids
        try {
            return (<keyValueList_1.default data={transformedData.map(function (_a) {
                    var _b = tslib_1.__read(_a, 2), key = _b[0], value = _b[1];
                    return ({
                        key: key,
                        subject: key,
                        value: value,
                        meta: meta,
                    });
                })} isContextData={isContextData}/>);
        }
        catch (_a) {
            return <pre>{data}</pre>;
        }
    };
    var transformedData = getTransformedData_1.default(data);
    if (!transformedData.length) {
        return null;
    }
    return (<clippedBox_1.default title={title} defaultClipped={defaultCollapsed}>
      <errorBoundary_1.default mini>{getContent(transformedData)}</errorBoundary_1.default>
    </clippedBox_1.default>);
};
exports.default = RichHttpContentClippedBoxKeyValueList;
//# sourceMappingURL=richHttpContentClippedBoxKeyValueList.jsx.map