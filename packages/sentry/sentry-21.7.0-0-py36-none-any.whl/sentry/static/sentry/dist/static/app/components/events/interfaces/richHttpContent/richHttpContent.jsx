Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var clippedBox_1 = tslib_1.__importDefault(require("app/components/clippedBox"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var richHttpContentClippedBoxBodySection_1 = tslib_1.__importDefault(require("./richHttpContentClippedBoxBodySection"));
var richHttpContentClippedBoxKeyValueList_1 = tslib_1.__importDefault(require("./richHttpContentClippedBoxKeyValueList"));
var RichHttpContent = function (_a) {
    var data = _a.data;
    return (<react_1.Fragment>
    {utils_1.defined(data.query) && (<richHttpContentClippedBoxKeyValueList_1.default title={locale_1.t('Query String')} data={data.query} meta={metaProxy_1.getMeta(data, 'query')} isContextData/>)}
    {utils_1.defined(data.fragment) && (<clippedBox_1.default title={locale_1.t('Fragment')}>
        <errorBoundary_1.default mini>
          <pre>{data.fragment}</pre>
        </errorBoundary_1.default>
      </clippedBox_1.default>)}
    {utils_1.defined(data.data) && (<richHttpContentClippedBoxBodySection_1.default data={data.data} meta={metaProxy_1.getMeta(data, 'data')} inferredContentType={data.inferredContentType}/>)}
    {utils_1.defined(data.cookies) && Object.keys(data.cookies).length > 0 && (<richHttpContentClippedBoxKeyValueList_1.default defaultCollapsed title={locale_1.t('Cookies')} data={data.cookies} meta={metaProxy_1.getMeta(data, 'cookies')}/>)}
    {utils_1.defined(data.headers) && (<richHttpContentClippedBoxKeyValueList_1.default title={locale_1.t('Headers')} data={data.headers} meta={metaProxy_1.getMeta(data, 'headers')}/>)}
    {utils_1.defined(data.env) && (<richHttpContentClippedBoxKeyValueList_1.default defaultCollapsed title={locale_1.t('Environment')} data={data.env} meta={metaProxy_1.getMeta(data, 'env')}/>)}
  </react_1.Fragment>);
};
exports.default = RichHttpContent;
//# sourceMappingURL=richHttpContent.jsx.map