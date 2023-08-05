Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var clippedBox_1 = tslib_1.__importDefault(require("app/components/clippedBox"));
var contextData_1 = tslib_1.__importDefault(require("app/components/contextData"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var keyValueList_1 = tslib_1.__importDefault(require("app/components/events/interfaces/keyValueList"));
var annotatedText_1 = tslib_1.__importDefault(require("app/components/events/meta/annotatedText"));
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var getTransformedData_1 = tslib_1.__importDefault(require("./getTransformedData"));
function RichHttpContentClippedBoxBodySection(_a) {
    var data = _a.data, meta = _a.meta, inferredContentType = _a.inferredContentType;
    if (!utils_1.defined(data)) {
        return null;
    }
    function getContent() {
        switch (inferredContentType) {
            case 'application/json':
                return (<contextData_1.default data-test-id="rich-http-content-body-context-data" data={data} preserveQuotes/>);
            case 'application/x-www-form-urlencoded':
            case 'multipart/form-data': {
                var transformedData = getTransformedData_1.default(data).map(function (_a) {
                    var _b = tslib_1.__read(_a, 2), key = _b[0], v = _b[1];
                    return ({
                        key: key,
                        subject: key,
                        value: v,
                        meta: meta,
                    });
                });
                if (!transformedData.length) {
                    return null;
                }
                return (<keyValueList_1.default data-test-id="rich-http-content-body-key-value-list" data={transformedData} isContextData/>);
            }
            default:
                return (<pre data-test-id="rich-http-content-body-section-pre">
            <annotatedText_1.default value={data && JSON.stringify(data, null, 2)} meta={meta} data-test-id="rich-http-content-body-context-data"/>
          </pre>);
        }
    }
    var content = getContent();
    if (!content) {
        return null;
    }
    return (<clippedBox_1.default title={locale_1.t('Body')} defaultClipped>
      <errorBoundary_1.default mini>{content}</errorBoundary_1.default>
    </clippedBox_1.default>);
}
exports.default = RichHttpContentClippedBoxBodySection;
//# sourceMappingURL=richHttpContentClippedBoxBodySection.jsx.map